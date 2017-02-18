from pypsi.core import Command
from pypsi.shell import Shell
from pypsi.ansi import AnsiCodes
from pypsi import topics

from pypsi.commands.help import HelpCommand, Topic
from pypsi.os import find_bins_in_path
from pypsi.completers import path_completer
from pypsi.plugins.cmd import CmdPlugin
from pypsi.plugins.multiline import MultilinePlugin



class Cesar(Command):

    def __init__(self, name='cesar', **kwargs):
          super(Cesar, self).__init__( name=name, **kwargs)


    def run(self, shell, args):
        cmd = CesarShell(shell)
        rc = cmd.cmdloop()




class CesarShell(Shell):
    help_cmd = HelpCommand()
    ml_plugin = MultilinePlugin()
    cmd_plugin = CmdPlugin(cmd_args=1)

    # Variable local pour ce shell
    fichier = ""

    def __init__(self, shell):
        super(CesarShell, self).__init__()
        for key in shell.commands:
            if "pypsi" in str(type(shell.commands.get(key))):
                self.register(shell.commands.get(key))
        self.prompt = "{cyan}Dcrypt_toolbox{r}{green}/Cesar >{r} ".format(
            gray=AnsiCodes.gray.prompt(), r=AnsiCodes.reset.prompt(),
            cyan=AnsiCodes.cyan.prompt(), green=AnsiCodes.green.prompt()
        )
        self.help_cmd.add_topic(self, Topic("shell", "Builtin Shell Commands"))
        self.help_cmd.add_topic(self, topics.IoRedirection)
        self._sys_bins = None

    def get_command_name_completions(self, prefix):
        if not self._sys_bins:
            self._sys_bins = find_bins_in_path()

        return sorted(
            [name for name in self.commands if name.startswith(prefix)] +
            [name for name in self._sys_bins if name.startswith(prefix)]
        )

    def do_go(self, args):
        '''
        Run Cesar algorithme
        '''
        print("do_cmdout(", args, ")")
        return 0

    def do_file(self, args):
        '''
        Change the file
        '''
        fichier = args
