import sublime
import sublime_plugin
import os
import re

from .code_getter import CodeGetter
from .code_sender import CodeSender
from .settings import Settings


def escape_dquote(cmd):
    cmd = cmd.replace('\\', '\\\\')
    cmd = cmd.replace('"', '\\"')
    return cmd


def escape_squote(cmd):
    cmd = cmd.replace('\\', '\\\\')
    cmd = cmd.replace("\'", "\'")
    return cmd

PATTERN = re.compile(r"""
    (?P<quote>["'])
    (?P<quoted_var>
        \$ (?: [_a-z][_a-z0-9]*  | \{[^}]*\} )
    )
    (?P=quote)
    |
    (?P<var>
        \$ (?: [_a-z][_a-z0-9]*  | \{[^}]*\} )
    )
""", re.VERBOSE)

def maybe_match(regex, string, default):
    match = re.search(regex, string)
    if match is not None:
        return match.group(1)
    else:
        return default

def parse_chunk_header(cmd):
    return (
        maybe_match(r'```{r (\S+)[,}]', cmd, 'tmp'),
        maybe_match(r'fig\.width *= *([^,}]+)', cmd, 4.5),
        maybe_match(r'fig\.height *= *([^,}]+)', cmd, 3),
    )

class SendCodeCommand(sublime_plugin.TextCommand):

    def resolve(self, cmd):
        view = self.view
        window = view.window()
        extracted_variables = window.extract_variables()
        if len(view.sel()) == 1:
            row, _ = view.rowcol(view.sel()[0].begin())
            extracted_variables["line"] = str(row + 1)

            word = view.substr(view.sel()[0])
            if not word:
                word = view.substr(view.word(view.sel()[0].begin()))
            extracted_variables["selection"] = word

        fname = view.file_name()
        if fname:
            fname = os.path.realpath(fname)
            for folder in window.folders():
                if fname.startswith(os.path.realpath(folder) + os.sep):
                    extracted_variables["current_folder"] = folder
                    break

        def convert(m):
            quote = m.group("quote")
            if quote:
                var = sublime.expand_variables(m.group("quoted_var"), extracted_variables)
                if quote == "'":
                    return "'" + escape_squote(var) + "'"
                else:
                    return '"' + escape_dquote(var) + '"'
            else:
                return sublime.expand_variables(m.group("var"), extracted_variables)

        cmd = PATTERN.sub(convert, cmd)

        return cmd

    def run(self, edit, advance=None, cell=False, cmd=None, prog=None, confirmation=None,
            prefix="", postfix="", setup=False):
        print('SendCode.run', prefix, postfix)
        is_rcall = self.view.score_selector(self.view.sel()[0].begin(), "rcall.julia")
        
        if advance is None:
            advance = Settings(self.view).get("auto_advance", True)

        # set CodeGetter before get_text() because get_text may change cursor locations.

        if confirmation:
            ok = sublime.ok_cancel_dialog(confirmation)
            if not ok:
                return

        sender = CodeSender.initialize(self.view, prog=prog, from_view=cmd is None)

        sender.bracketed_paste_mode = Settings(self.view).syntax() != 'sql'  # Fred hack
        if cmd:
            cmd = self.resolve(cmd)
        else:
            if Settings(self.view).syntax() == 'rmd':
                cell_cmd = CodeGetter.initialize(self.view, advance=False, cell=True, setup=setup).get_text()
                if cell or setup:
                    cmd = cell_cmd
                else:
                    cmd = CodeGetter.initialize(self.view, advance=False, cell=False).get_text()

                if cell_cmd.startswith('```{r'):
                    should_plot = '#noplot' not in cmd and (
                        (re.search(r'```{r,.*fig\.width', cmd) is not None) or 
                        (('plot' in cmd) and (re.search(r'^\s*fig\(', cmd, re.MULTILINE) is None))
                    )
                    if should_plot:
                        # save the figure using praams pulled from cell header
                        title, w, h = parse_chunk_header(cell_cmd)
                        cmd += 'fig("{}", {}, {})'.format(title, w, h)

                    if cmd.startswith('```{r'):  # remove header
                        cmd = cmd[re.search('}\n', cmd).end():]

                if advance:
                    if cell or setup:
                        self.view.window().run_command("jump_cell")
                    else:
                        CodeGetter.initialize(self.view, advance=True, cell=False).get_text()


            else:
                getter = CodeGetter.initialize(self.view, advance=advance, cell=cell, setup=setup)
                cmd = getter.get_text()

        cmd = cmd.strip()

        if is_rcall and not cmd.startswith('include('):
            prefix = '$'
            postfix = '\n\x7f'
            if '\n' in cmd:
                prefix += '{'
                postfix = '\n}' + postfix

        # if postfix:
        #     cmd = cmd.rstrip()
        # cmd = prefix + cmd + postfix
        # if prefix in ['?', ';']:
        #     sender.bracketed_paste_mode = False

        sublime.set_timeout_async(lambda: sender.send_text(cmd))


# historial reason
class SendReplCommand(SendCodeCommand):
    def run(self, *args, **kargs):
        super(SendReplCommand, self).run(*args, **kargs)


class SendCodeBuildCommand(sublime_plugin.WindowCommand):

    def run(self, cmd=None, prog=None):
        self.window.active_view().run_command(
            "send_code",
            {"cmd": cmd, "prog": prog}
        )
