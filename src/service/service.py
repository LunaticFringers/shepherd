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
    def build_service_image(self, service_type: str):
        pass

    def bootstrap_service(self, service_type: str):
        """Stub for bootstrapping a service."""
        pass

    def start_service(self, service_type: str):
        """Stub for starting a service."""
        pass

    def stop_service(self, service_type: str):
        """Stub for stopping a service."""
        pass

    def reload_service(self, service_type: str):
        """Stub for reloading a service."""
        pass

    def show_service_stdout(self, service_id: str):
        """Stub for showing service stdout."""
        pass

    def get_service_shell(self, service_id: str):
        """Stub for getting a shell session for a service."""
        pass
