#!/usr/bin/env python3

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

import os
import sys
import subprocess
from pathlib import Path

# Color constants (ANSI color codes)
RED = '\033[0;31m'
NC = '\033[0m'  # No Color
YELLOW = '\033[0;33m'
GREEN = '\033[0;32m'
BLUE = '\033[0;36m'


def print_color(message, color=NC):
    """Print a message with color."""
    print(f"{color}{message}{NC}")


def is_root():
    """Check if the script is running with root privileges."""
    return os.geteuid() == 0


def run_command(cmd, check=True, shell=False, capture_output=False):
    """Run a shell command and return the result.
    
    Args:
        cmd: Command to run (list or string)
        check: Whether to raise an exception on failure
        shell: Whether to run through shell
        capture_output: Whether to capture stdout/stderr
    
    Returns:
        CompletedProcess instance
    """
    if isinstance(cmd, str) and not shell:
        cmd = cmd.split()
    
    try:
        result = subprocess.run(
            cmd, 
            check=check, 
            shell=shell,
            text=True,
            capture_output=capture_output
        )
        return result
    except subprocess.CalledProcessError as e:
        print_color(f"Command failed: {e}", RED)
        if check:
            sys.exit(1)
        return e


def get_current_user():
    """Get the actual user, even when running with sudo."""
    return os.environ.get("SUDO_USER", os.getlogin())


def check_file_exists(path):
    """Check if a file exists and is accessible."""
    return os.path.isfile(path) and os.access(path, os.R_OK)


def check_package_installed(pkg_name):
    """Check if a Debian package is installed."""
    try:
        result = run_command(["dpkg", "-s", pkg_name], check=False, capture_output=True)
        return result.returncode == 0
    except Exception:
        return False


def get_os_info():
    """Get OS information from /etc/os-release."""
    os_info = {}
    if os.path.exists("/etc/os-release"):
        with open("/etc/os-release", "r") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    os_info[key] = value.strip('"')
    return os_info