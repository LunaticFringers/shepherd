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
from pathlib import Path

import pytest
from click.testing import CliRunner
from pytest_mock import MockerFixture

from database import DatabaseMng
from environment import EnvironmentMng
from service import ServiceMng
from shpdctl import ShepherdMng, cli

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
def temp_home(tmp_path: Path, mocker: MockerFixture) -> Path:
    """Fixture to create a temporary home directory and .shpd.conf file."""
    temp_home = tmp_path / "home"
    temp_home.mkdir()

    config_file = temp_home / ".shpd.conf"
    config_file.write_text(values)

    mocker.patch(
        "os.path.expanduser",
        side_effect=[temp_home / ".shpd.conf", temp_home / ".shpd"],
    )

    return temp_home


def test_shepherdmng_creates_dirs(temp_home: Path):
    """Test that ShepherdMng creates the required directories."""

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


def test_cli_flags_no_flags(
    temp_home: Path, runner: CliRunner, mocker: MockerFixture
):
    mock_init = mocker.patch.object(ShepherdMng, "__init__", return_value=None)

    result = runner.invoke(cli, ["test"])

    assert result.exit_code == 0
    mock_init.assert_called_once_with(
        {
            "verbose": False,
            "yes": False,
            "all": False,
            "follow": False,
            "porcelain": False,
            "keep": False,
            "replace": False,
            "checkout": False,
        }
    )


def test_cli_flags_verbose(
    temp_home: Path, runner: CliRunner, mocker: MockerFixture
):
    mock_init = mocker.patch.object(ShepherdMng, "__init__", return_value=None)

    result = runner.invoke(cli, ["--verbose", "test"])

    flags = {
        "verbose": True,
        "yes": False,
        "all": False,
        "follow": False,
        "porcelain": False,
        "keep": False,
        "replace": False,
        "checkout": False,
    }

    assert result.exit_code == 0
    mock_init.assert_called_once_with(flags)

    result = runner.invoke(cli, ["-v", "test"])

    assert result.exit_code == 0
    mock_init.assert_called_with(flags)


def test_cli_flags_yes(
    temp_home: Path, runner: CliRunner, mocker: MockerFixture
):
    mock_init = mocker.patch.object(ShepherdMng, "__init__", return_value=None)

    result = runner.invoke(cli, ["--yes", "test"])

    flags = {
        "verbose": False,
        "yes": True,
        "all": False,
        "follow": False,
        "porcelain": False,
        "keep": False,
        "replace": False,
        "checkout": False,
    }

    assert result.exit_code == 0
    mock_init.assert_called_once_with(flags)

    result = runner.invoke(cli, ["-y", "test"])

    assert result.exit_code == 0
    mock_init.assert_called_with(flags)


def test_cli_flags_all(
    temp_home: Path, runner: CliRunner, mocker: MockerFixture
):
    mock_init = mocker.patch.object(ShepherdMng, "__init__", return_value=None)

    result = runner.invoke(cli, ["--all", "test"])

    flags = {
        "verbose": False,
        "yes": False,
        "all": True,
        "follow": False,
        "porcelain": False,
        "keep": False,
        "replace": False,
        "checkout": False,
    }

    assert result.exit_code == 0
    mock_init.assert_called_once_with(flags)

    result = runner.invoke(cli, ["-a", "test"])

    assert result.exit_code == 0
    mock_init.assert_called_with(flags)


def test_cli_flags_follow(
    temp_home: Path, runner: CliRunner, mocker: MockerFixture
):
    mock_init = mocker.patch.object(ShepherdMng, "__init__", return_value=None)

    result = runner.invoke(cli, ["--follow", "test"])

    flags = {
        "verbose": False,
        "yes": False,
        "all": False,
        "follow": True,
        "porcelain": False,
        "keep": False,
        "replace": False,
        "checkout": False,
    }

    assert result.exit_code == 0
    mock_init.assert_called_once_with(flags)

    result = runner.invoke(cli, ["-f", "test"])

    assert result.exit_code == 0
    mock_init.assert_called_with(flags)


def test_cli_flags_porcelain(
    temp_home: Path, runner: CliRunner, mocker: MockerFixture
):
    mock_init = mocker.patch.object(ShepherdMng, "__init__", return_value=None)

    result = runner.invoke(cli, ["--porcelain", "test"])

    flags = {
        "verbose": False,
        "yes": False,
        "all": False,
        "follow": False,
        "porcelain": True,
        "keep": False,
        "replace": False,
        "checkout": False,
    }

    assert result.exit_code == 0
    mock_init.assert_called_once_with(flags)

    result = runner.invoke(cli, ["-p", "test"])

    assert result.exit_code == 0
    mock_init.assert_called_with(flags)


