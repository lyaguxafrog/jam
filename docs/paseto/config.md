# Config

## Params

### `version`: `str`
PASETO version.
Jam supports all stable and current versions of PASETO: `v1`, `v2`, `v3`, `v4`

### `purpose`: `str`
The purpose of PASETO. `local` or `public`

### `key`: `str | bytes` 
Key for PASETO.
Symmetric key for `local` PASETO or specific (e.g., RSA) for `public` PASETO.
You can pass the path to the file in the format `path/to/key`.

## TOML Example

### Local
```toml
[jam.paseto]
version = "v4"
purpose = "local"
key = "A9jZODyZ6c9hpuYHTCWxKoELfZ-irM3FxoFe2dBdCAc"
```

### Public
```toml
[jam.paseto]
version = "v4"
public = "public"
key = ".secrets/private.key"  # You can also pass the key as a raw string
```