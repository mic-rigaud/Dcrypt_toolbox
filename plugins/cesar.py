from pypsi.core import Command
from pypsi.shell import Shell
from pypsi.ansi import AnsiCodes
from pypsi import topics

from pypsi.commands.help import HelpCommand, Topic
from pypsi.os import find_bins_in_path
from pypsi.completers import path_completer
from pypsi.plugins.cmd import CmdPlugin
from pypsi.plugins.multiline import MultilinePlugin



class Start(Command):

    def __init__(self, name='cesar', **kwargs):
          super(Start, self).__init__( name=name, **kwargs)


    def run(self, shell, args):
        cmd = CesarShell(shell)
        rc = cmd.cmdloop()




class CesarShell(Shell):
    help_cmd = HelpCommand()
    ml_plugin = MultilinePlugin()
    cmd_plugin = CmdPlugin(cmd_args=1)

    # Variable local pour ce shell
    file_in = ""
    offset = 0

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

    def do_go(self, args):
        '''
        Run Cesar algorithme
        '''
        try:
            file = open(self.file_in, "r")
            ciphered = file.readlines()
            if self.offset==0:
                for ind in range(1,26):
                    print(self.crack(ciphered,ind))
            else:
                print(self.crack(ciphered, self.offset))
            file.close()
        except:
            print("*** Bad file. Usage: FileIn <file>")


    def crack(self, ciphered, offset):
        line=""
        line += "########################## \n"
        line += "Resultat avec l'offset: " + str(offset)
        line += "\n##########################\n"
        for cipheredLine in ciphered:
            for cipheredWord in cipheredLine.replace('\n','').split():
                line += self.rot(cipheredWord, offset)
                line += " "
            line += "\n"
        return line

    def do_fileIn(self, args):
        '''
        Change the file input
        '''
        self.file_in = args

    def do_changeRotation(self,args):
        '''
        If you know the offset. (0 if you don't know)
        '''
        self.offset = args


    def rot(self, cipheredChain, rotation):
        result = ""
        for cipheredChar in cipheredChain:
            if ('a' <= cipheredChar) and (cipheredChar <= 'z'):
                result += chr((ord(cipheredChar) - ord('a') + rotation) % 26 + ord('a'))
            elif ('A' <= cipheredChar) and (cipheredChar <= 'Z'):
                result += chr((ord(cipheredChar) - ord('A') + rotation) % 26 + ord('A'))
            else:
                result += cipheredChar
        return result

    def get_command_name_completions(self, prefix):
        if not self._sys_bins:
            self._sys_bins = find_bins_in_path()

        return sorted(
            [name for name in self.commands if name.startswith(prefix)] +
            [name for name in self._sys_bins if name.startswith(prefix)]
        )