def test_cli_flags_keep(
    temp_home: Path, runner: CliRunner, mocker: MockerFixture
):
    mock_init = mocker.patch.object(ShepherdMng, "__init__", return_value=None)

    result = runner.invoke(cli, ["--keep", "test"])

    flags = {
        "verbose": False,
        "yes": False,
        "all": False,
        "follow": False,
        "porcelain": False,
        "keep": True,
        "replace": False,
        "checkout": False,
    }

    assert result.exit_code == 0
    mock_init.assert_called_once_with(flags)

    result = runner.invoke(cli, ["-k", "test"])

    assert result.exit_code == 0
    mock_init.assert_called_with(flags)


def test_cli_flags_replace(
    temp_home: Path, runner: CliRunner, mocker: MockerFixture
):
    mock_init = mocker.patch.object(ShepherdMng, "__init__", return_value=None)

    result = runner.invoke(cli, ["--replace", "test"])

    flags = {
        "verbose": False,
        "yes": False,
        "all": False,
        "follow": False,
        "porcelain": False,
        "keep": False,
        "replace": True,
        "checkout": False,
    }

    assert result.exit_code == 0
    mock_init.assert_called_once_with(flags)

    result = runner.invoke(cli, ["-r", "test"])

    assert result.exit_code == 0
    mock_init.assert_called_with(flags)


def test_cli_flags_checkout(
    temp_home: Path, runner: CliRunner, mocker: MockerFixture
):
    mock_init = mocker.patch.object(ShepherdMng, "__init__", return_value=None)

    result = runner.invoke(cli, ["--checkout", "test"])

    flags = {
        "verbose": False,
        "yes": False,
        "all": False,
        "follow": False,
        "porcelain": False,
        "keep": False,
        "replace": False,
        "checkout": True,
    }

    assert result.exit_code == 0
    mock_init.assert_called_once_with(flags)

    result = runner.invoke(cli, ["-c", "test"])

    assert result.exit_code == 0
    mock_init.assert_called_with(flags)


def test_db_start(temp_home: Path, runner: CliRunner, mocker: MockerFixture):
    mock_start = mocker.patch.object(DatabaseMng, "start")
    result = runner.invoke(cli, ["db", "start"])
    assert result.exit_code == 0
    mock_start.assert_called_once()


def test_db_build(temp_home: Path, runner: CliRunner, mocker: MockerFixture):
    mock_build = mocker.patch.object(DatabaseMng, "build_image")
    result = runner.invoke(cli, ["db", "build"])
    assert result.exit_code == 0
    mock_build.assert_called_once()


def test_db_bootstrap(
    temp_home: Path, runner: CliRunner, mocker: MockerFixture
):
    mock_bootstrap = mocker.patch.object(DatabaseMng, "bootstrap")
    result = runner.invoke(cli, ["db", "bootstrap"])
    assert result.exit_code == 0
    mock_bootstrap.assert_called_once()


def test_db_halt(temp_home: Path, runner: CliRunner, mocker: MockerFixture):
    mock_halt = mocker.patch.object(DatabaseMng, "halt")
    result = runner.invoke(cli, ["db", "halt"])
    assert result.exit_code == 0
    mock_halt.assert_called_once()


def test_db_stdout(temp_home: Path, runner: CliRunner, mocker: MockerFixture):
    mock_stdout = mocker.patch.object(DatabaseMng, "stdout")
    result = runner.invoke(cli, ["db", "stdout"])
    assert result.exit_code == 0
    mock_stdout.assert_called_once()


def test_db_shell(temp_home: Path, runner: CliRunner, mocker: MockerFixture):
    mock_shell = mocker.patch.object(DatabaseMng, "shell")
    result = runner.invoke(cli, ["db", "shell"])
    assert result.exit_code == 0
    mock_shell.assert_called_once()


def test_db_sql_shell(
    temp_home: Path, runner: CliRunner, mocker: MockerFixture
):
    mock_sql_shell = mocker.patch.object(DatabaseMng, "sql_shell")
    result = runner.invoke(cli, ["db", "sql"])
    assert result.exit_code == 0
    mock_sql_shell.assert_called_once()


def test_env_init(temp_home: Path, runner: CliRunner, mocker: MockerFixture):
    mock_init = mocker.patch.object(EnvironmentMng, "init")
    result = runner.invoke(cli, ["env", "init", "db_type", "env_tag"])
    assert result.exit_code == 0
    mock_init.assert_called_once_with("db_type", "env_tag")


