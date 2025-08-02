# Copyright (c) 2025 Moony Fringers
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


from typing import override

from completion.completion_mng import AbstractCompletionMng
from config import ConfigMng


class CompletionDbMng(AbstractCompletionMng):

    COMMANDS_DB = ["sql-shell"]

    def __init__(self, cli_flags: dict[str, bool], configMng: ConfigMng):
        self.cli_flags = cli_flags
        self.configMng = configMng

    def is_command_chosen(self, args: list[str]) -> bool:
        """
        Checks if the second argument is a valid command
        for the chosen category.
        """
        if not args or len(args) < 1:
            return False
        command = args[0]
        return command in self.COMMANDS_DB

    @override
    def get_completions(self, args: list[str]) -> list[str]:
        if not self.is_command_chosen(args):
            return self.COMMANDS_DB

        command = args[0]
        match command:
            case "sql-shell":
                return self.get_sql_shell_completions(args[1:])
            case _:
                return []

    def is_svc_tag_chosen(self, args: list[str]) -> bool:
        if len(args) < 1:
            return False
        svc_tag = args[0]
        return svc_tag in self.get_svc_tags(args)

    def get_svc_tags(self, args: list[str]) -> list[str]:
        env = self.configMng.get_active_environment()
        if env:
            return self.configMng.get_service_tags(env)
        return []

    def get_sql_shell_completions(self, args: list[str]) -> list[str]:
        if not self.is_svc_tag_chosen(args):
            return self.get_svc_tags(args)
        return []
