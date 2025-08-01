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

from typing import Any, override

import yaml

from config import ConfigMng, EnvironmentCfg
from environment import Environment
from service import ServiceFactory


class DockerComposeEnv(Environment):

    def __init__(
        self,
        config: ConfigMng,
        svcFactory: ServiceFactory,
        envCfg: EnvironmentCfg,
    ):
        """Initialize a Docker Compose environment."""
        super().__init__(config, svcFactory, envCfg)

    @override
    def clone(self, dst_env_tag: str) -> DockerComposeEnv:
        """Clone the environment."""
        clonedCfg = self.configMng.env_cfg_from_other(self.to_config())
        clonedCfg.tag = dst_env_tag
        clonedEnv = DockerComposeEnv(
            self.configMng,
            self.svcFactory,
            clonedCfg,
        )
        return clonedEnv

    @override
    def start(self):
        """Start the environment."""
        pass

    @override
    def halt(self):
        """Halt the environment."""
        pass

    @override
    def reload(self):
        """Reload the environment."""
        pass

    @override
    def render(self) -> str:
        """
        Render the full docker-compose YAML configuration for the environment.
        """

        compose_config: dict[str, Any] = {
            "services": {},
        }

        for svc in self.services:
            svc_yaml = yaml.safe_load(svc.render())
            compose_config["services"].update(svc_yaml["services"])

        return yaml.dump(compose_config, sort_keys=False)

    @override
    def status(self):
        """Get environment status."""
        pass
