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
import argparse
from pathlib import Path

# Import utility functions
from install_utils import (
    is_root, print_color, 
    RED, NC, YELLOW, GREEN, BLUE,
    run_command, get_current_user, check_file_exists,
    check_package_installed, get_os_info
)


# Configuration variables
script_dir = Path(__file__).parent.resolve()
py_src_dir = (script_dir.parent / "src").resolve()

# Get environment variables with defaults
install_shepctl_dir = os.environ.get("INSTALL_SHEPCTL_DIR", "/opt/shepctl")
install_shepctl_dir = Path(install_shepctl_dir).resolve()
symlink_dir = os.environ.get("SYMLINK_DIR", "/usr/local/bin")
symlink_dir = Path(symlink_dir)

version = os.environ.get("VER", "latest")
url = f"https://github.com/LunaticFringers/shepherd/releases/download/v{version}/shepctl-{version}.tar.gz"


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Shepherd Control Tool Installer",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        "-m", "--install-method",
        choices=["binary", "source"],
        default="binary",
        help="Specify the installation method (binary or source). Default is binary."
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose mode."
    )
    
    parser.add_argument(
        "-s", "--skip-deps",
        action="store_true",
        help="Skip ensuring dependencies."
    )
    
    parser.add_argument(
        "command",
        choices=["install", "uninstall"],
        help="Command to execute."
    )
    
    return parser.parse_args()


def install():
    """Install shepctl."""
    print_color("Installing shepctl...", BLUE)
    
    if not skip_ensure_deps:
        print_color("Ensuring dependencies...", BLUE)
        
        # Check if we're on a Debian-like system
        os_info = get_os_info()
        os_id = os_info.get("ID", "").lower()
        
        if os_id in ["ubuntu", "debian", "pop", "mint"]:
            # Will implement ensure_deps_debian_like() in the utility file
            print("Detected Debian-like system. Dependency checking not yet implemented.")
        else:
            print("Unrecognized or unsupported distro. Please ensure dependencies manually.")
    
    # Clean existing installation if it exists
    if install_shepctl_dir.exists():
        import shutil
        shutil.rmtree(install_shepctl_dir)
    os.makedirs(install_shepctl_dir, exist_ok=True)
    
    # Call appropriate installation function based on method
    if install_method == "binary":
        print("Binary installation method selected (not yet implemented)")
        # Will implement install_binary() later
    elif install_method == "source":
        print("Source installation method selected (not yet implemented)")
        # Will implement install_sources() later
    else:
        print(f"Error: Unknown install method '{install_method}'")
        sys.exit(1)


def uninstall():
    """Uninstall shepctl."""
    print_color("Uninstalling shepctl...", BLUE)
    
    # Remove installation directory
    if install_shepctl_dir.exists():
        import shutil
        shutil.rmtree(install_shepctl_dir)
        print(f"Removed {install_shepctl_dir}")
    
    # Remove symlink
    symlink_path = symlink_dir / "shepctl"
    if symlink_path.exists():
        symlink_path.unlink()
        print(f"Removed symlink {symlink_path}")
    
    print("shepctl uninstalled successfully")


def main():
    """Main function."""
    # Check if running as root
    if not is_root():
        print("This script requires privileges to install.")
        sys.exit(1)
    
    args = parse_arguments()
    
    # Store arguments for use in other functions
    global verbose, skip_ensure_deps, install_method
    verbose = args.verbose
    skip_ensure_deps = args.skip_deps
    install_method = args.install_method
    
    # Execute the requested command
    if args.command == "install":
        install()
    elif args.command == "uninstall":
        uninstall()
    else:
        print(f"Unknown command: {args.command}")
        sys.exit(1)


if __name__ == "__main__":
    # Global variables to store command line options
    verbose = False
    skip_ensure_deps = False
    install_method = "binary"
    
    # Run the main function
    main()