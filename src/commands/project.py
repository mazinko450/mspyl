"""Project management commands."""

import shutil
from pathlib import Path
import os
import click
import requests
import subprocess

class ProjectManager:
    """Manages Python projects using UV."""

    def __init__(self, project_dir: str) -> None:
        """The function initializes a class instance with attributes related to project and virtual environment
        directories.
        
        Parameters
        ----------
        project_dir : str
            The `project_dir` parameter is a string representing the directory path where the project is
        located.
        
        """
        self.project_dir = Path(project_dir)
        self.venv_dir: Path = self.project_dir / ".venv"
        self.uv_path = f"uv{'.exe' if os.name == 'nt' else ''}"

    def create_project(self, args: str) -> Path:
        """Initialize a new project and set up pyproject.toml.
        Parameters
        ----------
        args : str
            Arguments for project initialization, separated by '!' or spaces.
        Returns
        -------
        Path
            Project directory path.
        """
        # Process arguments more efficiently
        args_list: list[str] = [arg for arg in args.strip('*').replace('!', ' ').split() if arg]

        try:
            # Create new project using UV
            subprocess.run([self.uv_path, "init"] + args_list, 
                         check=True, 
                         capture_output=True)

            # Update pyproject.toml if it doesn't exist
            pyproject_path = self.project_dir / "pyproject.toml"
            if not pyproject_path.exists():
                    TEMPLATE_URL = "https://raw.githubusercontent.com/mazinko450/programming_templates/a17b17c993bf0db6a9b3120daba4d5de4fe836ec/python/python_package_template.toml"

                    with requests.Session() as session:
                        response = session.get(TEMPLATE_URL)
                        response.raise_for_status()  # Check for HTTP errors
                        pyproject_path.write_text(response.text)

        except (subprocess.CalledProcessError, requests.RequestException) as e:
            raise RuntimeError(f"Failed to create project: {str(e)}") from e
        return self.project_dir

    def delete_project(self) -> Path:
        """The `delete_project` function deletes a project directory and all of its contents if it exists.
        
        Returns
        -------
            The `delete_project` method is returning the `project_dir` Path object after attempting to delete
        the project directory and all of its contents using `shutil.rmtree`. If the project directory
        exists, it will be deleted, and the method will return the `project_dir` Path object. If the project
        directory does not exist, the method will still return the `project_dir` Path object.
        
        """
        if self.project_dir.exists():
            # Remove the project directory and all of its contents
            shutil.rmtree(self.project_dir, ignore_errors=True)
            
        return self.project_dir

@click.command()
@click.argument("project_dir", required=False, default=".")
@click.argument("args", type=click.STRING, required=True, nargs=-1)  # Capture any additional arguments
def create(args: str,
           project_dir: str = "."
           ) -> None:
    """Create a new Python project."""
    pm = ProjectManager(project_dir)
    pm.create_project(args)


@click.command()
@click.argument("project_dir", required=False, default=".")
def delete(project_dir: str = ".") -> None:
    """Delete a Python project."""
    pm = ProjectManager(project_dir)
    pm.delete_project()
