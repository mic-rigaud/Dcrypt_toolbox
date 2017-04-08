from pypsi.core import Command
from pypsi.shell import Shell
from pypsi.ansi import AnsiCodes
from pypsi import topics

from pypsi.commands.help import HelpCommand, Topic
from pypsi.os import find_bins_in_path
from pypsi.completers import path_completer
from pypsi.plugins.cmd import CmdPlugin
from pypsi.plugins.multiline import MultilinePlugin

##############################################################################################################
# TODO: Ajouter la possibilite de choisir le dictionnaire et l'alphabet
##############################################################################################################

class Start(Command):

    def __init__(self, name='vigenere', **kwargs):
          super(Start, self).__init__( name=name, **kwargs)


    def run(self, shell, args):
        cmd = VigenereShell(shell)
        rc = cmd.cmdloop()




class VigenereShell(Shell):
    help_cmd = HelpCommand()
    ml_plugin = MultilinePlugin()
    cmd_plugin = CmdPlugin(cmd_args=1)

    # Variable local pour ce shell
    file_in = ""
    key = ""
    know_key = False

    def __init__(self, shell):
        super(VigenereShell, self).__init__()
        for key in shell.commands:
            if "pypsi" in str(type(shell.commands.get(key))):
                self.register(shell.commands.get(key))
        self.prompt = "{cyan}Dcrypt_toolbox{r}{green}/Vigenere >{r} ".format(
            gray=AnsiCodes.gray.prompt(), r=AnsiCodes.reset.prompt(),
            cyan=AnsiCodes.cyan.prompt(), green=AnsiCodes.green.prompt()
        )
        self.help_cmd.add_topic(self, Topic("shell", "Builtin Shell Commands"))
        self.help_cmd.add_topic(self, topics.IoRedirection)
        self._sys_bins = None

    def do_go(self, args):
        '''
        Run Vigenere algorithme
        '''
        try:
            print(self.file_in)
            file = open(self.file_in, "r")
            ciphered = file.readlines()
            if self.know_key:
                self.decryptMessage(self.key, ciphered)
            else:
                self.crack(ciphered)
            file.close()
        except:
            print("*** Mauvais Fichier. Usage: setFileIn <file>")

    def do_rechercheFrequentiel(self, args):
        '''
        Lance une analyse fréquentielle.
        Suppose une clef qui est multiple du nombre de caractère
        '''
        try:
            print(self.file_in)
            file = open(self.file_in, "r")
            ciphered = file.readlines()
            if self.know_key:
                self.decryptMessage(self.key, ciphered)
            else:
                self.crack(ciphered)
            file.close()
        except:
            print("*** Mauvais Fichier. Usage: setFileIn <file>")

    def do_setFileIn(self, args):
        '''
        Change the file input
        '''
        self.file_in = args

    def do_setKey(self,args):
        '''
        If you know the key. (0 if you don't know)
        '''
        if args==0:
            self.know_key = False
        else:
            self.know_key = True
            self.key = args


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
##############################################################################################################
# MES FONCTIONS
##############################################################################################################

    def crack(self, ciphered):
        tailleClef = self.rechercheTailleKey(ciphered)


        # line=""
        # line += "########################## \n"
        # line += "Resultat avec l'offset: " + str(offset)
        # line += "\n##########################\n"
        # for cipheredLine in ciphered:
        #     for cipheredWord in cipheredLine.replace('\n','').split():
        #         line += self.rot(cipheredWord, offset)
        #         line += " "
        #     line += "\n"
        # return line

    def rechercheTailleKey(self, ciphered):
        texte = ""
        for cipheredLine in ciphered:
            texte = texte + cipheredLine
        texte = texte.replace("'",'')\
                        .replace(' ','')\
                        .replace('\n','')\
                        .replace('\r','')\
                        .replace('.','')
        tailleTexte = len(texte)
        tailleClef=[]
        line = "######################################## \n"
        line += "Les tailles de clefs possibles sont:\n"
        for i in range(1,tailleTexte+1):
            if tailleTexte % i ==0:
                line += str(i)+","
                tailleClef.append(i)
        line += "\n########################################\n"
        print(line)
        return tailleClef




    def decryptMessage(self, key, ciphered):
        print("decrypt!!!")
