# Copyright (c) 2025 Lunatic Fringers
#
# This file is part of Shepherd Core Stack
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from typing import Dict

from config import ConfigMng


class CompletionMng:

    CATEGORIES = ["db", "env", "svc"]
    COMMANDS_SVC = ["build", "bootstrap", "up", "halt", "stdout", "shell"]
    COMMANDS_DB = COMMANDS_SVC + ["sql-shell"]
    COMMANDS_ENV = [
        "init",
        "clone",
        "rename",
        "checkout",
        "delete",
        "list",
        "up",
        "halt",
        "reload",
        "status",
        "add-resource",
    ]

    def __init__(self, cli_flags: Dict[str, bool], configMng: ConfigMng):
        self.cli_flags = cli_flags
        self.configMng = configMng

    def is_category_chosen(self, args: list[str]) -> bool:
        """
        Checks if the first argument is a valid category.
        """
        if not args:
            return False
        return args[0] in self.CATEGORIES

    def get_commands_for_category(self, category: str) -> list[str]:
        if category == "db":
            return self.COMMANDS_DB
        elif category == "env":
            return self.COMMANDS_ENV
        elif category == "svc":
            return self.COMMANDS_SVC
        return []

    def is_command_chosen(self, args: list[str]) -> bool:
        """
        Checks if the second argument is a valid command
        for the chosen category.
        """
        if len(args) < 2:
            return False
        category = args[0]
        command = args[1]
        commands = self.get_commands_for_category(category)
        return command in commands

    def get_completions(self, args: list[str]) -> list[str]:
        """
        Returns a list of completions based on the provided arguments.
        """

        if not self.is_category_chosen(args):
            return self.CATEGORIES

        if not self.is_command_chosen(args):
            return self.get_commands_for_category(args[0])

        return []
