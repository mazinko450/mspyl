"""Package management commands and utilities using UV."""

import re
import subprocess
import sys
from typing import Any, Callable, List, Optional

import click
from rich import print
from rich.progress import Progress
from rich.table import Table


UV_EXECUTABLE = "uv.exe" if sys.platform == "win32" else " uv"
PIP_COMMAND = "pip"
UPGRADE_FLAG = "--upgrade"
SYSTEM_FLAG = "--system"


def run_command(
    cmd: List[str], check: bool = True, capture_output: bool = True
) -> subprocess.CompletedProcess[str]:
    """Helper function to run uv commands."""
    try:
        result: subprocess.CompletedProcess[str] = subprocess.run(
            cmd, capture_output=capture_output, text=True, check=check
        )
        return result
    except FileNotFoundError as e:
        e.add_note(" or may uv not found. Please ensure it's installed and in your PATH.")
        raise e

    except subprocess.CalledProcessError as e:
        e.add_note(f" Error executing command `{cmd}` ")
        raise e

def get_python_version(path: str) -> Optional[str]:
    """The function `get_python_version` takes a path to a Python executable and returns the version
    information as a string.
    
    Parameters
    ----------
    path : str
        The `path` parameter in the `get_python_version` function is a string that represents the path to
    the Python executable for which you want to retrieve the version information.
    
    Returns
    -------
        the output of the command executed using the `run_command` function, after stripping any leading or
    trailing whitespaces.
    
    """

    if python_version := run_command([path.strip(), "--version"]):
        return python_version.stdout.strip()

def locate_python_version(target_version: str) -> str:
    """The function `locate_python_version` searches for the specified Python version in virtual
    environments and system paths.
    
    Parameters
    ----------
    target_version : str
        The `target_version` parameter in the `locate_python_version` function is a string that represents
    the version of Python you are looking for. This function is designed to locate the paths where the
    specified Python version is installed.
    
    Returns
    -------
        The function `locate_python_version` returns a string that contains the paths where the specified
    Python version is found. If no matching paths are found, it prints a message indicating that no
    Python versions of the specified target version were found.
    
    """

    venv_cmd: List[str] = [
        UV_EXECUTABLE,
        "python",
        "find",
        target_version,
    ]

    python_cmd: List[str] = venv_cmd + [SYSTEM_FLAG]

    venv_paths: subprocess.CompletedProcess[str] = run_command(venv_cmd, check=False)
    python_paths: subprocess.CompletedProcess[str] = run_command(python_cmd, check=False)
    paths: List[str] = (
        venv_paths.stdout.strip().splitlines()
        + python_paths.stdout.strip().splitlines()
    )
    matching_paths: List[str] = []

    matching_paths.extend(iter(paths))
    if not matching_paths:
        print(f"[bold red]No Python {target_version} versions found.[/bold red]")
    return "\n".join(matching_paths)

