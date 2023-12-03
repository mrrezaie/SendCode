import sublime
import re
import time

from ..settings import Settings
# from .terminal import send_to_terminal
# from .iterm import send_to_iterm
# from .r import send_to_r
# from .rstudio import send_to_rstudio
# from .conemu import send_to_conemu, send_to_cmder
# from .linux import send_to_linux_terminal
# from .tmux import send_to_tmux
# from .screen import send_to_screen
# from .chrome import send_to_chrome_jupyter, send_to_chrome_rstudio
# from .safari import send_to_safari_jupyter, send_to_safari_rstudio
# from .sublimerepl import send_to_sublimerepl
# from .terminalview import send_to_terminalview
from .terminus import send_to_terminus
from .clipboard import clipboard

class CodeSender:

    def __init__(self, view, cmd=None, prog=None, from_view=True):
        self.view = view
        self.settings = Settings(view)
        if prog:
            self.prog = prog
        else:
            self.prog = self.settings.get("prog")
        self.from_view = from_view
        self.bracketed_paste_mode = self.settings.get("bracketed_paste_mode")

    @classmethod
    def initialize(cls, view, **kwargs):
        syntax = Settings(view).syntax()
        if syntax == "r" or syntax == "rmd" or syntax == "rnw":
            return RCodeSender(view, **kwargs)
        elif syntax == "python":
            return PythonCodeSender(view, **kwargs)
        elif syntax == "julia":
            return JuliaCodeSender(view, **kwargs)
        else:
            return CodeSender(view, **kwargs)

    # def send_to_iterm(self, cmd, prefix="", postfix=""):
    #     if len(re.findall("\n", cmd)) > 0:
    #         cmd = "\x1b[200~" + cmd + "\x1b[201~"
    #     cmd = prefix + cmd + postfix

    #     self.view.window().run_command("term_send_text",
    #         {"text": cmd, "end": "" if postfix else "\n"})

    def send_text(self, cmd, prefix="", postfix=""):
        cmd = cmd.rstrip()
        cmd = cmd.expandtabs(self.view.settings().get("tab_size", 4))
        self.send_to_iterm(cmd, prefix, postfix)


class RCodeSender(CodeSender):
    pass

#     def send_text(self, cmd):
#         cmd = cmd.rstrip()
#         cmd = cmd.expandtabs(self.view.settings().get("tab_size", 4))
#         prog = self.prog.lower()
#         if prog == "r":
#             self.send_to_r(cmd)
#         elif prog == "chrome-rstudio":
#             self.send_to_chrome_rstudio(cmd)
#         elif prog == "safari-rstudio":
#             self.send_to_safari_rstudio(cmd)
#         else:
#             super(RCodeSender, self).send_text(cmd)

#     def send_to_r(self, cmd):
#         send_to_r(cmd)

#     def send_to_chrome_rstudio(self, cmd):
#         send_to_chrome_rstudio(cmd)

#     def send_to_safari_rstudio(self, cmd):
#         send_to_safari_rstudio(cmd)


