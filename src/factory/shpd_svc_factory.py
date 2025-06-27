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


from typing import override

from config import ConfigMng, ServiceCfg
from docker import DockerSvc
from service import Service, ServiceFactory
from util import Constants


class ShpdServiceFactory(ServiceFactory):

    def __init__(self, configMng: ConfigMng):
        self.configMng = configMng

    @override
    def new_service(self, svc_type: str, svc_tag: str) -> Service:
        """
        Create a service.
        """
        match svc_type:
            case Constants.SVC_TYPE_DOCKER:
                return DockerSvc(
                    self.configMng, ServiceCfg.from_tag(svc_type, svc_tag)
                )
            case _:
                raise ValueError(f"Unknown service type: {svc_type}")

    @override
    def new_service_cfg(self, svcCfg: ServiceCfg) -> Service:
        """
        Get a service.
        """
        match svcCfg.type:
            case Constants.SVC_TYPE_DOCKER:
                return DockerSvc(self.configMng, svcCfg)
            case _:
                raise ValueError(
                    f"""Unknown service type: {svcCfg.type},
                    plugins not supported yet!"""
                )
