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

from pathlib import Path

import pytest
from click.testing import CliRunner
from pytest_mock import MockerFixture

from shepctl import ShepherdMng, cli

values = """
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

  shpd_dir=~/shpd

  # Database Default Configuration
  db_sys_usr=sys
  db_sys_psw=sys
  db_usr=docker
  db_psw=docker

  # Logging Configuration
  log_file=~/shpd/shepctl.log
  log_level=WARNING
  log_stdout=false
  log_format=%(asctime)s - %(levelname)s - %(message)s
  """

shpd_config_svc_default = """
{
  "logging": {
    "file": "${log_file}",
    "level": "${log_level}",
    "stdout": "${log_stdout}",
    "format": "${log_format}"
  },
  "shpd_registry": {
    "ftp_server": "${shpd_registry}",
    "ftp_user": "${shpd_registry_ftp_usr}",
    "ftp_psw": "${shpd_registry_ftp_psw}",
    "ftp_shpd_path": "${shpd_registry_ftp_shpd_path}",
    "ftp_env_imgs_path": "${shpd_registry_ftp_imgs_path}"
  },
  "host_inet_ip": "${host_inet_ip}",
  "domain": "${domain}",
  "dns_type": "${dns_type}",
  "ca": {
    "country": "${ca_country}",
    "state": "${ca_state}",
    "locality": "${ca_locality}",
    "organization": "${ca_org}",
    "organizational_unit": "${ca_org_unit}",
    "common_name": "${ca_cn}",
    "email": "${ca_email}",
    "passphrase": "${ca_passphrase}"
  },
  "cert": {
    "country": "${cert_country}",
    "state": "${cert_state}",
    "locality": "${cert_locality}",
    "organization": "${cert_org}",
    "organizational_unit": "${cert_org_unit}",
    "common_name": "${cert_cn}",
    "email": "${cert_email}",
    "subject_alternative_names": []
  },
  "env_templates": [
    {
      "tag": "default",
      "factory": "docker-compose",
      "service_templates": [
        {
          "template": "default",
          "tag": "service-default"
        }
      ],
      "networks": [
        {
          "key": "shpdnet",
          "name": "envnet",
          "external": true
        }
      ]
    }
  ],
  "service_templates": [
    {
      "tag": "default",
      "factory": "docker",
      "image": "test-image:latest",
      "labels": [
        "com.example.label1=value1",
        "com.example.label2=value2"
      ],
      "workdir": "/test",
      "volumes": [
          "/home/test/.ssh:/home/test/.ssh",
          "/etc/ssh:/etc/ssh"
      ],
      "ingress": false,
      "empty_env": null,
      "environment": [],
      "ports": [
        "80:80",
        "443:443",
        "8080:8080"
      ],
      "properties": {},
      "networks": [
        "default"
      ],
      "extra_hosts": [
        "host.docker.internal:host-gateway"
      ],
      "subject_alternative_name": null
    }
  ],
  "envs": [
    {
      "template": "default",
      "factory": "docker-compose",
      "tag": "test-1",
      "services": [
        {
          "template": "default",
          "factory": "docker",
          "tag": "test",
          "image": "test-image:latest",
          "labels": [
            "com.example.label1=value1",
            "com.example.label2=value2"
          ],
          "workdir": "/test",
          "volumes": [
              "/home/test/.ssh:/home/test/.ssh",
              "/etc/ssh:/etc/ssh"
          ],
          "ingress": false,
          "empty_env": null,
          "environment": [],
          "ports": [
            "80:80",
            "443:443",
            "8080:8080"
          ],
          "properties": {},
          "networks": [
            "default"
          ],
          "extra_hosts": [
            "host.docker.internal:host-gateway"
          ],
          "subject_alternative_name": null
        }
      ],
      "archived": false,
      "active": true
    }
  ]
}
"""

