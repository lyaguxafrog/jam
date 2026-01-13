# -*- coding: utf-8 -*-

from typing import Any, Optional, Union

from .__base__ import BaseJWT
from .module import JWT
from .__types__ import KeyLike
from jam.logger import BaseLogger, logger
from jam.encoders import BaseEncoder, JsonEncoder


def create_instance(
    alg: str,
    secret: Optional[KeyLike] = None,
    secret_key: Optional[KeyLike] = None,  # Backward compatibility
    password: Optional[Union[str, bytes]] = None,
    logger: BaseLogger = logger,
    serializer: Union[BaseEncoder, type[BaseEncoder]] = JsonEncoder,
    **kwargs: Any
) -> JWT:
    """Create JWT instance.

    Args:
        alg: Algorithm (HS256, RS256, etc.)
        secret: Secret key (or use secret_key for backward compatibility)
        secret_key: Alias for secret (deprecated, use 'secret')
        password: Password for encrypted keys
        logger: Logger instance
        serializer: JSON encoder/decoder
        **kwargs: Additional params (e.g., custom_module)

    Returns:
        JWT instance or custom module
    """
    # Handle backward compatibility: secret_key -> secret
    if secret is None and secret_key is not None:
        secret = secret_key
    elif secret is None:
        raise ValueError("Either 'secret' or 'secret_key' must be provided")

    if kwargs.get("custom_module"):
        from jam.utils.config_maker import __module_loader__
        module_cls = __module_loader__(kwargs["custom_module"])
        return module_cls(
            alg=alg,
            secret=secret,
            password=password,
            logger=logger,
            serializer=serializer
        )

    return JWT(
        alg=alg,
        secret=secret,
        password=password,
        logger=logger,
        serializer=serializer
    )


__all__ = ["JWT", "BaseJWT", "create_instance"]
