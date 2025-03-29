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

from abc import ABC, abstractmethod
from typing import List

from service import Service


class Environment(ABC):

    tag: str
    archived: bool
    active: bool
    services: List[Service]

    def __init__(self):
        self.services = []

    @abstractmethod
    def init(self, db_type: str, env_tag: str):
        """Initialize an environment."""
        pass

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


class EnvironmentMng:
    def init(self, db_type: str, env_tag: str):
        """Initialize an environment."""
        pass

    def clone(self, src_env_tag: str, dst_env_tag: str):
        """Clone an environment."""
        pass

    def checkout(self, env_tag: str):
        """Checkout an environment."""
        pass

    def set_all_non_active(self):
        """Set all environments as non-active."""
        pass

    def list(self):
        """List all available environments."""
        pass

    def start(self):
        """Start an environment."""
        pass

    def halt(self):
        """Halt an environment."""
        pass

    def reload(self):
        """Reload an environment."""
        pass

    def status(self):
        """Get environment status."""
        pass
