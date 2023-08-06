#  Copyright (c) 2021, Daniel Mouritzen.

"""Main CLI entry point."""

import click


@click.command()
def main() -> None:
    """Welcome to the TMan CLI!"""  # noqa: D400
    click.echo("TMan")
    click.echo("=" * len("TMan"))
    click.echo("Skeleton project created by Cookiecutter PyPackage")
