# -*- coding: utf-8 -*-

from jam.saml.__base__ import BaseSAML
from jam.utils.config_maker import __key_loader__


class SAML(BaseSAML):
    """SAML instance."""

    def __init__(
        self,
        private_key: str,
        public_key: str | None = None,
        certificate: str | None = None,
        default_exp: int | None = None,
    ) -> None:
        """Initialize the SAML instance.

        Args:
            private_key (str): The private key to use for signing.
            public_key (str | None): The public key to use for verifying signatures.
            certificate (str | None): The certificate to use for verifying signatures.
            default_exp (int | None): The default expiration time in seconds.
        """
        self._private_key = __key_loader__(private_key)
        self._public_key = __key_loader__(public_key) if public_key else None
        self._certificate = certificate
        self.default_exp = default_exp
