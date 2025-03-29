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
from typing import Any

import click

from config import ConfigMng
from database import DatabaseMng
from environment import EnvironmentMng
from service import ServiceMng
from util import Util


class ShepherdMng:
    def __init__(self):
        self.configMng = ConfigMng(os.path.expanduser("~/.shpd.conf"))
        self.environmentMng = EnvironmentMng()
        self.serviceMng = ServiceMng()
        self.databaseMng = DatabaseMng()
        self.cli_flags = {}
        Util.ensure_dirs(self.configMng.constants)
        Util.ensure_config_file(self.configMng.constants)

    def create_cli(self):
        @click.group()
        @click.option(
            "-v", "--verbose", is_flag=True, help="Enable verbose mode."
        )
        @click.option("-b", "--brief", is_flag=True, help="Brief output.")
        @click.option(
            "-y",
            "--yes",
            is_flag=True,
            help="Automatic yes to prompts; run non-interactively.",
        )
        @click.option("-a", "--all", is_flag=True, help="Apply to all.")
        @click.option("-f", "--follow", is_flag=True, help="Follow log output.")
        @click.option(
            "-p",
            "--porcelain",
            is_flag=True,
            help="Produce machine-readable output.",
        )
        @click.option(
            "-k", "--keep", is_flag=True, help="Keep instead of drop."
        )
        @click.option(
            "-r", "--replace", is_flag=True, help="Replace when already there."
        )
        @click.option(
            "-c",
            "--checkout",
            is_flag=True,
            help="Contextually checkout the environment.",
        )
        @click.option(
            "-H", "--network-host", is_flag=True, help="Use host's network."
        )
        @click.option(
            "-n",
            "--no-gen-certs",
            is_flag=True,
            help="Do not generate certificates.",
        )
        def cli(**kwargs: dict[str, Any]):
            """Shepherd CLI:
            A tool to manage your environment, services, and database."""
            self.cli_flags = kwargs

        cli.add_command(self.create_db_commands(), "db")
        cli.add_command(self.create_env_commands(), "env")
        cli.add_command(self.create_svc_commands(), "svc")
        return cli

    def create_db_commands(self):
        @click.group()
        def db():
            """Database related operations."""
            pass

        @db.command(name="build")
        def build():  # pyright: ignore[reportUnusedFunction]
            """Build dbms image."""
            self.databaseMng.build_image()

        @db.command(name="bootstrap")
        def bootstrap():  # pyright: ignore[reportUnusedFunction]
            """Bootstrap dbms service."""
            self.databaseMng.bootstrap()

        @db.command(name="up")
        def start():  # pyright: ignore[reportUnusedFunction]
            """Start dbms service."""
            self.databaseMng.start()

        @db.command(name="halt")
        def halt():  # pyright: ignore[reportUnusedFunction]
            """Halt dbms service."""
            self.databaseMng.halt()

        @db.command(name="stdout")
        def stdout():  # pyright: ignore[reportUnusedFunction]
            """Show dbms service stdout."""
            self.databaseMng.stdout()

        @db.command(name="shell")
        def shell():  # pyright: ignore[reportUnusedFunction]
            """Get a shell session for the dbms service."""
            self.databaseMng.shell()

        @db.command(name="sql")
        def sql_shell():  # pyright: ignore[reportUnusedFunction]
            """Get a SQL session for the dbms service."""
            self.databaseMng.sql_shell()

        return db

    def create_env_commands(self):
        @click.group()
        def env():
            """Environment related operations."""
            pass

        @env.command(name="init")
        @click.argument("db_type")
        @click.argument("env_tag")
        def init(  # pyright: ignore[reportUnusedFunction]
            db_type: str, env_tag: str
        ):
            """Init an environment."""
            self.environmentMng.init(db_type, env_tag)

        @env.command(name="clone")
        @click.argument("src_env_tag")
        @click.argument("dst_env_tag")
        def clone(  # pyright: ignore[reportUnusedFunction]
            src_env_tag: str, dst_env_tag: str
        ):
            """Clone an environment."""
            self.environmentMng.clone(src_env_tag, dst_env_tag)

        @env.command(name="checkout")
        @click.argument("env_tag")
        def checkout(env_tag: str):  # pyright: ignore[reportUnusedFunction]
            """Checkout an environment."""
            self.environmentMng.checkout(env_tag)

        @env.command(name="noactive")
        def set():  # pyright: ignore[reportUnusedFunction]
            """Set all environments as non-active."""
            self.environmentMng.set_all_non_active()

        @env.command(name="list")
        def list():  # pyright: ignore[reportUnusedFunction]
            """List all available environments."""
            self.environmentMng.list()

        @env.command(name="up")
        def start():  # pyright: ignore[reportUnusedFunction]
            """Start environment."""
            self.environmentMng.start()

        @env.command(name="halt")
        def halt():  # pyright: ignore[reportUnusedFunction]
            """Halt environment."""
            self.environmentMng.halt()

        @env.command(name="reload")
        def reload():  # pyright: ignore[reportUnusedFunction]
            """Reload environment."""
            self.environmentMng.reload()

        @env.command(name="status")
        def status():  # pyright: ignore[reportUnusedFunction]
            """Print environment's status."""
            self.environmentMng.status()

        return env

    def create_svc_commands(self):
        @click.group()
        def svc():
            """Service related operations."""
            pass

        @svc.command(name="build")
        @click.argument("service_type", type=str)
        def build(service_type: str):  # pyright: ignore[reportUnusedFunction]
            """Build service image."""
            self.serviceMng.build_image(service_type)

        @svc.command(name="bootstrap")
        @click.argument("service_type", type=str)
        def bootstrap(  # pyright: ignore[reportUnusedFunction]
            service_type: str,
        ):
            """Bootstrap service."""
            self.serviceMng.bootstrap(service_type)

        @svc.command(name="up")
        @click.argument("service_type", type=str)
        def start(service_type: str):  # pyright: ignore[reportUnusedFunction]
            """Start service."""
            self.serviceMng.start(service_type)

        @svc.command(name="halt")
        @click.argument("service_type", type=str)
        def halt(service_type: str):  # pyright: ignore[reportUnusedFunction]
            """Stop service."""
            self.serviceMng.stop(service_type)

        @svc.command(name="reload")
        @click.argument("service_type", type=str)
        def reload(service_type: str):  # pyright: ignore[reportUnusedFunction]
            """Reload service."""
            self.serviceMng.reload(service_type)

        @svc.command(name="stdout")
        @click.argument("service_id", type=str)
        def stdout(service_id: str):  # pyright: ignore[reportUnusedFunction]
            """Show service stdout."""
            self.serviceMng.stdout(service_id)

        @svc.command(name="shell")
        @click.argument("service_id", type=str)
        def shell(service_id: str):  # pyright: ignore[reportUnusedFunction]
            """Get a shell session for the service."""
            self.serviceMng.shell(service_id)

        return svc


if __name__ == "__main__":
    shepherd = ShepherdMng()
    cli = shepherd.create_cli()
    cli()
