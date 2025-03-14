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

import click

from database import DatabaseMng
from environment import EnvironmentMng
from service import ServiceMng

# Initialize instances
databaseMng = DatabaseMng()
environmentMng = EnvironmentMng()
serviceMng = ServiceMng()


@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose mode.")
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
    "-p", "--porcelain", is_flag=True, help="Produce machine-readable output."
)
@click.option("-k", "--keep", is_flag=True, help="Keep instead of drop.")
@click.option(
    "-r", "--replace", is_flag=True, help="Replace when already there."
)
@click.option(
    "-c",
    "--checkout",
    is_flag=True,
    help="Contextually checkout the environment.",
)
@click.option("-H", "--network-host", is_flag=True, help="Use host's network.")
@click.option(
    "-n", "--no-gen-certs", is_flag=True, help="Do not generate certificates."
)
def cli(
    verbose: bool,
    brief: bool,
    yes: bool,
    all: bool,
    follow: bool,
    porcelain: bool,
    keep: bool,
    replace: bool,
    checkout: bool,
    network_host: bool,
    no_gen_certs: bool,
):
    """Shepherd CLI:
    A tool to manage your environment, services, and database.
    """
    pass


@click.group()
def db():
    """Database related operations."""
    pass


@db.command(name="build")
def build_dbms():
    """Build dbms image."""
    databaseMng.build_dbms_image()


@db.command(name="bootstrap")
def bootstrap():
    """Bootstrap dbms service."""
    databaseMng.bootstrap_dbms_service()


@db.command(name="start")
def up():
    """Start dbms service."""
    databaseMng.start_dbms_service()


@db.command(name="halt")
def halt():
    """Halt dbms service."""
    databaseMng.halt_dbms_service()


@db.command(name="stdout")
def stdout():
    """Show dbms service stdout."""
    databaseMng.show_dbms_stdout()


@db.command(name="shell")
def shell():
    """Get a shell session for the dbms service."""
    databaseMng.get_dbms_shell_session()


@db.command(name="sql")
def sql_shell():
    """Get a SQL session for the dbms service."""
    databaseMng.get_sql_shell_session()


# Environment commands
@click.group()
def env():
    """Environment related operations."""
    pass


@env.command(name="init")
@click.argument("db_type")
@click.argument("env_tag")
def init_environment(db_type: str, env_tag: str):
    """Init an environment with a dbms type and an environment's tag name."""
    environmentMng.init_environment(db_type, env_tag)


@env.command(name="clone")
@click.argument("src_env_tag")
@click.argument("dst_env_tag")
def clone_environment(src_env_tag: str, dst_env_tag: str):
    """Clone an environment."""
    environmentMng.clone_environment(src_env_tag, dst_env_tag)


@env.command(name="checkout")
@click.argument("env_tag")
def checkout_environment(env_tag: str):
    """Checkout an environment."""
    environmentMng.checkout_environment(env_tag)


@env.command(name="noactive")
def set_noactive():
    """Set all environments as non-active."""
    environmentMng.set_all_non_active()


@env.command(name="list")
def list_environments():
    """List all available environments."""
    environmentMng.list_environments()


@env.command(name="start")
def start_environment():
    """Start environment."""
    environmentMng.start_environment()


@env.command(name="halt")
def halt_environment():
    """Halt environment."""
    environmentMng.halt_environment()


@env.command(name="reload")
def reload_environment():
    """Reload environment."""
    environmentMng.reload_environment()


@env.command(name="status")
def environment_status():
    """Print environment's status."""
    environmentMng.environment_status()


@click.group()
def svc():
    """Service related operations."""
    pass


@svc.command(name="build")
@click.argument("service_type", type=str)
def build_service(service_type: str):
    """Build service image."""
    serviceMng.build_service_image(service_type)


@svc.command(name="bootstrap")
@click.argument("service_type", type=str)
def bootstrap_service(service_type: str):
    """Bootstrap service."""
    serviceMng.bootstrap_service(service_type)


@svc.command(name="start")
@click.argument("service_type", type=str)
def start_service(service_type: str):
    """Start service."""
    serviceMng.start_service(service_type)


@svc.command(name="halt")
@click.argument("service_type", type=str)
def stop_service(service_type: str):
    """Stop service."""
    serviceMng.stop_service(service_type)


@svc.command(name="reload")
@click.argument("service_type", type=str)
def reload_service(service_type: str):
    """Reload service."""
    serviceMng.reload_service(service_type)


@svc.command(name="stdout")
@click.argument("service_id", type=str)
def service_stdout(service_id: str):
    """Show service stdout."""
    serviceMng.show_service_stdout(service_id)


@svc.command(name="shell")
@click.argument("service_id", type=str)
def service_shell(service_id: str):
    """Get a shell session for the service."""
    serviceMng.get_service_shell(service_id)


if __name__ == "__main__":
    cli()
