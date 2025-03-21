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

import copy
from abc import ABC
from typing import List

from service import Service


class Environment(ABC):

    tag: str
    archived: bool
    active: bool
    services: List[Service]

    def __init__(self):
        self.services = []

    def init(self, db_type: str, env_tag: str):
        """Initialize an environment."""
        pass

    def clone(self, dst_env_tag: str) -> Environment:
        """Clone an environment."""
        pass
        cloned_env = copy.deepcopy(self)
        cloned_env.tag = dst_env_tag
        return cloned_env

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