shpd_config_pg_template = """
{
  "logging": {
    "file": "${log_file}",
    "level": "${log_level}",
    "stdout": "${log_stdout}",
    "format": "${log_format}"
  },
  "shpd_registry": {
    "ftp_server": "${shpd_registry}",
    "ftp_user": "${shpd_registry_ftp_usr}",
    "ftp_psw": "${shpd_registry_ftp_psw}",
    "ftp_shpd_path": "${shpd_registry_ftp_shpd_path}",
    "ftp_env_imgs_path": "${shpd_registry_ftp_imgs_path}"
  },
  "host_inet_ip": "${host_inet_ip}",
  "domain": "${domain}",
  "dns_type": "${dns_type}",
  "ca": {
    "country": "${ca_country}",
    "state": "${ca_state}",
    "locality": "${ca_locality}",
    "organization": "${ca_org}",
    "organizational_unit": "${ca_org_unit}",
    "common_name": "${ca_cn}",
    "email": "${ca_email}",
    "passphrase": "${ca_passphrase}"
  },
  "cert": {
    "country": "${cert_country}",
    "state": "${cert_state}",
    "locality": "${cert_locality}",
    "organization": "${cert_org}",
    "organizational_unit": "${cert_org_unit}",
    "common_name": "${cert_cn}",
    "email": "${cert_email}",
    "subject_alternative_names": []
  },
  "env_templates": [
    {
      "tag": "default",
      "factory": "docker-compose",
      "service_templates": [
        {
          "template": "default",
          "tag": "service-default"
        }
      ],
      "networks": [
        {
          "key": "shpdnet",
          "name": "envnet",
          "external": true
        }
      ]
    }
  ],
  "service_templates": [
    {
      "tag": "default",
      "factory": "docker",
      "image": "",
      "ingress": false,
      "empty_env": null,
      "envvars": {},
      "ports": [],
      "properties": {},
      "subject_alternative_name": null
    },
    {
      "tag": "postgres",
      "factory": "postgres",
      "image": "${pg_image}",
      "ingress": false,
      "empty_env": "${pg_empty_env}",
      "envvars": {},
      "ports": [
        "net_listener_port:${pg_listener_port}"
      ],
      "properties": {
        "sys_user": "${db_sys_usr}",
        "sys_psw": "${db_sys_psw}",
        "user": "${db_usr}",
        "psw": "${db_psw}"
      },
      "subject_alternative_name": null
    }
  ],
  "envs": []
}
"""


@pytest.fixture
def temp_home(tmp_path: Path, mocker: MockerFixture) -> Path:
    """Fixture to create a temporary home directory and .shpd.conf file."""
    temp_home = tmp_path / "home"
    temp_home.mkdir()

    config_file = temp_home / ".shpd.conf"
    config_file.write_text(values)

    return temp_home


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def make_expanduser_side_effect(path: Path, calls: int):
    """Generate a list of `os.path.expanduser` return
    values repeating [shpd, .shpd.conf, shpd/shepctl.log]."""
    return [
        (
            path / ".shpd.conf"
            if i % 3 == 0
            else (
                path / "shpd" if i % 3 == 1 else path / "shpd" / "shepctl.log"
            )
        )
        for i in range(calls * 3)
    ]


@pytest.mark.svc
@pytest.mark.parametrize("expanduser_side_effects", [4])
def test_svc_add_one_default(
    temp_home: Path,
    runner: CliRunner,
    mocker: MockerFixture,
    expanduser_side_effects: int,
):
    side_effect = make_expanduser_side_effect(
        temp_home, expanduser_side_effects
    )
    mocker.patch("os.path.expanduser", side_effect=side_effect)

    result = runner.invoke(cli, ["env", "init", "default", "test-svc-add"])
    assert result.exit_code == 0

    result = runner.invoke(cli, ["env", "checkout", "test-svc-add"])
    assert result.exit_code == 0

    result = runner.invoke(cli, ["env", "add", "svc", "svc-1"])
    assert result.exit_code == 0

    sm = ShepherdMng()

    env = sm.configMng.get_active_environment()

    assert env is not None, "Active environment should not be None"
    assert env.services is not None, "Services should not be None"
    assert len(env.services) == 2, "There should be exactly two services"

    assert (
        env.services[0].tag == "service-default"
    ), "Service tag should be 'service-default'"
    assert (
        env.services[0].template == "default"
    ), "Service type should be 'default'"
    assert (
        env.services[0].factory == "docker"
    ), "Service factory should be 'docker'"
    assert env.services[0].image == "", "Service image should be ''"

    assert env.services[0].ingress is False, "Service ingress should be False"
    assert (
        env.services[0].environment == []
    ), "Service environment should be empty"
    assert env.services[0].ports == [], "Service ports should be empty"
    assert (
        env.services[0].properties == {}
    ), "Service properties should be empty"
    assert (
        env.services[0].subject_alternative_name is None
    ), "Service SAN should be None"

    assert env.services[1].tag == "svc-1", "Service tag should be 'svc-1'"
    assert (
        env.services[1].template == "default"
    ), "Service type should be 'default'"
    assert (
        env.services[1].factory == "docker"
    ), "Service factory should be 'docker'"
    assert env.services[1].image == "", "Service image should be ''"

    assert env.services[1].ingress is False, "Service ingress should be False"
    assert (
        env.services[1].environment == []
    ), "Service environment should be empty"
    assert env.services[1].ports == [], "Service ports should be empty"
    assert (
        env.services[1].properties == {}
    ), "Service properties should be empty"
    assert (
        env.services[1].subject_alternative_name is None
    ), "Service SAN should be None"


