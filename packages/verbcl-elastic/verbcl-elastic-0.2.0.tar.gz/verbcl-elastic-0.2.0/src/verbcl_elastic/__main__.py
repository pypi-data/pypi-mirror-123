"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """VerbCL Elastic."""  # noqa: D403


if __name__ == "__main__":
    main(prog_name="verbcl-elastic")  # pragma: no cover
