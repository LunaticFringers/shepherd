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

from abc import ABC, abstractmethod


class Service(ABC):
    @abstractmethod
    def build_image(self):
        """Build the service image."""
        pass

    @abstractmethod
    def bootstrap(self):
        """Bootstrap the service."""
        pass

    @abstractmethod
    def start(self):
        """Start the service."""
        pass

    @abstractmethod
    def halt(self):
        """Stop the service."""
        pass

    @abstractmethod
    def reload(self):
        """Reload the service."""
        pass

    @abstractmethod
    def show_stdout(self):
        """Show the service stdout."""
        pass

    @abstractmethod
    def get_shell(self):
        """Get a shell session for the service."""
        pass


class ServiceMng:
    def build_image(self, service_type: str):
        pass

    def bootstrap(self, service_type: str):
        """Bootstrap a service."""
        pass

    def start(self, service_type: str):
        """Start a service."""
        pass

    def stop(self, service_type: str):
        """Stop a service."""
        pass

    def reload(self, service_type: str):
        """Reload a service."""
        pass

    def stdout(self, service_id: str):
        """Get service stdout."""
        pass

    def shell(self, service_id: str):
        """Get a shell session for a service."""
        pass
