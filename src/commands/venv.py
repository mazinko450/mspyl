"""Virtual environment management commands and utilities using UV."""

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Union


import click
from rich import print


class VenvManager:
    """Manages Python virtual environments using UV."""
    
    def __init__(self, python_version: str = "3.8", venv_path: Union[str, Path] = ".venv") -> None:
        """The function initializes a Python virtual environment with specified Python version and virtual
        environment path.
        
        Parameters
        ----------
        python_version : str, optional
            The `python_version` parameter in the `__init__` method is a string parameter with a default value
        of "3.8". It is used to specify the Python version that will be used within the virtual environment
        created by the class.
        venv_path : Union[str, Path], optional
            The `venv_path` parameter in the `__init__` method is used to specify the path where the virtual
        environment will be created. By default, it is set to `".venv"`, which means that if no path is
        provided when initializing an instance of the class, the virtual
        
        """
        self.venv_path = Path(venv_path)
        self.bin_dir: str = "Scripts" if os.name == "nt" else "bin"
        self.python_path: Path = (
            self.venv_path
            / self.bin_dir
            / ("python.exe" if os.name == "nt" else "python3")
        )
        self.uv_path: str = "uv"
        self.activate_script: Path = (
            self.venv_path
            / self.bin_dir
            / ("activate.bat" if os.name == "nt" else "activate")
        )
        self.python_version: str = python_version

    def create(self) -> None:
        """The `create` function initializes a virtual environment using the specified Python version.
        
        """
        try:
            # Initialize the virtual environment
            subprocess.run(
                [sys.executable, "-m", "uv", "venv", str(self.venv_path), "-p", self.python_version],
                check=True,
            )

            print(
                "[bold green]Virtual environment created successfully[/bold green]"
            )
        except subprocess.CalledProcessError as e:
            e.add_note(" Error creating virtual environment ")
            raise e

    def activate(self) -> None:
        """The `activate` function sets up the virtual environment by updating environment variables and
        displaying a message.
        
        """
        try:
            os.environ["VIRTUAL_ENV"] = str(self.venv_path)
            os.environ["PATH"] = os.pathsep.join([
                str(self.venv_path / self.bin_dir),
                os.environ["PATH"],
            ])
            print("[bold green]Virtual environment activated[/bold green]")
        except (KeyError, TypeError) as e:
            e.add_note(" Error activating virtual environment ")
            raise e

    def deactivate(self) -> None:
        """The `deactivate` function in Python deactivates a virtual environment by removing its path from the
        system PATH variable and displaying a message.
        
        """
        
        if "VIRTUAL_ENV" in os.environ:
            old_path = os.environ["PATH"]
            os.environ["PATH"] = os.pathsep.join(
                p
                for p in old_path.split(os.pathsep)
                if not p.startswith(os.environ["VIRTUAL_ENV"])
            )
            del os.environ["VIRTUAL_ENV"]
        print("[bold green]Virtual environment deactivated[/bold green]")

    def add_package(self, packages: str) -> None:
        """The `add_package` function adds packages to dependencies and installs them using UV and pip in
        Python.
        
        Parameters
        ----------
        packages : str
            The `add_package` method takes a string `packages` as input, which represents a list of packages
        separated by spaces. The method then converts this string into a list of package names by splitting
        it at spaces and converting all package names to lowercase.
        
        """
        
        try:
            package_list: List[str] = packages.split()

            # Add & Install packages to dependencies using UV
            cmd: List[str] = [str(self.uv_path), "add", "--compile-bytecode"] + package_list
            subprocess.run(cmd, check=True)

            subprocess.run(cmd, check=True)

            print(
                f"[bold green]Packages {', '.join(package_list)} added successfully[/bold green]"
            )
        except subprocess.CalledProcessError as e:
            e.add_note(" Error adding packages ")
            raise e

    def remove_package(self, packages: str) -> None:
        """The `remove_package` function removes specified packages using UV and displays a success message,
        handling any errors with subprocess.
        
        Parameters
        ----------
        packages : str
            The `remove_package` method takes a string `packages` as input, which represents the names of the
        packages to be removed. The method then converts this string to lowercase and splits it into a list
        of package names. These package names are then used to uninstall the packages using UV (assuming UV
        is
        
        """
        
        try:
            package_list: List[str] = packages.lower().split()

            # Remove package using UV
            subprocess.run(
                [str(self.uv_path), "pip", "uninstall"] + package_list,
                check=True,
            )

            # Remove package from dependencies

            subprocess.run(
                [str(self.uv_path), "remove"] + package_list, check=True
            )

            print(
                f"[bold green]Package {', '.join(package_list)} removed successfully[/bold green]"
            )
        except subprocess.CalledProcessError as e:
            e.add_note(" Error removing package ")
            raise e

    def remove_venv(self) -> None:
        """The `remove_venv` function deactivates the virtual environment and removes its directory.
        
        """
        

        self.deactivate()
        shutil.rmtree(self.venv_path, ignore_errors=True)
        print(
            "[bold green]Virtual environment removed successfully[/bold green]"
        )

    def list_installed_packages(self) -> None:
        """The function `list_installed_packages` lists the installed packages in a virtual environment using
        the `pip freeze` command.
        
        """
        
        try:
            print("\n[bold green]Installed packages:[/bold green]\n")
            subprocess.run(
                [str(self.uv_path), "pip", "freeze"],
                check=True,
            )
        except subprocess.CalledProcessError as e:
            e.add_note(" Error listing installed packages. Please ensure the virtual environment is activated and has pip installed ")
            raise e

    def list_updates(self) -> List[str]:
        """This Python function lists available updates for pip packages using subprocess.
        
        Returns
        -------
            The `list_updates` method returns a list of strings representing the available updates for
        packages. The method first prints a message indicating "Available updates" in bold green style using
        the `console.print` function. It then runs a subprocess command to get a list of outdated packages
        using the `pip list --outdated` command. The output of the command is captured and printed using
        `console.print`, and
        
        """
        
        try:
            print("\n[bold green]Available updates:[/bold green]\n")
            result: subprocess.CompletedProcess[str] = subprocess.run(
                [str(self.uv_path), "pip", "list", "--outdated"],
                capture_output=True,
                text=True,
                check=True,
            )
            print(result.stdout)
            return result.stdout.splitlines()[2:]
        except subprocess.CalledProcessError as e:
            e.add_note(" Error checking updates ")
            raise e

    def list_dependencies(self) -> None:
        """The function `list_dependencies` prints the dependencies tree using the `pip tree` command.
        
        """
        
        try:
            print("\n[bold green]Dependencies tree:[/bold green]\n")
            subprocess.run(
                [str(self.uv_path), "pip", "tree"],
                check=True,
            )
        except subprocess.CalledProcessError as e:
            e.add_note(" Error listing dependencies. Please ensure the virtual environment is activated and has pip installed ")
            raise e

    def update_packages(self, packages: str = "") -> None:
        """The function `update_packages` attempts to upgrade specified packages using pip.
        
        Parameters
        ----------
        packages : str
            The `packages` parameter in the `update_packages` method is a string that represents the packages
        to be updated. If this parameter is provided with a list of package names, those packages will be
        included in the command for upgrading.
        
        """
        try:
            cmd: List[str] = [str(self.uv_path), "pip", "install", "--compile-bytecode", "--upgrade"]
            if packages:
                cmd.extend(packages)

        except subprocess.CalledProcessError as e:
            e.add_note(" Error updating packages. Please ensure the virtual environment is activated and has pip installed ")
            raise e
        
    def update_all_packages(self) -> None:
        """The function `update_all_packages` upgrades all packages listed in the output of `list_updates`
        using pip and prints a success message if any packages were upgraded.
        
        """
        
        try:
            if packages_list := [line.split()[0] for line in self.list_updates()]:
                cmd: List[str] = [str(self.uv_path), "pip", "install", "--compile-bytecode", "--upgrade"] + packages_list
                subprocess.run(cmd, check=True)
                print(
                    "[bold green]Packages upgraded successfully[/bold green]"
                )
            else:
                print("[bold green]No packages to upgrade[/bold green]")



        except subprocess.CalledProcessError as e:
            e.add_note("Error upgrading all packages. Please ensure the virtual environment is activated and has pip installed ")
            raise e


