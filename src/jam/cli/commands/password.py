# -*- coding: utf-8 -*-

import click

from jam.utils import (
    check_password,
    deserialize_hash,
    hash_password,
    serialize_hash,
)


@click.group()
def password() -> None:
    """Password hashing and verification utilities."""
    pass


@password.command()
@click.argument("password")
@click.option("--out", "-o", default=None, help="Output file (default: stdout)")
def hash(password: str, out: str | None) -> None:
    """Hash a password."""
    salt, hash_hex = hash_password(password)
    serialized = serialize_hash(salt, hash_hex)

    if out:
        with open(out, "w") as f:
            f.write(serialized)
        click.echo(f"Password hash written to: {out}")
    else:
        click.echo(serialized)


@password.command()
@click.option(
    "--hash",
    "-h",
    required=True,
    help="Hash to verify against (format: salt$hash)",
)
def verify(hash: str) -> None:
    """Verify a password against a hash."""
    salt_hex, hash_hex = deserialize_hash(hash)

    password = click.prompt("Password", hide_input=True)

    result = check_password(password, salt_hex, hash_hex)
    if result:
        click.echo("✓ Password matches")
    else:
        click.echo("✗ Password does not match")
        raise click.Abort()
