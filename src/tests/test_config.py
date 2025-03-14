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
import tempfile
from unittest.mock import mock_open

import pytest
from pytest_mock import MockerFixture

from config import Config, ConfigMng

config_json = """{
  "ora": {
    "image": "${ora_image}",
    "empty_env": "${ora_empty_env}",
    "pump_dir_name": "${ora_pump_dir}",
    "root_db_name": "${ora_root_db_name}",
    "plug_db_name": "${ora_plug_db_name}",
    "net_listener_port": "${ora_listener_port}"
  },
  "pg": {
    "image": "${pg_image}",
    "empty_env": "${pg_empty_env}",
    "net_listener_port": "${pg_listener_port}"
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
  "envs_dir": "${env_base_dir}",
  "db_default": {
    "sys_user": "${db_sys_usr}",
    "sys_psw": "${db_sys_psw}",
    "user": "${db_usr}",
    "psw": "${db_psw}"
  },
  "envs": [
    {
      "tag": "sample-1",
      "services": [
        {
          "type": "pg",
          "tag": "pg-1",
          "image": "ghcr.io/lunaticfringers/shepherd/postgres:17-3.5",
          "ingress": null,
          "envvars": null,
          "ports": {},
          "properties": {
            "sys_user": "syspg1",
            "sys_psw": "syspg1",
            "user": "pg1",
            "psw": "pg1"
          },
          "subject_alternative_name": null,
          "db_upstreams": [
            {
              "tag": "upstream",
              "type": "pg",
              "user": "pg1up",
              "psw": "pg1up",
              "host": "localhost",
              "port": "5432",
              "database": "d_pg1",
              "unix_user": "postgres",
              "dump_dir": "/dumps",
              "enabled": false
            }
          ]
        },
        {
          "type": "traefik",
          "tag": "traefik-1",
          "image": "",
          "ingress": true,
          "envvars": null,
          "ports": {},
          "properties": {},
          "subject_alternative_name": null,
          "db_upstreams": []
        },
        {
          "type": "custom-1",
          "tag": "primary",
          "image": "",
          "ingress": true,
          "envvars": null,
          "ports": null,
          "properties": {
            "instance.name": "primary",
            "instance.id": 1
          },
          "subject_alternative_name": null,
          "db_upstreams": []
        },
        {
          "type": "nodejs",
          "tag": "poke",
          "image": "",
          "ingress": null,
          "envvars": {
            "USER": "user",
            "PSW": "psw"
          },
          "ports": {
            "http": "3000:3000"
          },
          "properties": {},
          "subject_alternative_name": null,
          "db_upstreams": []
        }
      ],
      "archived": false,
      "active": false
    }
  ]
}"""

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

  # Environment Directory Configuration
  env_base_dir=~/shpdenvs

  # Database Default Configuration
  db_sys_usr=sys
  db_sys_psw=sys
  db_usr=docker
  db_psw=docker
  """


def test_load_config(mocker: MockerFixture):
    """Test regular parsing"""

    cMng = ConfigMng()

    mock_open1 = mock_open(read_data=config_json)
    mock_open2 = mock_open(read_data=values)

    mocker.patch("os.path.exists", return_value=True)
    mocker.patch(
        "builtins.open",
        side_effect=[mock_open1.return_value, mock_open2.return_value],
    )

    config: Config = cMng.load_config("mock.1", "mock.2")

    assert (
        config.ora.image
        == "ghcr.io/lunaticfringers/shepherd/oracle:19.3.0.0_TZ40"
    )
    assert config.pg.image == "ghcr.io/lunaticfringers/shepherd/postgres:17-3.5"
    assert config.shpd_registry.ftp_server == "ftp.example.com"
    assert config.envs[0].tag == "sample-1"
    assert config.db_default.sys_user == "sys"
    services = config.envs[0].services
    assert services and services[0].type == "pg"
    assert services[0].tag == "pg-1"
    assert services[0].image == (
        "ghcr.io/lunaticfringers/shepherd/postgres:17-3.5"
    )
    properties = services[0].properties
    assert properties and properties["sys_user"] == "syspg1"
    assert properties["sys_psw"] == "syspg1"
    assert properties["user"] == "pg1"
    assert properties["psw"] == "pg1"
    db_upstreams = services[0].db_upstreams
    assert db_upstreams and db_upstreams[0].tag == "upstream"
    assert db_upstreams[0].type == "pg"
    assert db_upstreams[0].user == "pg1up"
    assert db_upstreams[0].psw == "pg1up"
    assert db_upstreams[0].host == "localhost"
    assert db_upstreams[0].port == "5432"
    assert db_upstreams[0].database == "d_pg1"
    assert db_upstreams[0].unix_user == "postgres"
    assert db_upstreams[0].dump_dir == "/dumps"
    assert db_upstreams[0].enabled is False
    assert services[1].type == "traefik"
    assert services[1].ingress is True
    assert services[2].type == "custom-1"
    assert services[2].tag == "primary"
    assert services[3].type == "nodejs"
    assert services[3].tag == "poke"
    envvars = services[3].envvars
    assert envvars and envvars.get("USER") == "user"
    assert envvars and envvars.get("PSW") == "psw"
    ports = services[3].ports
    assert ports and ports["http"] == "3000:3000"
    assert config.host_inet_ip == "127.0.0.1"
    assert config.domain == "sslip.io"
    assert config.dns_type == "autoresolving"
    assert config.ca.country == "IT"
    assert config.ca.state == "MS"
    assert config.ca.locality == "Carrara"
    assert config.ca.organization == "LunaticFringe"
    assert config.ca.organizational_unit == "Development"
    assert config.ca.common_name == "sslip.io"
    assert config.ca.email == "lf@sslip.io"
    assert config.ca.passphrase == "test"
    assert config.cert.country == "IT"
    assert config.cert.state == "MS"
    assert config.cert.locality == "Carrara"
    assert config.cert.organization == "LunaticFringe"
    assert config.cert.organizational_unit == "Development"
    assert config.cert.common_name == "sslip.io"
    assert config.cert.email == "lf@sslip.io"
    assert config.cert.subject_alternative_names == []
    assert config.envs_dir == "~/shpdenvs"
    assert config.db_default.sys_psw == "sys"
    assert config.db_default.user == "docker"
    assert config.db_default.psw == "docker"
    assert config.envs[0].archived is False
    assert config.envs[0].active is False


def test_load_user_values_file_not_found(mocker: MockerFixture):
    """Test file_values_path does not exist"""

    cMng = ConfigMng()

    mock_open1 = mock_open(read_data="{}")
    mocker.patch(
        "builtins.open",
        side_effect=[mock_open1.return_value, OSError("File not found")],
    )

    with pytest.raises(FileNotFoundError):
        cMng.load_config("mock.1", "not-exist")


def test_load_invalid_user_values(mocker: MockerFixture):
    """Test invalid user values"""

    cMng = ConfigMng()

    mock_open1 = mock_open(read_data="{}")
    mock_open2 = mock_open(read_data="key")

    mocker.patch("os.path.exists", return_value=True)
    mocker.patch(
        "builtins.open",
        side_effect=[mock_open1.return_value, mock_open2.return_value],
    )

    with pytest.raises(ValueError):
        cMng.load_config("mock.1", "mock.2")


def test_store_config_with_temp_files():
    """Test storing config using real temp files"""

    cMng = ConfigMng()

    with (
        tempfile.NamedTemporaryFile(delete=False) as temp_config_file,
        tempfile.NamedTemporaryFile(delete=False) as temp_values_file,
        tempfile.NamedTemporaryFile(delete=False) as temp_output_file,
    ):

        temp_config_file.write(config_json.encode())
        temp_values_file.write(values.encode())
        temp_config_file.close()
        temp_values_file.close()

        config: Config = cMng.load_config(
            temp_config_file.name, temp_values_file.name
        )

        cMng.store_config(config, temp_output_file.name)

        content = temp_output_file.read().decode()
        assert content == config_json

        os.remove(temp_config_file.name)
        os.remove(temp_values_file.name)
        os.remove(temp_output_file.name)
