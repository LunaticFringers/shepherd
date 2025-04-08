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


from __future__ import annotations

from typing import override

from config import ConfigMng
from environment import Environment
from util import Constants


class DockerComposeEnv(Environment):

    def __init__(self, config: ConfigMng, db_type: str, env_tag: str):
        """Initialize a Docker Compose environment."""
        super().__init__(
            config, Constants.ENV_TYPE_DOCKER_COMPOSE, db_type, env_tag
        )

    @override
    def clone(self, dst_env_tag: str) -> DockerComposeEnv:
        """Clone an environment."""
        return DockerComposeEnv(self.config, self.db_type, dst_env_tag)

    @override
    def start(self):
        """Start an environment."""
        pass

    @override
    def halt(self):
        """Halt an environment."""
        pass

    @override
    def reload(self):
        """Reload an environment."""
        pass

    @override
    def status(self):
        """Get environment status."""
        pass
