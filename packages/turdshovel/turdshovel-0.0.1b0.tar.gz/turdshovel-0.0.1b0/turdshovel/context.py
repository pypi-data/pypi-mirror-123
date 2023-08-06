import os
from typing import Any, List, Tuple
from copy import copy
from nubia import context, eventbus
from pygments.token import Token, Name
from rich.console import Console
from rich.text import Text
from rich import inspect
from .constants import TITLE_ASCII
from ._nubia import _Exit, _Help


class TurdshovelContext(context.Context):
    """Context for the Turdshovel app. Only allows interactive mode"""

    def get_prompt_tokens(self) -> List[Tuple[Any, str]]:
        tokens = [
            (Token.NewLine, "\n"),
            (Token.Title, "Turdshovel"),
            (Token.Space, ""),
            (Token.Pound, "> "),
        ]
        if self.target_friendly_name:
            tokens.insert(3, (Name.Command, self.target_friendly_name))
            tokens.insert(3, (Token.At, "@"))

        return tokens

    def on_interactive(self, args):
        self.verbose = args.verbose
        self.console = Console(soft_wrap=True)

        # This will be whatever the DataTarget is connected to and the related runtime
        self.target = None
        self.target_friendly_name = ""
        self.runtime = None

        self.console.print(Text(TITLE_ASCII, style="bold #8B4513"))
        self.console.print(
            "[bold #8B4513]Dump objects from .NET dumps\nWritten by[/] [bold green]daddycocoaman[/]\n"
        )

        # Make copy of commands and remove the builtins from original list and completers
        for k, v in copy(self._registry._cmd_instance_map).items():
            if v.__module__.startswith("nubia.internal.commands"):
                self._registry._cmd_instance_map.pop(k)
                self._registry._completer.meta_dict.pop(k)
                self._registry._completer.words.remove(k)

        # Readd commands for exit and help with less aliases
        for cmd in [_Exit, _Help]:
            self._registry.register_command(cmd())

        self.registry.dispatch_message(eventbus.Message.CONNECTED)
