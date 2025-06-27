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
from typing import Dict, Optional

from config import ConfigMng, ServiceCfg


class Service(ABC):

    type: str
    tag: str
    image: str
    ingress: bool
    empty_env: str
    envvars: Dict[str, str]
    ports: Dict[str, str]
    properties: Dict[str, str]
    subject_alternative_name: Optional[str]

    def __init__(self, configMng: ConfigMng, svcCfg: ServiceCfg):
        self.configMng = configMng
        self.type = svcCfg.type
        self.tag = svcCfg.tag
        self.image = svcCfg.image
        self.ingress = svcCfg.ingress if svcCfg.ingress else False
        self.empty_env = svcCfg.empty_env if svcCfg.empty_env else ""
        self.envvars = svcCfg.envvars if svcCfg.envvars else {}
        self.ports = svcCfg.ports if svcCfg.ports else {}
        self.properties = svcCfg.properties if svcCfg.properties else {}
        self.subject_alternative_name = svcCfg.subject_alternative_name

    @abstractmethod
    def clone(self, dst_svc_tag: str) -> Service:
        """Clone a service."""
        pass

    @abstractmethod
    def build(self):
        """Build the service."""
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

    def to_config(self) -> ServiceCfg:
        return ServiceCfg(
            type=self.type,
            tag=self.tag,
            image=self.image,
            ingress=self.ingress,
            empty_env=self.empty_env,
            envvars=self.envvars,
            ports=self.ports,
            properties=self.properties,
            subject_alternative_name=self.subject_alternative_name,
        )


class ServiceFactory(ABC):
    """
    Factory class for services.
    """

    def __init__(self, config: ConfigMng):
        self.config = config

    @abstractmethod
    def new_service(self, svc_type: str, svc_tag: str) -> Service:
        """
        Create a new service.
        """
        pass

    @abstractmethod
    def new_service_cfg(self, svcCfg: ServiceCfg) -> Service:
        """
        Create a new service.
        """
        pass


class ServiceMng:

    def __init__(self, cli_flags: Dict[str, bool], configMng: ConfigMng):
        self.cli_flags = cli_flags
        self.configMng = configMng
        pass

    def build_image_svc(self, service_type: str):
        pass

    def bootstrap_svc(self, service_type: str):
        """Bootstrap a service."""
        pass

    def start_svc(self, service_type: str):
        """Start a service."""
        pass

    def halt_svc(self, service_type: str):
        """Halt a service."""
        pass

    def reload_svc(self, service_type: str):
        """Reload a service."""
        pass

    def stdout_svc(self, service_id: str):
        """Get service stdout."""
        pass

    def shell_svc(self, service_id: str):
        """Get a shell session for a service."""
        pass
