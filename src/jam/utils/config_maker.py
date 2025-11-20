# -*- coding: utf-8 -*-

from collections.abc import Callable
from importlib import import_module
import os
import re
import sys
from typing import Any, Union


GENERIC_POINTER = "jam"


def __yaml_config_parser(
    path: str, pointer: str = GENERIC_POINTER
) -> dict[str, Any]:
    """Private method for parsing YML config with env substitution.

    Args:
        path (str): Path to config.yml
        pointer (str): Pointer to config section to read.

    Raises:
        ImportError: If pyyaml not installed
        FileNotFoundError: If file not found
        ValueError: If invalid YAML

    Returns:
        dict[str, Any]: Parsed YAML section with environment variable substitution.
    """
    try:
        import yaml
    except ImportError:
        raise ImportError(
            "To generate a configuration file from YAML/YML, you need to install PyYaml: "
            "`pip install pyyaml` or `pip install jamlib[yaml]`"
        )

    pattern = re.compile(r"\$\{([^}^{]+)\}")

    # FIXME: Refactor
    def _env_constructor(loader, node):
        value = loader.construct_scalar(node)
        for var in pattern.findall(value):
            env_value = os.getenv(var)
            if env_value is None:
                raise ValueError(f"Environment variable '{var}' not set")
            value = value.replace(f"${{{var}}}", env_value)
        return value

    yaml.SafeLoader.add_implicit_resolver("!env", pattern, None)
    yaml.SafeLoader.add_constructor("!env", _env_constructor)

    try:
        with open(path) as file:
            config = yaml.safe_load(file)
        if not config:
            return {}
        return config[pointer] if pointer in config else config
    except FileNotFoundError:
        raise FileNotFoundError(f"YAML config file not found at: {path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file: {e}")


# TODO: env
def __toml_config_parser(
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
            import toml  # type: ignore
        except ImportError:
            raise ImportError(
                "To parse TOML config files, install toml: "
                "`pip install toml` or use Python 3.11+ (built-in tomllib)."
            )

    try:
        with open(path) as file:
            config = toml.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"TOML config file not found at: {path}")
    except Exception as e:
        raise ValueError(f"Error parsing TOML file: {e}") from e

    env_pattern = re.compile(r"\$\{([^}^{]+)\}|\$([A-Za-z_][A-Za-z0-9_]*)")

    def _env_constructor(value: Any) -> Any:
        """Recursively substitute ${VAR} and $VAR in strings."""
        if isinstance(value, str):
            for match in env_pattern.findall(value):
                var_name = match[0] or match[1]
                env_value = os.getenv(var_name)
                if env_value is None:
                    raise ValueError(
                        f"Environment variable '{var_name}' not set"
                    )
                value = re.sub(
                    rf"\$\{{{var_name}\}}|\${var_name}", env_value, value
                )
            return value
        elif isinstance(value, dict):
            return {k: _env_constructor(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [_env_constructor(v) for v in value]
        else:
            return value

    config = _env_constructor(config)

    if pointer:
        section = config
        for part in pointer.split("."):
            if isinstance(section, dict):
                section = section.get(part, {})
            else:
                return {}
        return section
    return config


def __config_maker__(
    config: Union[str, dict[str, Any]], pointer: str = GENERIC_POINTER
) -> dict[str, Any]:
    """Base config masker.

    Args:
        config (str | dict[str, Any): Config dict or file path
        pointer (str): Pointer to config read

    Returns:
        dict[str, Any]: Parsed config
    """
    if isinstance(config, str):
        if config.split(".")[1] == ("yml" or "yaml"):
            return __yaml_config_parser(path=config, pointer=pointer).copy()
        elif config.split(".")[1] == "toml":
            return __toml_config_parser(path=config, pointer=pointer).copy()
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
