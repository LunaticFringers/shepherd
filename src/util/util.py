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
import sys

from rich.console import Console

from .constants import Constants


class Util:
    console = Console()

    @staticmethod
    def create_dir(dir_path: str, desc: str):
        try:
            os.makedirs(dir_path, exist_ok=True)
        except OSError as e:
            Util.print_error_and_die(
                f"[{desc}] Failed to create directory: {dir_path}\nError: {e}"
            )

    @staticmethod
    def print_error_and_die(message: str):
        Util.console.print(
            f"[bold red]ERROR:[/bold red] {message}", style="bold red"
        )
        sys.exit(1)

    @staticmethod
    def ensure_dirs(constants: Constants):
        dirs = {
            "LO_ENVS_IMAGES_DIR": constants.SHPD_ENV_IMGS_DIR,
            "LO_ENVS_CERTS_DIR": constants.SHPD_CERTS_DIR,
            "LO_ENVS_SSH_DIR": constants.SHPD_SSH_DIR,
            "LO_ENVS_SSHD_DIR": constants.SHPD_SSHD_DIR,
        }

        for desc, dir_path in dirs.items():
            resolved_path = os.path.realpath(dir_path)
            if not os.path.exists(resolved_path) or not os.path.isdir(
                resolved_path
            ):
                Util.create_dir(resolved_path, desc)
