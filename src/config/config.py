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

import json
import os
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DBUpstreamCfg:
    tag: str
    type: str
    user: str
    psw: str
    host: str
    port: str
    database: str
    unix_user: str
    dump_dir: str
    enabled: bool


@dataclass
class ServiceCfg:
    type: str
    tag: str
    image: str
    ingress: Optional[bool] = None
    envvars: Optional[dict[str, str]] = field(default_factory=dict)
    ports: Optional[dict[str, str]] = field(default_factory=dict)
    properties: Optional[dict[str, str]] = field(default_factory=dict)
    subject_alternative_name: Optional[str] = None
    db_upstreams: Optional[List[DBUpstreamCfg]] = field(default_factory=list)


@dataclass
class EnvironmentCfg:
    tag: str
    services: Optional[List[ServiceCfg]]
    archived: bool
    active: bool


@dataclass
class OracleCfg:
    image: str
    empty_env: str
    pump_dir_name: str
    root_db_name: str
    plug_db_name: str
    net_listener_port: str


@dataclass
class PostgresCfg:
    image: str
    empty_env: str
    net_listener_port: str


@dataclass
class ShpdRegistryCfg:
    ftp_server: str
    ftp_user: str
    ftp_psw: str
    ftp_shpd_path: str
    ftp_env_imgs_path: str


@dataclass
class CACfg:
    country: str
    state: str
    locality: str
    organization: str
    organizational_unit: str
    common_name: str
    email: str
    passphrase: str


@dataclass
class CertCfg:
    country: str
    state: str
    locality: str
    organization: str
    organizational_unit: str
    common_name: str
    email: str
    subject_alternative_names: List[str] = field(default_factory=list)


@dataclass
class DbDefaultCfg:
    sys_user: str
    sys_psw: str
    user: str
    psw: str


@dataclass
class Config:
    ora: OracleCfg
    pg: PostgresCfg
    shpd_registry: ShpdRegistryCfg
    host_inet_ip: str
    domain: str
    dns_type: str
    ca: CACfg
    cert: CertCfg
    envs_dir: str
    db_default: DbDefaultCfg
    envs: List[EnvironmentCfg] = field(default_factory=list)


def parse_config(json_str: str) -> Config:
    data = json.loads(json_str)

    def parse_upstream(item: Any) -> DBUpstreamCfg:
        return DBUpstreamCfg(
            tag=item["tag"],
            type=item["type"],
            user=item["user"],
            psw=item["psw"],
            host=item["host"],
            port=item["port"],
            database=item["database"],
            unix_user=item["unix_user"],
            dump_dir=item["dump_dir"],
            enabled=item["enabled"],
        )

    def parse_service(item: Any) -> ServiceCfg:
        return ServiceCfg(
            type=item["type"],
            tag=item["tag"],
            image=item["image"],
            ingress=item.get("ingress"),
            envvars=item.get("envvars", {}),
            ports=item.get("ports", {}),
            properties=item.get("properties", {}),
            subject_alternative_name=item.get("subject_alternative_name"),
            db_upstreams=[
                parse_upstream(upstream)
                for upstream in item.get("db_upstreams", [])
            ],
        )

    def parse_environment(item: Any) -> EnvironmentCfg:
        return EnvironmentCfg(
            tag=item["tag"],
            services=[
                parse_service(service) for service in item.get("services", [])
            ],
            archived=item["archived"],
            active=item["active"],
        )

    def parse_oracle_config(item: Any) -> OracleCfg:
        return OracleCfg(
            image=item["image"],
            empty_env=item["empty_env"],
            pump_dir_name=item["pump_dir_name"],
            root_db_name=item["root_db_name"],
            plug_db_name=item["plug_db_name"],
            net_listener_port=item["net_listener_port"],
        )

    def parse_postgres_config(item: Any) -> PostgresCfg:
        return PostgresCfg(
            image=item["image"],
            empty_env=item["empty_env"],
            net_listener_port=item["net_listener_port"],
        )

    def parse_shpd_registry(item: Any) -> ShpdRegistryCfg:
        return ShpdRegistryCfg(
            ftp_server=item["ftp_server"],
            ftp_user=item["ftp_user"],
            ftp_psw=item["ftp_psw"],
            ftp_shpd_path=item["ftp_shpd_path"],
            ftp_env_imgs_path=item["ftp_env_imgs_path"],
        )

    def parse_ca_config(item: Any) -> CACfg:
        return CACfg(
            country=item["country"],
            state=item["state"],
            locality=item["locality"],
            organization=item["organization"],
            organizational_unit=item["organizational_unit"],
            common_name=item["common_name"],
            email=item["email"],
            passphrase=item["passphrase"],
        )

    def parse_cert_config(item: Any) -> CertCfg:
        return CertCfg(
            country=item["country"],
            state=item["state"],
            locality=item["locality"],
            organization=item["organization"],
            organizational_unit=item["organizational_unit"],
            common_name=item["common_name"],
            email=item["email"],
            subject_alternative_names=item.get("subject_alternative_names", []),
        )

    def parse_db_default(item: Any) -> DbDefaultCfg:
        return DbDefaultCfg(
            sys_user=item["sys_user"],
            sys_psw=item["sys_psw"],
            user=item["user"],
            psw=item["psw"],
        )

    return Config(
        ora=parse_oracle_config(data["ora"]),
        pg=parse_postgres_config(data["pg"]),
        shpd_registry=parse_shpd_registry(data["shpd_registry"]),
        host_inet_ip=data["host_inet_ip"],
        domain=data["domain"],
        dns_type=data["dns_type"],
        ca=parse_ca_config(data["ca"]),
        cert=parse_cert_config(data["cert"]),
        envs_dir=data["envs_dir"],
        db_default=parse_db_default(data["db_default"]),
        envs=[parse_environment(env) for env in data["envs"]],
    )


