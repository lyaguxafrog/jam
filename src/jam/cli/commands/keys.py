# -*- coding: utf-8 -*-

import click

from jam.utils import (
    generate_aes_key,
    generate_ecdsa_p384_keypair,
    generate_ed25519_keypair,
    generate_rsa_key_pair,
    generate_symmetric_key,
)


@click.group()
def keys() -> None:
    """Generate cryptographic keys."""
    pass


@keys.command()
@click.option(
    "--public-out", "-p", default="public.pem", help="Public key output file"
)
@click.option(
    "--private-out", "-o", default="private.pem", help="Private key output file"
)
def rsa(public_out: str, private_out: str) -> None:
    """Generate RSA key pair."""
    key_pair = generate_rsa_key_pair()

    with open(private_out, "w") as f:
        f.write(key_pair["private"])
    with open(public_out, "w") as f:
        f.write(key_pair["public"])

    click.echo(f"RSA key pair generated: {private_out}, {public_out}")


@keys.command()
@click.option(
    "--public-out", "-p", default="public.pem", help="Public key output file"
)
@click.option(
    "--private-out", "-o", default="private.pem", help="Private key output file"
)
def ed25519(public_out: str, private_out: str) -> None:
    """Generate Ed25519 key pair."""
    key_pair = generate_ed25519_keypair()

    with open(private_out, "w") as f:
        f.write(key_pair["private"])
    with open(public_out, "w") as f:
        f.write(key_pair["public"])

    click.echo(f"Ed25519 key pair generated: {private_out}, {public_out}")


@keys.command()
@click.option(
    "--public-out", "-p", default="public.pem", help="Public key output file"
)
@click.option(
    "--private-out", "-o", default="private.pem", help="Private key output file"
)
def ecdsa(public_out: str, private_out: str) -> None:
    """Generate ECDSA P-384 key pair."""
    key_pair = generate_ecdsa_p384_keypair()

    with open(private_out, "w") as f:
        f.write(key_pair["private"])
    with open(public_out, "w") as f:
        f.write(key_pair["public"])

    click.echo(f"ECDSA P-384 key pair generated: {private_out}, {public_out}")


@keys.command()
@click.option("--out", "-o", default="aes.key", help="AES key output file")
def aes(out: str) -> None:
    """Generate AES key."""
    key = generate_aes_key()

    with open(out, "wb") as f:
        f.write(key)

    click.echo(f"AES key generated: {out}")


@keys.command()
@click.option(
    "--out", "-o", default="symmetric.key", help="Symmetric key output file"
)
@click.option(
    "--bytes", "-b", default=32, help="Key size in bytes (default: 32)"
)
def symmetric(out: str, bytes: int) -> None:
    """Generate symmetric key."""
    key = generate_symmetric_key(bytes)

    with open(out, "w") as f:
        f.write(key)

    click.echo(f"Symmetric key generated: {out} ({bytes} bytes)")
