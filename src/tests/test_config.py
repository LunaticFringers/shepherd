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
from unittest.mock import mock_open

import pytest
from pytest_mock import MockerFixture

from config import Config, ConfigMng

config_json = """{
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
  "service_types": [
    {
      "type": "oracle",
      "image": "${ora_image}",
      "ingress": false,
      "empty_env": "${ora_empty_env}",
      "envvars": {},
      "ports": {
        "net_listener_port": "${ora_listener_port}"
      },
      "properties": {
        "pump_dir_name": "${ora_pump_dir}",
        "root_db_name": "${ora_root_db_name}",
        "plug_db_name": "${ora_plug_db_name}",
        "sys_user": "${db_sys_usr}",
        "sys_psw": "${db_sys_psw}",
        "user": "${db_usr}",
        "psw": "${db_psw}"
      },
      "subject_alternative_name": null
    },
    {
      "type": "postgres",
      "image": "${pg_image}",
      "ingress": false,
      "empty_env": "${pg_empty_env}",
      "envvars": {},
      "ports": {
        "net_listener_port": "${pg_listener_port}"
      },
      "properties": {
        "sys_user": "${db_sys_usr}",
        "sys_psw": "${db_sys_psw}",
        "user": "${db_usr}",
        "psw": "${db_psw}"
      },
      "subject_alternative_name": null
    }
  ],
  "envs": [
    {
      "tag": "sample-1",
      "services": [
        {
          "type": "postgres",
          "tag": "pg-1",
          "image": "ghcr.io/lunaticfringers/shepherd/postgres:17-3.5",
          "ingress": null,
          "empty_env": null,
          "envvars": null,
          "ports": {},
          "properties": {
            "sys_user": "syspg1",
            "sys_psw": "syspg1",
            "user": "pg1",
            "psw": "pg1"
          },
          "subject_alternative_name": null,
          "upstreams": [
            {
              "tag": "upstream-1",
              "type": "postgres",
              "enabled": true,
              "properties": {
                "user": "pg1up",
                "psw": "pg1up",
                "host": "localhost",
                "port": "5432",
                "database": "d_pg1",
                "unix_user": "postgres",
                "dump_dir": "/dumps"
              }
            },
            {
              "tag": "upstream-2",
              "type": "postgres",
              "enabled": false,
              "properties": {
                "user": "pg2up",
                "psw": "pg2up",
                "host": "moon",
                "port": "5432",
                "database": "d_pg2",
                "unix_user": "postgres",
                "dump_dir": "/dumps/2"
              }
            }
          ]
        },
        {
          "type": "traefik",
          "tag": "traefik-1",
          "image": "",
          "ingress": true,
          "empty_env": null,
          "envvars": null,
          "ports": {},
          "properties": {},
          "subject_alternative_name": null,
          "upstreams": []
        },
        {
          "type": "custom-1",
          "tag": "primary",
          "image": "",
          "ingress": true,
          "empty_env": null,
          "envvars": null,
          "ports": null,
          "properties": {
            "instance.name": "primary",
            "instance.id": 1
          },
          "subject_alternative_name": null,
          "upstreams": []
        },
        {
          "type": "nodejs",
          "tag": "poke",
          "image": "",
          "ingress": null,
          "empty_env": null,
          "envvars": {
            "USER": "user",
            "PSW": "psw"
          },
          "ports": {
            "http": "3000:3000"
          },
          "properties": {},
          "subject_alternative_name": null,
          "upstreams": []
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

  shpd_dir=.

  # Database Default Configuration
  db_sys_usr=sys
  db_sys_psw=sys
  db_usr=docker
  db_psw=docker
  """


