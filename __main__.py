"""Main CLI entry point for MSPYL."""

import click

from src import package_commands
from src import project_commands
from src import venv_commands
from src import build_commands


@click.group()
@click.version_option("0.1.1", prog_name="mspyl", message="%(prog)s %(version)s")
@click.help_option("-h", "--help")
def main() -> None:
    """MSPYL - Mazen Shaikh's Python Launcher"""
    pass

# Register command groups
main.add_command(package_commands.install)
main.add_command(package_commands.uninstall)
main.add_command(package_commands.update)
main.add_command(package_commands.list)
main.add_command(venv_commands.venv)
main.add_command(project_commands.create)
main.add_command(project_commands.delete)
main.add_command(build_commands.build)
main.add_command(build_commands.publish)
main.add_command(build_commands.check)


if __name__ == "__main__":
    main()
