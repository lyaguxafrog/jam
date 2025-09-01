# -*- coding: utf-8 -*-

import tomllib
from collections.abc import Callable
from importlib import import_module
from typing import Any, Union

import yaml


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
        return config.get("jam", {})
    except FileNotFoundError:
        raise FileNotFoundError(f"TOML config file not found at: {path}")
    except tomllib.TOMLDecodeError as e:
        raise ValueError(f"Error parsing TOML file: {e}")


def __config_maker__(config: Union[str, dict[str, Any]]) -> dict[str, Any]:
    """Base config masker.

    Args:
        config (Union[str, dict[str, Any]): Config dict or file path

    Returns:
        dict[str, Any]: Parsed config
    """
    if isinstance(config, str):
        if config.split(".")[1] == ("yml" or "yaml"):
            return __yaml_config_parser__(config)
        elif config.split(".")[1] == "toml":
            return __toml_config_parser__(config)
        else:
            raise ValueError("YML/YAML or TOML configs only!")
    else:
        return config


def __module_loader__(path: str) -> Callable:
    """Loader custom modules from config.

    Args:
        path (str): Path to module. For example: `my_app.classes.SomeClass`

    Raises:
        TypeError: If path not str

    Returns:
        Callable
    """
    if not isinstance(path, str):
        raise TypeError("Path must be a string")
    module_path, class_name = path.rsplit(".", 1)
    module = import_module(module_path)
    return getattr(module, class_name)
