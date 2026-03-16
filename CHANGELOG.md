# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!-- 
## VERSION

#### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security
-->

## [3.1.0] - unreleased

### Added
- Add CLI tool for generate keys.

### Changed

### Deprecated

### Removed

### Fixed

### Security

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
[3.0.0] https://github.com/lyaguxafrog/jam/compare/v2.5.6...v3.0.0