class PythonCodeSender(CodeSender):

    # def send_to_terminal(self, cmd):
    #     if len(re.findall("\n", cmd)) > 0:
    #         if self.bracketed_paste_mode:
    #             send_to_terminal(cmd, bracketed=True)
    #             time.sleep(0.01)
    #             send_to_terminal("\x1B", bracketed=False)
    #         else:
    #             send_to_terminal(r"%cpaste -q")
    #             send_to_terminal(cmd)
    #             send_to_terminal("--")
    #     else:
    #         send_to_terminal(cmd)

    # def send_to_iterm(self, cmd, prefix="", postfix=""):
    #     if len(re.findall("\n", cmd)) > 0:
    #         cmd += '\n'
    #     super().send_to_iterm(cmd, prefix, postfix)


    # def send_to_iterm(self, cmd):
    #     if len(re.findall("\n", cmd)) > 0:
    #         cmd = "\x1b[200~" + cmd + "\n\x1b[201~"
    #     self.view.window().run_command("term_send_text", {"text": cmd})
    # def send_to_iterm(self, cmd):
    #     if len(re.findall("\n", cmd)) > 0:
    #         if self.bracketed_paste_mode:
    #             send_to_iterm(cmd, bracketed=True, commit=False)
    #             time.sleep(0.01)
    #             send_to_iterm("\x1B", bracketed=False)
    #         else:
    #             send_to_iterm(r"%cpaste -q")
    #             send_to_iterm(cmd)
    #             send_to_iterm("--")
    #     else:
    #         send_to_iterm(cmd)

    # def send_to_conemu(self, cmd):
    #     conemuc = self.settings.get("conemuc")
    #     if len(re.findall("\n", cmd)) > 0:
    #         if self.bracketed_paste_mode:
    #             send_to_conemu(cmd, conemuc, bracketed=False, commit=False)
    #             time.sleep(0.05)
    #             send_to_conemu("\x1B", conemuc, bracketed=False)
    #         else:
    #             send_to_conemu(r"%cpaste -q", conemuc)
    #             send_to_conemu(cmd, conemuc)
    #             send_to_conemu("--", conemuc)
    #     else:
    #         send_to_conemu(cmd, conemuc)

    # def send_to_cmder(self, cmd):
    #     conemuc = self.settings.get("conemuc")
    #     if len(re.findall("\n", cmd)) > 0:
    #         if self.bracketed_paste_mode:
    #             send_to_cmder(cmd, conemuc, bracketed=False, commit=False)
    #             time.sleep(0.05)
    #             send_to_cmder("\x1B", conemuc, bracketed=False)
    #         else:
    #             send_to_cmder(r"%cpaste -q", conemuc)
    #             send_to_cmder(cmd, conemuc)
    #             send_to_cmder("--", conemuc)
    #     else:
    #         send_to_cmder(cmd, conemuc)

    # def send_to_linux_terminal(self, cmd):
    #     linux_terminal = self.settings.get("linux_terminal")

    #     if len(re.findall("\n", cmd)) > 0:
    #         if self.bracketed_paste_mode:
    #             send_to_linux_terminal(linux_terminal, [cmd, ""])
    #         else:
    #             send_to_linux_terminal(linux_terminal, [r"%cpaste -q", cmd, "--"])
    #     else:
    #         send_to_linux_terminal(linux_terminal, cmd)

    # def send_to_tmux(self, cmd):
    #     tmux = self.settings.get("tmux", "tmux")
    #     if len(re.findall("\n", cmd)) > 0:
    #         if self.bracketed_paste_mode:
    #             send_to_tmux(cmd, tmux, bracketed=True, commit=False)
    #             time.sleep(0.01)
    #             send_to_tmux("\x1B", tmux, bracketed=False)
    #         else:
    #             send_to_tmux(r"%cpaste -q", tmux)
    #             send_to_tmux(cmd, tmux)
    #             # send ctrl-D instead of "--" since `set-buffer` does not work properly
    #             send_to_tmux("\x04", tmux)
    #     else:
    #         send_to_tmux(cmd, tmux)

    # def send_to_screen(self, cmd):
    #     screen = self.settings.get("screen", "screen")
    #     if len(re.findall("\n", cmd)) > 0:
    #         if self.bracketed_paste_mode:
    #             send_to_screen(cmd, screen, bracketed=True, commit=False)
    #             time.sleep(0.01)
    #             send_to_screen("\x1B", screen, bracketed=False)
    #         else:
    #             send_to_screen(r"%cpaste -q", screen)
    #             send_to_screen(cmd, screen)
    #             send_to_screen("--", screen)
    #     else:
    #         send_to_screen(cmd, screen)

    # def send_to_terminalview(self, cmd):
    #     if len(re.findall("\n", cmd)) > 0:
    #         if self.bracketed_paste_mode:
    #             send_to_terminalview(cmd, bracketed=True)
    #             time.sleep(0.05)
    #             send_to_terminalview("\x1B", bracketed=False)
    #         else:
    #             send_to_terminalview(r"%cpaste -q")
    #             send_to_terminalview(cmd)
    #             send_to_terminalview("--")
    #     else:
    #         send_to_terminalview(cmd)

    # def send_to_terminus(self, cmd):
    #     if len(re.findall("\n", cmd)) > 0:
    #         if self.bracketed_paste_mode:
    #             if sublime.platform() == "windows":
    #                 send_to_terminus(cmd, bracketed=False, commit=False)
    #                 time.sleep(0.05)
    #                 send_to_terminus("\x1B", bracketed=False)
    #             else:
    #                 send_to_terminus(cmd, bracketed=True, commit=False)
    #                 time.sleep(0.05)
    #                 send_to_terminus("\x1B", bracketed=False)
    #         else:
    #             send_to_terminus(r"%cpaste -q")
    #             send_to_terminus(cmd)
    #             send_to_terminus("--")
    #     else:
    #         if sublime.platform() == "windows":
    #             send_to_terminus(cmd, bracketed=False, commit=False)
    #             time.sleep(0.05)
    #             send_to_terminus("\r", bracketed=False)
    #         else:
    #             send_to_terminus(cmd, bracketed=False)

    def paste_to_console(self):
        value = self.settings.get("paste_to_console", None)
        if value is None:
            value = self.settings.get("ctrl+v_to_console", None)
        return value

    def send_to_terminus(self, cmd):
        if sublime.platform() == "windows" and self.paste_to_console:
            clipboard.set_clipboard(cmd)
            # send ctrl+v
            send_to_terminus("\x16", bracketed=False, commit=False)
            time.sleep(0.05)
            send_to_terminus("\x1b", bracketed=False, commit=False)
            time.sleep(0.2)
            send_to_terminus("\r", bracketed=False, commit=False)
            clipboard.reset_clipboard()
        else:
            if len(re.findall("\n", cmd)) > 0:
                if self.bracketed_paste_mode:
                    send_to_terminus(cmd, bracketed=True, commit=False)
                    send_to_terminus("\x1b", bracketed=False)
                else:
                    send_to_terminus(r"%cpaste -q")
                    send_to_terminus(cmd)
                    send_to_terminus("--")
            else:
                send_to_terminus(cmd, bracketed=False)


class JuliaCodeSender(CodeSender):

    pass
