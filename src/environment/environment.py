# MIT License
#
# Copyright (c) 2025 Lunatic Fringers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
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
    def init_environment(self, db_type: str, env_tag: str):
        """Stub for initializing an environment."""
        pass

    def clone_environment(self, src_env_tag: str, dst_env_tag: str):
        """Stub for cloning an environment."""
        pass

    def checkout_environment(self, env_tag: str):
        """Stub for checking out an environment."""
        pass

    def set_all_non_active(self):
        """Stub for setting all environments as non-active."""
        pass

    def list_environments(self):
        """Stub for listing all available environments."""
        pass

    def start_environment(self):
        """Stub for starting an environment."""
        pass

    def halt_environment(self):
        """Stub for halting an environment."""
        pass

    def reload_environment(self):
        """Stub for reloading an environment."""
        pass

    def environment_status(self):
        """Stub for getting environment status."""
        pass
