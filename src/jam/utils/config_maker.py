# -*- coding: utf-8 -*-

import sys
from collections.abc import Callable
from importlib import import_module
from typing import Any, Union


GENERIC_POINTER = "jam"


def __yaml_config_parser__(
    path: str, pointer: str = GENERIC_POINTER
) -> dict[str, Any]:
    """Private method for parsing YML config.

    Args:
        path (str): Path to config.yml
        pointer (str): Pointer to config read

    Raises:
        ImportError: If pyyaml not installed
        FileNotFoundError: If file not found
        ValueError: If invalid YML

    Returns:
        (dict[str, Any]): Dict with configs params
    """
    try:
        import yaml
    except ImportError:
        raise ImportError(
            "To generate a configuration file from YAML/YML, you need to install PyYaml: `pip install pyyaml` or `pip install jamlib[yaml]`"
        )
    try:
        with open(path) as file:
            config = yaml.safe_load(file)
        return config[pointer] if config else {}
    except FileNotFoundError:
        raise FileNotFoundError(f"YAML config file not found at: {path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file: {e}")


def __toml_config_parser__(
    path: str = "pyproject.toml", pointer: str = GENERIC_POINTER
) -> dict[str, Any]:
    """Private method for parsing TOML config.

    Args:
        path (str): Path to config.toml
        pointer (str): Pointer to config read

    Raises:
        FileNotFoundError: If file not found
        ValueError: If invalid TOML file

    Returns:
        (dict[str, Any]): Dict with config param
    """
    if sys.version_info >= (3, 11):
        import tomllib as toml
    else:
        try:
            import toml
        except ImportError:
            raise ImportError(
                "To generate a configuration file from TOML, you need to install toml: "
                "`pip install toml` or `pip install jamlib[toml]`"
            )
    try:
        with open(path, "rb") as file:
            config = toml.load(file)
        return config.get(pointer, {})
    except FileNotFoundError:
        raise FileNotFoundError(f"TOML config file not found at: {path}")
    except toml.TOMLDecodeError as e:
        raise ValueError(f"Error parsing TOML file: {e}")


def __config_maker__(
    config: Union[str, dict[str, Any]], pointer: str = GENERIC_POINTER
) -> dict[str, Any]:
    """Base config masker.

    Args:
        config (Union[str, dict[str, Any]): Config dict or file path
        pointer (str): Pointer to config read

    Returns:
        dict[str, Any]: Parsed config
    """
    if isinstance(config, str):
        if config.split(".")[1] == ("yml" or "yaml"):
            return __yaml_config_parser__(config, pointer).copy()
        elif config.split(".")[1] == "toml":
            return __toml_config_parser__(config, pointer).copy()
        else:
            raise ValueError("YML/YAML or TOML configs only!")
    else:
        return config.copy()


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