class ConfigMng:

    original_placeholders: Dict[str, str] = {}

    def load_user_values(self, file_path: str) -> Dict[str, str]:
        """
        Loads a file holding the user's values in key=value format
        into a dictionary.

        Args:
            file_path (str): Path to the user's values file.

        Returns:
            Dict[str, str]: A dictionary containing the key-value pairs
            from the file.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            ValueError: If the file is improperly formatted.
        """
        user_values: Dict[str, str] = {}

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"The configuration file '{file_path}' does not exist."
            )

        try:
            with open(file_path, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    if "=" in line:
                        key, value = line.split("=", 1)
                        user_values[key.strip()] = value.strip()
                    else:
                        raise ValueError(
                            f"Invalid line format in config file: '{line}'"
                        )
        except Exception as e:
            raise ValueError(f"Error reading configuration file: {e}")

        return user_values

    def substitute_placeholders(
        self, config_data: Dict[Any, Any], values: Dict[str, str]
    ) -> Dict[Any, Any]:
        """
        Recursively replaces placeholders in the given configuration
        dictionary with values from the provided dictionary.

        Placeholders follow the format "${key}". If a placeholder key is
        not found in `values`, it is replaced with `None`.

        :param config_data: The configuration dictionary containing
         placeholders.
        :param values: A dictionary mapping placeholder keys to their values.
        :return: A new dictionary with all placeholders replaced.
        """

        def replace(value: Any, path: str = "") -> Any:
            if (
                isinstance(value, str)
                and value.startswith("${")
                and value.endswith("}")
            ):
                key = value[2:-1]
                if path:
                    self.original_placeholders[path] = value
                return values.get(key, None)

            elif isinstance(value, dict):
                valDict: Dict[Any, Any] = value
                return {
                    k: replace(v, f"{path}.{k}" if path else k)
                    for k, v in valDict.items()
                }
            elif isinstance(value, list):
                valList: List[Any] = value
                return [
                    replace(v, f"{path}[{i}]") for i, v in enumerate(valList)
                ]
            return value

        return replace(config_data)

    def load_config(
        self, file_config_path: str, file_values_path: str
    ) -> Config:
        """
        Loads a JSON configuration file, substitutes placeholders with
        values from another file, and returns a parsed Config object.

        :param file_config_path: Path to the JSON configuration file
                                containing placeholders.
        :param file_values_path: Path to the JSON file with key-value
                                pairs for substitution.
        :return: A Config object with resolved values.
        """
        with open(file_config_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)

        values = self.load_user_values(file_values_path)
        substituted_config = self.substitute_placeholders(config_data, values)

        return parse_config(json.dumps(substituted_config))

    def store_config(self, config: Config, file_output_path: str) -> None:
        """
        Stores the given Config object as a JSON file, replacing known keys
        with placeholders before saving.

        :param config: The Config object to be stored.
        :param file_output_path: Path to save the JSON configuration file.
        """

        def replace_keys_with_placeholders(
            config: Any, parent_key: str = ""
        ) -> Any:
            """
            Recursively traverses the config dictionary, tracking the full
            key path, and replaces values if the key path exists in
            original_placeholders.
            """
            if isinstance(config, dict):
                new_dict: Dict[Any, Any] = {}
                configDict: Dict[Any, Any] = config
                for k, v in configDict.items():
                    full_key = (
                        f"{parent_key}.{k}" if parent_key else k
                    )  # Construct full key path
                    new_dict[k] = (
                        replace_keys_with_placeholders(v, full_key)
                        if isinstance(v, (dict, list))
                        else self.original_placeholders.get(full_key, v)
                    )
                return new_dict
            elif isinstance(config, list):
                configList: List[Any] = config
                return [
                    replace_keys_with_placeholders(item, parent_key)
                    for item in configList
                ]
            else:
                return config

        processed_config = replace_keys_with_placeholders(asdict(config))

        with open(file_output_path, "w", encoding="utf-8") as f:
            json.dump(processed_config, f, indent=2)
