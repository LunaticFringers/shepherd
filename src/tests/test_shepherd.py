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
from pathlib import Path

import pytest
from click.testing import CliRunner
from pytest_mock import MockerFixture

from shpdctl import ShepherdMng

values = """
  # Oracle (ora) Configuration
  ora_image=ghcr.io/lunaticfringers/shepherd/oracle:19.3.0.0_TZ40
  ora_empty_env=fresh-ora-19300
  ora_pump_dir=PUMP_DIR
  ora_root_db_name=ORCLCDB
  ora_plug_db_name=ORCLPDB1
  ora_listener_port=1521

  # PostgreSQL (pg) Configuration
  pg_image=ghcr.io/lunaticfringers/shepherd/postgres:17-3.5
  pg_empty_env=fresh-pg-1735
  pg_listener_port=5432

  # SHPD Registry Configuration
  shpd_registry=ftp.example.com
  shpd_registry_ftp_usr=
  shpd_registry_ftp_psw=
  shpd_registry_ftp_shpd_path=shpd
  shpd_registry_ftp_imgs_path=imgs

  # Host and Domain Configuration
  host_inet_ip=127.0.0.1
  domain=sslip.io
  dns_type=autoresolving

  # Certificate Authority (CA) Configuration
  ca_country=IT
  ca_state=MS
  ca_locality=Carrara
  ca_org=LunaticFringe
  ca_org_unit=Development
  ca_cn=sslip.io
  ca_email=lf@sslip.io
  ca_passphrase=test

  # Certificate Configuration
  cert_country=IT
  cert_state=MS
  cert_locality=Carrara
  cert_org=LunaticFringe
  cert_org_unit=Development
  cert_cn=sslip.io
  cert_email=lf@sslip.io
  cert_subject_alternative_names=

  shpd_dir=~/.shpd

  # Database Default Configuration
  db_sys_usr=sys
  db_sys_psw=sys
  db_usr=docker
  db_psw=docker
  """


@pytest.fixture
def temp_home(tmp_path: Path) -> Path:
    """Fixture to create a temporary home directory and .shpd.conf file."""
    temp_home = tmp_path / "home"
    temp_home.mkdir()

    config_file = temp_home / ".shpd.conf"
    config_file.write_text(values)

    return temp_home


@pytest.fixture
def shepherd(temp_home: Path, mocker: MockerFixture) -> ShepherdMng:

    # ~ -> temp_home
    mocker.patch(
        "os.path.expanduser",
        return_value=str(os.path.join((temp_home), ".shpd.conf")),
    )

    return ShepherdMng()


def test_shepherdmng_creates_dirs(temp_home: Path, mocker: MockerFixture):
    """Test that ShepherdMng creates the required directories."""

    # ~ -> temp_home
    mocker.patch(
        "os.path.expanduser",
        return_value=str(os.path.join((temp_home), ".shpd.conf")),
    )

    sm = ShepherdMng()

    expected_dirs = [
        sm.configMng.constants.SHPD_ENVS_DIR,
        sm.configMng.constants.SHPD_ENV_IMGS_DIR,
        sm.configMng.constants.SHPD_CERTS_DIR,
        sm.configMng.constants.SHPD_SSH_DIR,
        sm.configMng.constants.SHPD_SSHD_DIR,
    ]

    for directory in expected_dirs:
        assert os.path.isdir(
            directory
        ), f"Directory {directory} was not created."

    shpd_config_file = sm.configMng.constants.SHPD_CONFIG_FILE
    assert os.path.isfile(
        shpd_config_file
    ), f"Config file {shpd_config_file} does not exist or is not a file."


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def test_create_cli(shepherd: ShepherdMng, runner: CliRunner):
    cli = shepherd.create_cli()

    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Shepherd CLI" in result.output
    assert "db" in result.output
    assert "env" in result.output
    assert "svc" in result.output

    result = runner.invoke(cli, ["-v", "--help"])


def test_create_env_commands(shepherd: ShepherdMng, runner: CliRunner):
    env_commands = shepherd.create_env_commands()

    result = runner.invoke(env_commands, ["--help"])
    assert result.exit_code == 0
    assert "Environment related operations" in result.output

    assert "init" in result.output
    assert "clone" in result.output
    assert "checkout" in result.output
    assert "noactive" in result.output
    assert "list" in result.output
    assert "up" in result.output
    assert "halt" in result.output
    assert "reload" in result.output
    assert "status" in result.output


def test_create_svc_commands(shepherd: ShepherdMng, runner: CliRunner):
    svc_commands = shepherd.create_svc_commands()

    result = runner.invoke(svc_commands, ["--help"])
    assert result.exit_code == 0
    assert "Service related operations" in result.output

    assert "build" in result.output
    assert "bootstrap" in result.output
    assert "up" in result.output
    assert "halt" in result.output
    assert "reload" in result.output
    assert "stdout" in result.output
    assert "shell" in result.output