class PackageManager:
    """Manages Python packages using UV."""

    def __init__(self, python_version: Optional[str] = None) -> None:
        """The function initializes a Python object with an optional version and sets the Python path based on
        the provided version or the system default.
        
        Parameters
        ----------
        python_version : Optional[str]
            The `python_version` parameter in the `__init__` method is used to specify the version of Python
        that the class instance should work with. It is an optional parameter with a default value of
        `None`. If a valid Python version is provided, the class will attempt to locate the corresponding
        Python
        
        """
        self.python_version: Optional[str] = python_version
        self.python_path: str = ""

        version_pattern: re.Pattern[str] = re.compile(r"\d+\.\d+\.?\d?[A-z]?")
        self.match_python_version: Callable[..., Any] = version_pattern.match

        if self.python_version and self.match_python_version(
            self.python_version
        ):
            self.python_path = locate_python_version(self.python_version)
            if not self.python_path:
                print(
                    f"[bold red]Error: Could not locate Python version {self.python_version}.[/bold red]"
                )


    def install(self, args: str) -> None:
        """The `install` function in Python takes a string of arguments, processes them, and then runs a
        command to install packages using uv.
        
        Parameters
        ----------
        args : str
            The `args` parameter in the `install` method is expected to be a string started by `*` and containing a list of
        arguments separated by `!`. The method then processes this string to create a list of arguments
        that will be used in the installation command.
        
        """
        cmd: List[str]

        list_of_args: List[str] = args.strip("*").replace("!", " ").split()

        if self.python_path:
            cmd = [
                self.python_path.strip(),
                "-m",
                "uv",
                PIP_COMMAND,
                "install",
                *list_of_args,
                "--compile-bytecode"
            ]

        else:
            cmd = [
                UV_EXECUTABLE,
                PIP_COMMAND,
                "install",
                *list_of_args,
                SYSTEM_FLAG,
                "--compile-bytecode"
            ]

        if result := run_command(cmd):
            print(result.stdout)
            print(
                "[bold green]Packages installed successfully.[/bold green]"
            )

    def uninstall(self, args: str) -> None:
        """The `uninstall` function takes a string of arguments, processes them, constructs a command to
        uninstall packages using uv, and then runs the command, displaying a success message if the
        uninstallation is successful.
        
        Parameters
        ----------
        args : str
            The `args` parameter in the `uninstall` method is expected to be a string containing the arguments
        for uninstalling a package or packages. The method processes this string to extract the individual
        arguments needed for the uninstall command. The arguments are then used to construct a command that
        will be executed to uninstall
        
        """

        cmd: List[str]

        list_of_args: List[str] = args.strip("*").replace("!", " ").split()

        if self.python_path:
            cmd = [
                self.python_path,
                "-m",
                "uv",
                PIP_COMMAND,
                "uninstall",
                *list_of_args,
            ]

        else:
            cmd = [
                UV_EXECUTABLE,
                PIP_COMMAND,
                "uninstall",
                *list_of_args,
                SYSTEM_FLAG,
            ]

        if _ := run_command(cmd):
            print(
                "[bold green]Packages uninstalled successfully.[/bold green]"
            )

    def update(self, package_name: str) -> None:
        """Updates a package using UV.

        Args:
            package_name: The name of the package to update.
        """
        cmd: List[str]
        if self.python_path:
            cmd = [
                self.python_path.strip(),
                "-m",
                "uv",
                PIP_COMMAND,
                "install",
                package_name,
                UPGRADE_FLAG,
            ]
        else:
            cmd = [
                UV_EXECUTABLE,
                PIP_COMMAND,
                "install",
                package_name,
                UPGRADE_FLAG,
                SYSTEM_FLAG,
            ]
        if _ := run_command(cmd):
            print(
                f"[bold green]Package '{package_name}' updated successfully.[/bold green]"
            )

    def update_all(self) -> None:
        """The `update_all` function updates all Python packages listed in the requirements file using pip,
        displaying progress and handling errors.
        
        Returns
        -------
            The `update_all` method returns `None` if the `run_command` function does not return a result.
        
        """
        
        result: subprocess.CompletedProcess[str] = run_command([
            UV_EXECUTABLE,
            PIP_COMMAND,
            "freeze",
            SYSTEM_FLAG
        ])
        if not result:
            return None
        packages: List[str] = [
            line.split("==")[0] for line in result.stdout.strip().splitlines()
        ]

        with Progress() as progress:
            task = progress.add_task("Updating packages", total=len(packages))

            cmd: List[str]
            for package in packages:
                if self.python_path:
                    cmd = [
                        self.python_path.strip(),
                        "-m",
                        "uv",
                        PIP_COMMAND,
                        "install",
                        package,
                        UPGRADE_FLAG,
                    ]
                else:
                    cmd = [
                        UV_EXECUTABLE,
                        PIP_COMMAND,
                        "install",
                        package,
                        UPGRADE_FLAG,
                        SYSTEM_FLAG,
                    ]
                result = run_command(cmd, check=False)
                if result and result.returncode != 0:
                    print(
                        f"[bold red]Error updating {package}:[/bold red] {result.stderr}"
                    )
                progress.update(task, advance=1)
        print(
            "[bold green]All packages updated successfully.[/bold green]"
        )

    @staticmethod
    def check_updates(package_name: Optional[str] = None) -> None:
        """This function checks for outdated packages and displays the information in a table format.
        
        Parameters
        ----------
        package_name : Optional[str]
            The `package_name` parameter in the `check_updates` method is an optional parameter that specifies
        the name of a specific package for which you want to check updates. If provided, the method will
        only check for updates for the specified package. If not provided, the method will check for updates
        for all
        
        """
        cmd: List[str] = [
            UV_EXECUTABLE,
            PIP_COMMAND,
            "list",
            "--outdated",
            SYSTEM_FLAG,
        ]
        if package_name:
            cmd.append(package_name)
        if result := run_command(cmd):
            if result.stdout:
                table = Table(title="Outdated Packages")
                table.add_column("Package", style="cyan", no_wrap=True)
                table.add_column("Current Version", style="magenta")
                table.add_column("Latest Version", style="green")
                for line in result.stdout.strip().splitlines()[2:]:
                    parts: List[str] = line.split()
                    if len(parts) == 3:
                        table.add_row(parts[0], parts[1], parts[2])
                print(table)
            else:
                print("\n[yellow]No outdated packages found.[/yellow]\n")

    @staticmethod
    def list_python_versions() -> None:
        """The `list_python_versions` function retrieves and displays information about Python versions
        installed on the system.
        
        """

        if sys.platform == "win32":
            cmd = ["where.exe", "python"]
        else:
            cmd = ["which", "-a", "python3"]
            
        result: subprocess.CompletedProcess[str] = run_command(cmd)

        table = Table(title="Python Versions")
        table.add_column("Version", style="cyan", no_wrap=True)
        table.add_column("Path", style="magenta")
        if result:
            for path in result.stdout.strip().splitlines():
                version: Optional[str] = get_python_version(path)
                if "venv" in path:
                    table.add_row(f"venv{version.strip('Python'):>9}", path)
                else:
                    table.add_row(version, path)
        print(table)

    @staticmethod
    def list_external_modules() -> None:
        """The function `list_external_modules` lists external Python modules along with their versions and
        locations.
        
        """
        
        if not (
            _ := run_command([UV_EXECUTABLE, PIP_COMMAND, "list", SYSTEM_FLAG])
        ):
            return
        if _.stdout:
            table = Table(title="External Modules")
            table.add_column("Package", style="cyan", no_wrap=True)
            table.add_column("Version", style="magenta")
            table.add_column("Location", style="green")
            for line in _.stdout.strip().splitlines()[2:]:
                parts: List[str] = line.split()
                table.add_row(*parts)
            print(table)
        else:
            print("No external modules found.")

    @staticmethod
    def list_internal_modules() -> None:
        """The function `list_internal_modules` lists internal modules in Python that do not contain
        underscores in their names.
        
        """

        table = Table(title="Internal Modules")
        table.add_column("Module", style="cyan", no_wrap=True)
        for module in sys.builtin_module_names:
            if "_" not in module:
                table.add_row(module)
        print(table)


