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

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Constants:
    """Constants for the application."""

    SHPD_CONFIG_VALUES_FILE: str
    SHPD_DIR: str

    HOME_DIR: str = os.path.expanduser("~")

    @property
    def SHPD_CONFIG_FILE(self) -> str:
        return os.path.join(self.SHPD_DIR, ".shpd.json")

    @property
    def SHPD_ENVS_DIR(self) -> str:
        return os.path.join(self.SHPD_DIR, "envs")

    @property
    def SHPD_ENV_IMGS_DIR(self) -> str:
        return os.path.join(self.SHPD_DIR, ".env_imgs")

    @property
    def SHPD_CERTS_DIR(self) -> str:
        return os.path.join(self.SHPD_DIR, ".certs")

    @property
    def SHPD_SSH_DIR(self) -> str:
        return os.path.join(self.SHPD_DIR, ".ssh")

    @property
    def SHPD_SSHD_DIR(self) -> str:
        return os.path.join(self.SHPD_DIR, ".sshd")

    APP_NAME: str = "shpdctl"
    APP_VERSION: str = "0.0.0"
    APP_AUTHOR: str = "Lunatic Fringers"
    APP_LICENSE: str = "MIT"
    APP_URL: str = "https://github.com/LunaticFringers/shepherd"
