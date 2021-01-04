"""Command line interface."""

import logging
import sys

import click

log = logging.getLogger(__name__)


@click.group()
@click.version_option()
def cli() -> None:
    # log to sys out
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s",
        level=logging.INFO,
        stream=sys.stdout,
    )


@click.command("generate")
@click.option(
    "--libraries-key",
    "-l",
    required=False,
    type=click.STRING,
    help="Libraries.io API Key (from https://libraries.io/api)",
)
@click.option(
    "--github-key",
    "-g",
    required=False,
    type=click.STRING,
    help="Github API Token (from: https://github.com/settings/tokens)",
)
@click.argument("path", type=click.Path(exists=True))
def generate(path: str, libraries_key: str, github_key: str) -> None:
    """Generates a best-of markdown page from a yaml file."""
    from best_of import generator

    generator.generate_markdown(path, libraries_key, github_key)


cli.add_command(generate)


if __name__ == "__main__":
    cli()