@click.group()
@click.help_option()
def venv() -> None:
    """Virtual environment management commands."""
    pass


@venv.command()
@click.option(
    "-p",
    "--path",
    default=".venv",
    help="Name or path of the virtual environment",
)
@click.option("-py", "--python", type=click.STRING, help="Python interpreter to use")
def create(py: str, path: str) -> None:
    """Create a new virtual environment."""
    vm = VenvManager(py, path)
    vm.create()


@venv.command()
@click.option(
    "-p",
    "--path",
    default=".venv",
    help="Name or path of the virtual environment",
)
def activate(path: str) -> None:
    """Activate a virtual environment."""
    vm = VenvManager(path)
    vm.activate()


@venv.command()
@click.option(
    "-p",
    "--path",
    default=".venv",
    help="Name or path of the virtual environment",
)
def deactivate(path: str) -> None:
    """Deactivate the current virtual environment."""
    vm = VenvManager(path)
    vm.deactivate()


@venv.command()
@click.argument("packages", type=click.STRING, required=True)
@click.option(
    "-p",
    "--path",
    default=".venv",
    help="Name or path of the virtual environment",
)
def add(packages: str, path: str) -> None:
    """Add a package to the virtual environment."""
    vm = VenvManager(path)
    vm.add_package(packages)