def test_env_clone(temp_home: Path, runner: CliRunner, mocker: MockerFixture):
    mock_clone = mocker.patch.object(EnvironmentMng, "clone")
    result = runner.invoke(cli, ["env", "clone", "src_env_tag", "dst_env_tag"])
    assert result.exit_code == 0
    mock_clone.assert_called_once_with("src_env_tag", "dst_env_tag")


def test_env_checkout(
    temp_home: Path, runner: CliRunner, mocker: MockerFixture
):
    mock_checkout = mocker.patch.object(EnvironmentMng, "checkout")
    result = runner.invoke(cli, ["env", "checkout", "env_tag"])
    assert result.exit_code == 0
    mock_checkout.assert_called_once_with("env_tag")


def test_env_set_noactive(
    temp_home: Path, runner: CliRunner, mocker: MockerFixture
):
    mock_noactive = mocker.patch.object(EnvironmentMng, "set_all_non_active")
    result = runner.invoke(cli, ["env", "noactive"])
    assert result.exit_code == 0
    mock_noactive.assert_called_once()


def test_env_list(temp_home: Path, runner: CliRunner, mocker: MockerFixture):
    mock_list = mocker.patch.object(EnvironmentMng, "list")
    result = runner.invoke(cli, ["env", "list"])
    assert result.exit_code == 0
    mock_list.assert_called_once()


def test_env_start(temp_home: Path, runner: CliRunner, mocker: MockerFixture):
    mock_start = mocker.patch.object(EnvironmentMng, "start")
    result = runner.invoke(cli, ["env", "start"])
    assert result.exit_code == 0
    mock_start.assert_called_once()


def test_env_halt(temp_home: Path, runner: CliRunner, mocker: MockerFixture):
    mock_halt = mocker.patch.object(EnvironmentMng, "halt")
    result = runner.invoke(cli, ["env", "halt"])
    assert result.exit_code == 0
    mock_halt.assert_called_once()


def test_env_reload(temp_home: Path, runner: CliRunner, mocker: MockerFixture):
    mock_reload = mocker.patch.object(EnvironmentMng, "reload")
    result = runner.invoke(cli, ["env", "reload"])
    assert result.exit_code == 0
    mock_reload.assert_called_once()


def test_env_status(temp_home: Path, runner: CliRunner, mocker: MockerFixture):
    mock_status = mocker.patch.object(EnvironmentMng, "status")
    result = runner.invoke(cli, ["env", "status"])
    assert result.exit_code == 0
    mock_status.assert_called_once()


def test_srv_build(temp_home: Path, runner: CliRunner, mocker: MockerFixture):
    mock_build = mocker.patch.object(ServiceMng, "build_image")
    result = runner.invoke(cli, ["svc", "build", "service_type"])
    assert result.exit_code == 0
    mock_build.assert_called_once_with("service_type")


def test_srv_bootstrap(
    temp_home: Path, runner: CliRunner, mocker: MockerFixture
):
    mock_bootstrap = mocker.patch.object(ServiceMng, "bootstrap")
    result = runner.invoke(cli, ["svc", "bootstrap", "service_type"])
    assert result.exit_code == 0
    mock_bootstrap.assert_called_once_with("service_type")


def test_srv_start(temp_home: Path, runner: CliRunner, mocker: MockerFixture):
    mock_start = mocker.patch.object(ServiceMng, "start")
    result = runner.invoke(cli, ["svc", "start", "service_type"])
    assert result.exit_code == 0
    mock_start.assert_called_once_with("service_type")


def test_srv_halt(temp_home: Path, runner: CliRunner, mocker: MockerFixture):
    mock_halt = mocker.patch.object(ServiceMng, "halt")
    result = runner.invoke(cli, ["svc", "halt", "service_type"])
    assert result.exit_code == 0
    mock_halt.assert_called_once_with("service_type")


def test_srv_reload(temp_home: Path, runner: CliRunner, mocker: MockerFixture):
    mock_reload = mocker.patch.object(ServiceMng, "reload")
    result = runner.invoke(cli, ["svc", "reload", "service_type"])
    assert result.exit_code == 0
    mock_reload.assert_called_once_with("service_type")


def test_srv_stdout(temp_home: Path, runner: CliRunner, mocker: MockerFixture):
    mock_stdout = mocker.patch.object(ServiceMng, "stdout")
    result = runner.invoke(cli, ["svc", "stdout", "service_id"])
    assert result.exit_code == 0
    mock_stdout.assert_called_once_with("service_id")


def test_srv_shell(temp_home: Path, runner: CliRunner, mocker: MockerFixture):
    mock_shell = mocker.patch.object(ServiceMng, "shell")
    result = runner.invoke(cli, ["svc", "shell", "service_id"])
    assert result.exit_code == 0
    mock_shell.assert_called_once_with("service_id")
