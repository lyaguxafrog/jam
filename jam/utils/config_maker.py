# -*- coding: utf-8 -*-

import tomllib
from typing import Any, Literal

import yaml

from jam.__logger__ import logger
from jam.exceptions.jwt import EmptyPublicKey, EmptySecretKey, EmtpyPrivateKey
from jam.jwt.lists.__abc_list_repo__ import ABCList


def make_jwt_config(
    alg: Literal[
        "HS256",
        "HS384",
        "HS512",
        "RS256",
        "RS384",
        "RS512",
        # "PS256",
        # "PS384",
        # "PS512",
    ] = "HS256",
    secret_key: str | None = None,
    public_key: str | None = None,
    private_key: str | None = None,
    expire: int = 3600,
    list: ABCList | None = None,
) -> dict[str, Any]:
    """Util for making JWT config.

    Args:
        alg (Literal["HS256", "HS384", "HS512", "RS256", "RS384", "RS512", "PS512", "PS384", "PS512"]): Algorithm for token encryption
        secret_key (str | None): Secret key for HMAC encryption
        private_key (str | None): Private key for RSA encryption
        public_key (str | None): Public key for RSA
        expire (int): Token lifetime in seconds
        list (ABCList | None): List module for checking

    Raises:
        EmptySecretKey: If HS* algorithm is selected, but the secret key is empty
        EmtpyPrivateKey: If RS* algorithm is selected, but the private key is empty
        EmtpyPublicKey: If RS* algorithm is selected, but the public key is empty

    Returns:
        (dict[str, Any]): Dict with config params
    """
    if alg.startswith("HS") and secret_key is None:
        raise EmptySecretKey

    if alg.startswith("RS") and private_key is None:
        raise EmtpyPrivateKey

    if alg.startswith("RS") and public_key is None:
        raise EmptyPublicKey

    logger.debug(
        "Creating JWT config with parameters: \n"
        "{alg: %s, secret_key: %s, private_key: %s, public_key: %s, expire: %d, list: %s}",
        alg,
        secret_key,
        private_key,
        public_key,
        expire,
        list,
    )

    return {
        "alg": alg,
        "secret_key": secret_key,
        "private_key": private_key,
        "public_key": public_key,
        "expire": expire,
        "list": list,
    }


def __yaml_config_parser__(path: str) -> dict[str, Any]:
    """Private method for parsing YML config.

    Args:
        path (str): Path to config.yml

    Raises:
        FileNotFoundError: If file not found
        ValueError: If invalid YML

    Returns:
        (dict[str, Any]): Dict with configs params
    """
    try:
        with open(path) as file:
            config = yaml.safe_load(file)
        return config["jam"] if config else {}
    except FileNotFoundError:
        raise FileNotFoundError(f"YAML config file not found at: {path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file: {e}")


def __toml_config_parser__(path: str = "pyproject.toml") -> dict[str, Any]:
    """Private method for parsing TOML config.

    Args:
        path (str): Path to config.toml

    Raises:
        FileNotFoundError: If file not found
        ValueError: If invalid TOML file

    Returns:
        (dict[str, Any]): Dict with config param
    """
    try:
        with open(path, "rb") as file:
            config = tomllib.load(file)
        return config.get("jam", {}).get("config", {})
    except FileNotFoundError:
        raise FileNotFoundError(f"TOML config file not found at: {path}")
    except tomllib.TOMLDecodeError as e:
        raise ValueError(f"Error parsing TOML file: {e}")