@venv.command()
@click.argument(
    "packages",
    type=click.STRING,
    required=False,
    default="",
)
@click.option("--venv", is_flag=True, default=False)
@click.option(
    "-p",
    "--path",
    default=".venv",
    help="Name or path of the virtual environment",
)
def remove(packages: str, venv: bool, path: str) -> None:
    """Remove a package from the virtual environment or the entire virtual environment.
    If no package name is provided, it will ask for confirmation to remove the virtual environment."""
    vm = VenvManager(path)
    if packages:
        vm.remove_package(packages)
    elif venv and click.confirm(
        "Are you sure you want to remove the virtual environment? (y/n)"
    ):
        vm.remove_venv()


@venv.command()
@click.argument("packages", type=click.STRING, required=False)
@click.option("--all", is_flag=True, default=False)
@click.option("-p", "--path", default=".venv", help="Name or path of the virtual environment")
def update(packages: str, all: bool, path: str) -> None:
    """Update the virtual environment."""
    vm = VenvManager(path)
    if all:
        vm.update_all_packages()
    elif packages:
        vm.update_packages(packages=packages)


@venv.command()
@click.option("--packages", is_flag=True, help="List installed modules", default=False)
@click.option("--deps", is_flag=True, help="List virtual environment dependencies", default=False)
@click.option("--outdated", is_flag=True, help="List outdated modules", default=False)
@click.option("--all", is_flag=True, default=False)
@click.option(
    "-p",
    "--path",
    default=".venv",
    help="Name or path of the virtual environment",
)
def list(packages: bool, deps: bool, outdated: bool, all: bool, path: str) -> None:
    """List installed modules, dependencies, or outdated modules in a virtual environment."""
    vm = VenvManager(path)
    if packages:
        vm.list_installed_packages()
    elif deps:
        vm.list_dependencies()
    elif outdated:
        vm.list_updates()
    elif all:
        vm.list_installed_packages()
        vm.list_dependencies()
        vm.list_updates()
        