def test_load_config(mocker: MockerFixture):
    """Test regular parsing"""

    mock_open1 = mock_open(read_data=values)
    mock_open2 = mock_open(read_data=config_json)

    mocker.patch("os.path.exists", return_value=True)
    mocker.patch(
        "builtins.open",
        side_effect=[mock_open1.return_value, mock_open2.return_value],
    )

    cMng = ConfigMng(".shpd.conf")
    config: Config = cMng.load_config()

    service_types = config.service_types
    assert service_types and service_types[0].type == "oracle"
    assert service_types[0].image == (
        "ghcr.io/lunaticfringers/shepherd/oracle:19.3.0.0_TZ40"
    )
    assert service_types[0].empty_env == "fresh-ora-19300"
    assert service_types[0].ingress is False
    assert service_types[0].envvars == {}
    assert (
        service_types[0].ports
        and service_types[0].ports["net_listener_port"] == "1521"
    )
    assert (
        service_types[0].properties
        and service_types[0].properties["pump_dir_name"] == "PUMP_DIR"
    )
    assert service_types[0].properties["root_db_name"] == "ORCLCDB"
    assert service_types[0].properties["plug_db_name"] == "ORCLPDB1"
    assert service_types[0].properties["sys_user"] == "sys"
    assert service_types[0].properties["sys_psw"] == "sys"
    assert service_types[0].properties["user"] == "docker"
    assert service_types[0].properties["psw"] == "docker"
    assert service_types[0].subject_alternative_name is None
    assert service_types[1].type == "postgres"
    assert service_types[1].image == (
        "ghcr.io/lunaticfringers/shepherd/postgres:17-3.5"
    )
    assert service_types[1].empty_env == "fresh-pg-1735"
    assert service_types[1].ingress is False
    assert service_types[1].envvars == {}
    assert (
        service_types[1].ports
        and service_types[1].ports["net_listener_port"] == "5432"
    )
    assert (
        service_types[1].properties
        and service_types[1].properties["sys_user"] == "sys"
    )
    assert service_types[1].properties["sys_psw"] == "sys"
    assert service_types[1].properties["user"] == "docker"
    assert service_types[1].properties["psw"] == "docker"
    assert service_types[1].subject_alternative_name is None

    assert config.shpd_registry.ftp_server == "ftp.example.com"
    assert config.envs[0].tag == "sample-1"
    services = config.envs[0].services
    assert services and services[0].type == "postgres"
    assert services[0].tag == "pg-1"
    assert services[0].image == (
        "ghcr.io/lunaticfringers/shepherd/postgres:17-3.5"
    )
    properties = services[0].properties
    assert properties and properties["sys_user"] == "syspg1"
    assert properties["sys_psw"] == "syspg1"
    assert properties["user"] == "pg1"
    assert properties["psw"] == "pg1"
    upstreams = services[0].upstreams
    assert upstreams and upstreams[0].tag == "upstream-1"
    properties = upstreams[0].properties
    assert properties and properties["user"] == "pg1up"
    assert properties["psw"] == "pg1up"
    assert properties["host"] == "localhost"
    assert properties["port"] == "5432"
    assert properties["database"] == "d_pg1"
    assert properties["unix_user"] == "postgres"
    assert properties["dump_dir"] == "/dumps"
    assert upstreams[0].enabled is True
    assert upstreams[1].tag == "upstream-2"
    properties = upstreams[1].properties
    assert properties and properties["user"] == "pg2up"
    assert properties["psw"] == "pg2up"
    assert properties["host"] == "moon"
    assert properties["port"] == "5432"
    assert properties["database"] == "d_pg2"
    assert properties["unix_user"] == "postgres"
    assert properties["dump_dir"] == "/dumps/2"
    assert upstreams[1].enabled is False
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
    assert config.envs[0].archived is False
    assert config.envs[0].active is False


def test_load_user_values_file_not_found(mocker: MockerFixture):
    """Test file_values_path does not exist"""

    mock_open1 = mock_open(read_data="{}")
    mocker.patch(
        "builtins.open",
        side_effect=[OSError("File not found"), mock_open1.return_value],
    )

    with pytest.raises(SystemExit) as exc_info:
        ConfigMng(".shpd.conf")
        assert exc_info.value.code == 1


def test_load_invalid_user_values(mocker: MockerFixture):
    """Test invalid user values"""

    mock_open1 = mock_open(read_data="key")
    mock_open2 = mock_open(read_data="{}")

    mocker.patch("os.path.exists", return_value=True)
    mocker.patch(
        "builtins.open",
        side_effect=[mock_open1.return_value, mock_open2.return_value],
    )

    with pytest.raises(SystemExit) as exc_info:
        ConfigMng(".shpd.conf")
        assert exc_info.value.code == 1


def test_store_config_with_real_files():
    """Test storing config using real files in ./"""

    try:
        with (
            open(".shpd.json", "w") as config_file,
            open(".shpd.conf", "w") as values_file,
        ):
            config_file.write(config_json)
            values_file.write(values)

        cMng = ConfigMng(values_file.name)
        config: Config = cMng.load_config()
        cMng.store_config(config)

        with open(".shpd.json", "r") as output_file:
            content = output_file.read()
            assert content == config_json

    finally:
        for file_path in (".shpd.json", ".shpd.conf"):
            if os.path.exists(file_path):
                os.remove(file_path)
