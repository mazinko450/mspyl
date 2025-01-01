"""Build and publish commands and utilities."""

import subprocess

import click


class BuildManager:

    @staticmethod
    def build(sdist: bool = False, wheel: bool = False) -> None:
        """The `build` function in Python constructs a command list based on specified options and runs it
        using `subprocess.run`.
        
        Parameters
        ----------
        sdist : bool, optional
            The `sdist` parameter in the `build` method is a boolean flag that indicates whether to create a
        source distribution package (`sdist`) during the build process. If `sdist` is set to `True`, the
        method will include the `--sdist` flag in the command that
        wheel : bool, optional
            The `wheel` parameter in the `build` method is a boolean flag that indicates whether to build a
        wheel distribution. If `wheel` is set to `True`, the method will include the `--wheel` flag in the
        command that is executed using `subprocess.run`. This flag specifies that
        
        """
        
        cmd: list[str] = ["uv", "build"]
        if sdist:
            cmd.append("--sdist")
        if wheel:
            cmd.append("--wheel")
        subprocess.run(cmd, check=True)

    @staticmethod
    def check() -> None:
        """The `check` function runs the `uv pip check` command using the `subprocess` module in Python.
        
        """
        
        subprocess.run(["uv", "pip", "check"], check=True)

    @staticmethod
    def publish(
        test_pypi: bool = False, pypi: bool = False, github: bool = False
    ) -> None:
        """The `publish` function in the Python code snippet facilitates publishing packages to TestPyPI, PyPI,
        and GitHub.
        
        Parameters
        ----------
        test_pypi : bool, optional
            The `test_pypi` parameter is a boolean flag that indicates whether the package should be published
        to TestPyPI. If `test_pypi` is set to `True`, the `publish` method will attempt to upload the
        package to TestPyPI using the `uv` tool. If the
        pypi : bool, optional
            The `pypi` parameter in the `publish` method is a boolean flag that determines whether the package
        should be published to the official Python Package Index (PyPI). If `pypi` is set to `True`, the
        method will attempt to upload the package to PyPI using the `uv
        github : bool, optional
            The `github` parameter in the `publish` method is a boolean flag that determines whether the
        package should be published as a GitHub release. However, the current implementation for the
        `github` flag only includes a placeholder message stating that the GitHub release functionality is
        not yet implemented.
        
        Returns
        -------
            The `publish` method returns `None` if an error occurs during the publishing process to TestPyPI or
        PyPI. If the GitHub option is selected, it currently does not have an implementation and simply
        prints a message indicating that the functionality is not yet implemented.
        
        """
        
        if test_pypi:
            # Use uv to upload to TestPyPI
            try:
                subprocess.run(
                    ["uv", "publish", "--repository", "testpypi", "dist/*"],
                    check=True,
                )
            except subprocess.CalledProcessError as e:
                print(f"Error publishing to TestPyPI: {e}")
                return None

        if pypi:
            # Use uv to upload to PyPI
            try:
                subprocess.run(
                    ["uv", "publish", "dist/*"],
                    check=True,
                )
            except subprocess.CalledProcessError as e:
                print(f"Error publishing to PyPI: {e}")
                return None

        if github:
            # Implementation for GitHub release
            print("GitHub release functionality not yet implemented.")
            pass


@click.command()
@click.option(
    "--sdist", is_flag=True, help="Build source distribution", default=False
)
@click.option(
    "--wheel", is_flag=True, help="Build wheel distribution", default=False
)
def build(sdist: bool, wheel: bool) -> None:
    """Build Python package."""
    BuildManager.build(sdist=sdist, wheel=wheel)


@click.command()
def check() -> None:
    """Check Python package"""
    BuildManager.check()

@click.command()
@click.option(
    "--test-pypi", is_flag=True, help="Publish to Test PyPI", default=False
)
@click.option("--pypi", is_flag=True, help="Publish to PyPI", default=False)
@click.option("--all", is_flag=True, help="Publish all", default=False)
def publish(test_pypi: bool, pypi: bool, all: bool) -> None:
    """Publish package."""

    if all:
        pypi = True
        test_pypi = True
    BuildManager.publish(test_pypi=test_pypi, pypi=pypi)