@click.command()
@click.argument("args", type=click.STRING)
@click.option(
    "-py", "--python", type=click.STRING, help="Python version to use", required=False
)
def install(args: str, python: Optional[str]) -> None:
    """Install a Python package.
    Note: Anything after install command must start with * sign and replace spaces with ! sign
    """
    pm = PackageManager(python_version=python)
    if args[0] == "*":
        pm.install(args=args)
    else:
        print(
            "[bold red]Error: Anything after install command must start with * sign and replace spaces with ! sign[/bold red]"
        )


@click.command()
@click.argument("args", type=click.STRING)
@click.option(
    "-py", "--python", type=click.STRING, help="Python version to use", required=False
)
def uninstall(args: str, python: Optional[str]) -> None:
    """Uninstall a Python package."""
    pm = PackageManager(python_version=python)
    pm.uninstall(args)


@click.command()
@click.argument("package_name", required=False)
@click.option(
    "-py", "--python", type=click.STRING, help="Python version to use", required=False
)
@click.option("--all", is_flag=True, help="Update all packages", default=False)
def update(package_name: str, python: Optional[str], all: bool) -> None:
    """Update packages or Python version."""
    pm = PackageManager(python_version=python)
    if package_name:
        pm.update(package_name)
    elif all:
        pm.update_all()
    else:
        print(
            "[bold red]Please specify a package name or use --all to update all packages.[/bold red]"
        )


@click.command()
@click.option(
    "-py", "--python", is_flag=True, help="List DIRs of Python versions", default=False
)
@click.option(
    "--internal", is_flag=True, help="List built-in modules", default=False
)
@click.option(
    "--external", is_flag=True, help="List external modules", default=False
)
@click.option(
    "--outdated", is_flag=True, help="List outdated modules", default=False
)
@click.option("--all", is_flag=True, help="List all", default=False)
def list(
    python: bool = False,
    internal: bool = False,
    external: bool = False,
    outdated: bool = False,
    all: bool = False,
) -> None:
    """Lists Python versions, internal modules, external modules, outdated modules or all."""
    if not any([python, internal, external, outdated, all]):
        print(
            "[bold red]Please specify at least one option: --python, --internal, --external, --outdated, or --all[/bold red]"
        )
        return None

    if python:
        PackageManager.list_python_versions()
    if internal:
        PackageManager.list_internal_modules()
    if external:
        PackageManager.list_external_modules()
    if outdated:
        PackageManager.check_updates()
    if all:
        PackageManager.list_python_versions()
        PackageManager.list_internal_modules()
        PackageManager.list_external_modules()
        PackageManager.check_updates()
