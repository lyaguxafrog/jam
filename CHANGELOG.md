# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!-- 
## VERSION - [unreleased]

#### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security
-->

## 3.2.0 - [unreleased]

#### Added
- New JOSE module:
  - JWT
  - JWE
  - JWK(s)
  - JWS
- `JamJWTNotYetValid` exception for nbf claim validation
- `check_nbf` parameter in `Jam.jwt_decode()` and `Jam.aio.jwt_decode()`
- `include_headers` parameter in `Jam.jwt_decode()` and `Jam.aio.jwt_decode()`
- `jti` parameter in `Jam.jwt_encode()` and `Jam.aio.jwt_encode()`
- Support for pre-built JWS/JWE instances in JWT constructor
- `JWT.decode()` always returns `{"header": dict, "payload": dict}`

### Changed
- JWT sign-then-encrypt now follows RFC 7519 specification
- Auto-detection of JWE key management algorithm based on key type (RSA→RSA-OAEP, EC→ECDH-ES, symmetric→A*-KW)
- `exp` and `nbf` claims validation moved from JOSE module to `Jam` instances
- `include_headers` parameter added to both sync and async `jwt_decode()`

### Deprecated
- `jam.Jam.jwt_make_payload`: The JWT specification has been introduced, so signing is now done via JWS
- `jam.Jam.jwt_create`: Use `jam.Jam.jwt_encode`
- `jam.jwt.JWT`: Use `jam.jose.JWT`

### Removed

### Fixed
- Fixed typo in CLI documentation (`bahs` → `bash`)

### Security

---

## [3.1.0] - 16-03-2026

### Added
- Add CLI tool for generate keys.

---

## [3.0.0] - 15-03-2026

### Added
- New changelog format.
- JSON configuration.
- New JWT module.
- Environment variable support in config.
- PASETO v1–v4 modules.
- New utilities:
  - Utility for generating symmetric keys
  - Utility for generating ED key pairs

### Changed
- License changed to Apache-2.0.
- Renamed all `__abc_*_module__` to `__base__`.
- Exception format updated.
- Refactored Litestar plugins.
- Refactored Flask extensions.
- Refactored Starlette integrations.
- Renamed `default_ttl` to `ttl` in Redis sessions.

### Removed
- Removed obsolete dependencies.
- Removed module `jam.modules`.
- Removed all deprecated modules.

### Fixed
- YAML config builder.
- Fixed JWT lists in Starlette/FastAPI extensions.
- Fixed all typo errors.

### Security
- Updated all dependencies.

---

- [3.2.0] https://github.com/lyaguxafrog/jam/compare/v3.1.0...unstable
- [3.1.0] https://github.com/lyaguxafrog/jam/compare/v3.0.0...v3.1.0
- [3.0.0] https://github.com/lyaguxafrog/jam/compare/v2.5.6...v3.0.0
