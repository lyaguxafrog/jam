---
title: JOSE
---

## Overview

JOSE (JSON Object Signing and Encryption) is a set of standards for secure data transmission:

- **JWS** (RFC 7515) - JSON Web Signature - digital signature
- **JWE** (RFC 7516) - JSON Web Encryption - data encryption
- **JWK** (RFC 7517) - JSON Web Key - cryptographic key representation
- **JWT** (RFC 7519) - JSON Web Token - compact token format

Jam provides a complete implementation of all JOSE standards with support for:

- Symmetric (HMAC) and asymmetric (RSA, ECDSA) signing algorithms
- Multiple key management algorithms (RSA, AES Key Wrap, ECDH-ES, PBES2)
- Various content encryption modes (AES-CBC-HS, AES-GCM)
- JWT standard claims validation (exp, nbf)
- Token black/white lists

## Navigation

- [JWT](jwt.md) - high-level token operations
- [JWS](jws.md) - data signing and verification
- [JWE](jwe.md) - data encryption and decryption
- [JWK](jwk.md) - cryptographic keys management
- [Lists](lists.md) - token black and white lists
- [Algorithms](algorithms.md) - supported algorithms reference