@pytest.mark.svc
@pytest.mark.parametrize("expanduser_side_effects", [5])
def test_svc_add_two_default(
    temp_home: Path,
    runner: CliRunner,
    mocker: MockerFixture,
    expanduser_side_effects: int,
):
    side_effect = make_expanduser_side_effect(
        temp_home, expanduser_side_effects
    )
    mocker.patch("os.path.expanduser", side_effect=side_effect)

    result = runner.invoke(cli, ["env", "init", "default", "test-svc-add"])
    assert result.exit_code == 0

    result = runner.invoke(cli, ["env", "checkout", "test-svc-add"])
    assert result.exit_code == 0

    result = runner.invoke(cli, ["env", "add", "svc", "svc-1"])
    assert result.exit_code == 0

    result = runner.invoke(cli, ["env", "add", "svc", "svc-2"])
    assert result.exit_code == 0

    sm = ShepherdMng()

    env = sm.configMng.get_active_environment()
    assert env is not None, "Active environment should not be None"
    assert env.services is not None, "Services should not be None"
    assert len(env.services) == 3, "There should be exactly three services"

    assert env.services[1].tag == "svc-1", "Service tag should be 'svc-1'"
    assert (
        env.services[1].template == "default"
    ), "Service type should be 'default'"
    assert (
        env.services[1].factory == "docker"
    ), "Service factory should be 'docker'"
    assert env.services[1].image == "", "Service image should be ''"

    assert env.services[1].ingress is False, "Service ingress should be False"
    assert (
        env.services[1].environment == []
    ), "Service environment should be empty"
    assert env.services[1].ports == [], "Service ports should be empty"
    assert (
        env.services[1].properties == {}
    ), "Service properties should be empty"
    assert (
        env.services[1].subject_alternative_name is None
    ), "Service SAN should be None"

    assert env.services[2].tag == "svc-2", "Service tag should be 'svc-2'"
    assert (
        env.services[2].template == "default"
    ), "Service type should be 'default'"
    assert (
        env.services[2].factory == "docker"
    ), "Service factory should be 'docker'"
    assert env.services[2].image == "", "Service image should be ''"

    assert env.services[2].ingress is False, "Service ingress should be False"
    assert (
        env.services[2].environment == []
    ), "Service environment should be empty"
    assert env.services[2].ports == [], "Service ports should be empty"
    assert (
        env.services[2].properties == {}
    ), "Service properties should be empty"
    assert (
        env.services[2].subject_alternative_name is None
    ), "Service SAN should be None"


