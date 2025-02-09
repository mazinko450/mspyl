
import click
import pyfiglet
from rich import print
from commands import package, project, venv, build

@click.group()
@click.version_option("0.2.0", prog_name="mspyl", message="%(prog)s %(version)s")
@click.help_option("-h", "--help")
def main() -> None:
    ...

# Register command groups
main.add_command(package.install)
main.add_command(package.uninstall)
main.add_command(package.update)
main.add_command(package.list)
main.add_command(venv.venv)
main.add_command(project.create)
main.add_command(project.delete)
main.add_command(build.build)
main.add_command(build.publish)
main.add_command(build.check)

if __name__ == "__main__":
    msg = """
    [bold]Welcome to Mspyl, Mazen Shaikh's Python Launcher
      a Python package manager built for MakeS PYthon development a Lot better

    Type 'mspyl --help' for a list of available commands.

    [bold cyan]Version: 0.2.0
    [bold green]Author: mazinko450
    """
    print(pyfiglet.figlet_format("Mspyl", justify="center"))
    print(msg)
    main()
