#!/usr/bin/python3
# Copyright (c) 2015, Adam Meily <meily.adam@gmail.com>
# Pypsi - https://github.com/ameily/pypsi
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#


'''
This is an example Pypsi shell using several key features of the Pypsi API and
architecture. The code is provided as an example of the overarching Pypsi design
and API. The demo shell can be used as a skeleton for new shells and can be
easily modified.
'''

from pypsi.shell import Shell
from pypsi.core import Command
from pypsi.plugins.cmd import CmdPlugin
from pypsi.plugins.block import BlockPlugin
from pypsi.plugins.hexcode import HexCodePlugin
from pypsi.commands.macro import MacroCommand
from pypsi.commands.system import SystemCommand
from pypsi.plugins.multiline import MultilinePlugin
from pypsi.commands.xargs import XArgsCommand
from pypsi.commands.exit import ExitCommand
from pypsi.plugins.variable import VariablePlugin
from pypsi.plugins.history import HistoryPlugin
from pypsi.plugins.alias import AliasPlugin
from pypsi.commands.echo import EchoCommand
from pypsi.commands.include import IncludeCommand
from pypsi.commands.help import HelpCommand, Topic
from pypsi.commands.tip import TipCommand
from pypsi.commands.tail import TailCommand
from pypsi.commands.chdir import ChdirCommand
from pypsi.commands.pwd import PwdCommand
from pypsi.plugins.comment import CommentPlugin

from pypsi import wizard as wiz
from pypsi.format import Table, Column, title_str
from pypsi.completers import path_completer


from pypsi.ansi import AnsiCodes
from pypsi import topics

from pypsi.os import find_bins_in_path

import sys
from plugins import *


ShellTopic = """These commands are built into the Pypsi shell (all glory and honor to the pypsi shell).
This is a single newline

and This is a double"""


class DemoShell(Shell):
    '''
    Example demonstration shell.
    '''

    # First, add commands and plugins to the shell
    echo_cmd = EchoCommand()
    block_plugin = BlockPlugin()
    hexcode_plugin = HexCodePlugin()
    macro_cmd = MacroCommand()


    # Drop commands to cmd.exe if the platform is Windows
    ml_plugin = MultilinePlugin()
    exit_cmd = ExitCommand()
    history_plugin = HistoryPlugin()
    cmd_plugin = CmdPlugin(cmd_args=1)
    tail_cmd = TailCommand()
    help_cmd = HelpCommand()
    var_plugin = VariablePlugin(case_sensitive=False, env=False)
    comment_plugin = CommentPlugin()


    def __init__(self):
        # You must call the Shell.__init__() method.
        super(DemoShell, self).__init__()

        self.prompt = "{cyan}Dcrypt_toolbox{r} {green}>{r} ".format(
            gray=AnsiCodes.gray.prompt(), r=AnsiCodes.reset.prompt(),
            cyan=AnsiCodes.cyan.prompt(), green=AnsiCodes.green.prompt()
        )
        # self.fallback_cmd = self.system_cmd

        # Register the shell topic for the help command
        self.help_cmd.add_topic(self, Topic("shell", "Builtin Shell Commands"))
        # Add the I/O redirection topic
        self.help_cmd.add_topic(self, topics.IoRedirection)

        self._sys_bins = None
        plugin_cesar = cesar.Cesar()
        self.register(plugin_cesar)





    ############################################################################
    # This functions demonstrate that existing Python :mod:`cmd` shell commands
    # work without modification in Pypsi.
    ############################################################################
    def do_cmddoc(self, args):
        '''
        This is some long description for the cmdargs command.
        '''
        print("do_cmdargs(", args, ")")
        return 0

    def help_cmdout(self):
        print("this is the help message for the cmdout command")

    def do_cmdout(self, args):
        print(self.plugins)
        return 0

    def get_command_name_completions(self, prefix):
        if not self._sys_bins:
            self._sys_bins = find_bins_in_path()

        return sorted(
            [name for name in self.commands if name.startswith(prefix)] +
            [name for name in self._sys_bins if name.startswith(prefix)]
        )


if __name__ == '__main__':
    shell = DemoShell()
    rc = shell.cmdloop()
    sys.exit(rc)
