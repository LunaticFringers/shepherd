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

import os
from abc import ABC, abstractmethod
from typing import List

from config import ConfigMng, EnvironmentCfg
from service import Service
from util import Util


class Environment(ABC):

    type: str
    db_type: str
    tag: str
    archived: bool
    active: bool
    services: List[Service]

    def __init__(
        self, config: ConfigMng, type: str, db_type: str, env_tag: str
    ):
        self.config = config
        self.type = type
        self.db_type = db_type
        self.tag = env_tag
        self.archived = False
        self.active = False
        self.services = []

    @abstractmethod
    def clone(self, dst_env_tag: str) -> Environment:
        """Clone an environment."""
        pass

    @abstractmethod
    def start(self):
        """Start an environment."""
        pass

    @abstractmethod
    def halt(self):
        """Halt an environment."""
        pass

    @abstractmethod
    def reload(self):
        """Reload an environment."""
        pass

    @abstractmethod
    def status(self):
        """Get environment status."""
        pass

    def to_config(self) -> EnvironmentCfg:
        """To config"""
        return EnvironmentCfg(
            type=self.type,
            tag=self.tag,
            services=[service.to_config() for service in self.services],
            archived=self.archived,
            active=self.active,
        )

    def realize(self):
        """Realize the environment."""
        Util.create_dir(
            os.path.join(self.config.constants.SHPD_ENVS_DIR, self.tag),
            self.tag,
        )
        pass

    def get_tag(self) -> str:
        """Return the tag of the environment."""
        return self.tag

    def set_tag(self, tag: str):
        """Set the tag of the environment."""
        self.tag = tag

    def is_archived(self) -> bool:
        return self.archived

    def set_archived(self, archived: bool):
        self.archived = archived

    def is_active(self) -> bool:
        return self.active

    def set_active(self, active: bool):
        self.active = active

    def add_service(self, service: Service):
        """Add a service to the environment."""
        self.services.append(service)

    def remove_service(self, service: Service):
        """Remove a service from the environment."""
        self.services.remove(service)

    def get_services(self) -> List[Service]:
        """Return the list of services in the environment."""
        return self.services


class EnvironmentFactory(ABC):
    """
    Factory class for creating environments.
    """

    def __init__(self, config: ConfigMng):
        self.config = config

    @abstractmethod
    def create_environment(
        self, env_type: str, db_type: str, env_tag: str
    ) -> Environment:
        """
        Create an environment.
        """
        pass


class EnvironmentMng:

    def __init__(self, configMng: ConfigMng, envFactory: EnvironmentFactory):
        self.configMng = configMng
        self.envFactory = envFactory

    def init_env(self, env_type: str, db_type: str, env_tag: str):
        """Initialize an environment."""
        env = self.envFactory.create_environment(env_type, db_type, env_tag)
        self.configMng.add_environment(env.to_config())
        env.realize()
        pass

    def clone_env(self, src_env_tag: str, dst_env_tag: str):
        """Clone an environment."""
        pass

    def checkout_env(self, env_tag: str):
        """Checkout an environment."""
        pass

    def set_all_envs_non_active(self):
        """Set all environments as non-active."""
        pass

    def list_envs(self):
        """List all available environments."""
        pass

    def start_env(self):
        """Start an environment."""
        pass

    def halt_env(self):
        """Halt an environment."""
        pass

    def reload_env(self):
        """Reload an environment."""
        pass

    def status_env(self):
        """Get environment status."""
        pass
