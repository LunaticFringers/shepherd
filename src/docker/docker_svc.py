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

from config import ConfigMng, ServiceCfg
from service import Service


class DockerSvc(Service):

    def __init__(self, config: ConfigMng, svcCfg: ServiceCfg):
        """Initialize a Docker service."""
        super().__init__(config, svcCfg)

    @override
    def clone(self, dst_svc_tag: str) -> DockerSvc:
        """Clone a service."""
        clonedCfg = ServiceCfg.from_other(self.to_config())
        clonedCfg.tag = dst_svc_tag
        clonedSvc = DockerSvc(
            self.configMng,
            clonedCfg,
        )
        return clonedSvc

    @override
    def build(self):
        """Build the service."""
        pass

    @override
    def bootstrap(self):
        """Bootstrap the service."""
        pass

    @override
    def start(self):
        """Start the service."""
        pass

    @override
    def halt(self):
        """Stop the service."""
        pass

    @override
    def reload(self):
        """Reload the service."""
        pass

    @override
    def show_stdout(self):
        """Show the service stdout."""
        pass

    @override
    def get_shell(self):
        """Get a shell session for the service."""
        pass