@pytest.mark.svc
@pytest.mark.parametrize("expanduser_side_effects", [5])
def test_svc_add_two_same_tag_default(
    temp_home: Path,
    runner: CliRunner,
    mocker: MockerFixture,
    expanduser_side_effects: int,
):
    side_effect = make_expanduser_side_effect(
        temp_home, expanduser_side_effects
    )
    mocker.patch("os.path.expanduser", side_effect=side_effect)

    result = runner.invoke(cli, ["env", "init", "default", "test-svc-add"])
    assert result.exit_code == 0

    result = runner.invoke(cli, ["env", "checkout", "test-svc-add"])
    assert result.exit_code == 0

    result = runner.invoke(cli, ["env", "add", "svc", "svc-1"])
    assert result.exit_code == 0

    result = runner.invoke(cli, ["env", "add", "svc", "svc-1"])
    assert result.exit_code == 1

    sm = ShepherdMng()

    env = sm.configMng.get_active_environment()
    assert env is not None, "Active environment should not be None"
    assert env.services is not None, "Services should not be None"
    assert len(env.services) == 2, "There should be exactly one service"
    assert env.services[1].tag == "svc-1", "Service tag should be 'svc-1'"
    assert (
        env.services[1].template == "default"
    ), "Service type should be 'default'"
    assert (
        env.services[1].factory == "docker"
    ), "Service factory should be 'docker'"
    assert env.services[1].image == "", "Service image should be ''"

    assert env.services[1].ingress is False, "Service ingress should be False"
    assert (
        env.services[1].environment == []
    ), "Service environment should be empty"
    assert env.services[1].ports == [], "Service ports should be empty"
    assert (
        env.services[1].properties == {}
    ), "Service properties should be empty"
    assert (
        env.services[1].subject_alternative_name is None
    ), "Service SAN should be None"


@pytest.mark.svc
@pytest.mark.parametrize("expanduser_side_effects", [4])
def test_svc_add_one_with_template(
    temp_home: Path,
    runner: CliRunner,
    mocker: MockerFixture,
    expanduser_side_effects: int,
):
    side_effect = make_expanduser_side_effect(
        temp_home, expanduser_side_effects
    )
    mocker.patch("os.path.expanduser", side_effect=side_effect)
    shpd_dir = temp_home / "shpd"
    shpd_dir.mkdir(parents=True, exist_ok=True)
    shpd_json = shpd_dir / ".shpd.json"
    shpd_json.write_text(shpd_config_pg_template)

    result = runner.invoke(cli, ["env", "init", "default", "test-svc-add"])
    assert result.exit_code == 0

    result = runner.invoke(cli, ["env", "checkout", "test-svc-add"])
    assert result.exit_code == 0

    result = runner.invoke(
        cli, ["env", "add", "svc", "pg-1", "postgres", "database"]
    )

    # no 'postgres' factory, so this should fail
    assert result.exit_code == 1

    sm = ShepherdMng()

    env = sm.configMng.get_active_environment()
    assert env is not None, "Active environment should not be None"
    assert env.services is not None, "Services should not be None"
    assert (
        len(env.services) == 1
    ), "There should be exactly one (default) service"

    assert (
        env.services[0].tag == "service-default"
    ), "Service tag should be 'service-default'"


@pytest.mark.svc
@pytest.mark.parametrize("expanduser_side_effects", [1])
def test_svc_render_compose_service(
    temp_home: Path,
    runner: CliRunner,
    mocker: MockerFixture,
    expanduser_side_effects: int,
):
    side_effect = make_expanduser_side_effect(
        temp_home, expanduser_side_effects
    )
    mocker.patch("os.path.expanduser", side_effect=side_effect)
    shpd_dir = temp_home / "shpd"
    shpd_dir.mkdir(parents=True, exist_ok=True)
    shpd_json = shpd_dir / ".shpd.json"
    shpd_json.write_text(shpd_config_svc_default)

    result = runner.invoke(cli, ["svc", "render", "test"])
    assert result.exit_code == 0

    assert result.output == (
        "services:\n"
        "  test-test-1:\n"
        "    image: test-image:latest\n"
        "    hostname: test-test-1\n"
        "    container_name: test-test-1\n"
        "    labels:\n"
        "    - com.example.label1=value1\n"
        "    - com.example.label2=value2\n"
        "    volumes:\n"
        "    - /home/test/.ssh:/home/test/.ssh\n"
        "    - /etc/ssh:/etc/ssh\n"
        "    ports:\n"
        "    - 80:80\n"
        "    - 443:443\n"
        "    - 8080:8080\n"
        "    extra_hosts:\n"
        "    - host.docker.internal:host-gateway\n"
        "    networks:\n"
        "    - default\n\n"
    )
