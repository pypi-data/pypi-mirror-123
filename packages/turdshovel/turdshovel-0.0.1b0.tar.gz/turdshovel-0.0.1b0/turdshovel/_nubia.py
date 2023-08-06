from nubia.internal.commands.builtin import Exit
from nubia.internal.commands.help import HelpCommand


class _Exit(Exit):
    cmd = ["exit"]


class _Help(HelpCommand):
    cmds = {"help": HelpCommand.HELP}
