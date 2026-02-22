# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 3.0.0 [Unreleased]

### Added
- New changelog format.
- Json configuration.
- New JWT Module.
- Environment variables support in config.
- PASETO v1-v4 modules.
- New utils:
  - Util for generate symmetric keys
  - Util for generate ED key pairs

### Changed
- Change license to Apache-2.0.
- Rename all `__abc_*_module__` to `__base__`.
- Exception format.

### Deprecated

### Removed
- Deleted old useless dependencies.
- Delete module `jam.modules`.
- Remove all deprecated modules.

### Fixed
- YAML Config builder.
- Fixed JWT lists in starlette/fastapi ext.

### Security
