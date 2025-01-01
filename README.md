# MSPYL - Mazen Shaikh's Python Launcher

MSPYL is a powerful command-line interface tool that wraps around UV for Python package management, providing a streamlined experience for managing Python environments and packages.

## Features

- 🚀 **Fast Package Management**: Powered by UV for lightning-fast package operations
- 🔄 **Virtual Environment Management**: Create and manage Python virtual environments
- 📦 **Project Dependencies**: Track and manage project dependencies easily
- 🔍 **Package Information**: View installed modules and their details
- 🛠️ **Build & Publish**: Build packages and publish to PyPI
- 🔄 **Git Integration (Coming Soon)**: Basic git operations for version control
- ⚒️ **Compile Python Scripts (Coming Soon)**: Convert Python script to bytecode, .c, .cpp, .exe, .dep, .rpm, and .apk and also compatible with Apple silicon
- ⚡**Optimize Python Scripts (Coming Soon)**: I'm still doing researches

- ⌛ **Time Measurement (Coming Soon)**: Calculate taken time to run python script or to load imported modules
- 🧪 **Testing Features (Coming Soon)**: Offer one command to test compatibility and more
- 📜 **History Management (Coming Soon)**: Can see the history of all commands you use with `mspyl` and can undo it and redo it
- 🤝 **Contributors Managing (Coming Soon)**: Can manage and contact contributors with `team` command

## Installation

```bash
pip install mspyl
```
**Note: It's Very Recommended To Install `mspyl` With UV**

```bash
uv pip install mspyl
```

## Quick Start

**Note: If You Want To Pass Any Option To UV Directly Must Start With * Sign And Replace Spaces With ! Sign Like This:**
```bash
mspyl install *-e!. # Equal to uv pip install -e .
```

### 1. Install Python Packages

**Note: -py Or --python Is Optional**

```bash
# Install a single package (specify Python version)
mspyl install package_name

# Install from requirements.txt
mspyl install *-r!requirements.txt
```

### 2. Uninstall Python Packages
```bash
mspyl uninstall packages
```

### 3. Update Python Packages
```bash
# Update a packages
mspyl update packages

# Update all packages
mspyl update --all
```

### 4. List
```bash
# List python versions & DIRs
mspyl list -py

# List internal packages
mspyl list --internal

# List external packages
mspyl list --external

# List outdated packages
mspyl list --outdated

# List everything
mspyl list --all
```

### 5. Virtual Environment Management

**Note: -p Or --path Is Optional**

```bash
# Create and activate virtual environment
mspyl venv create /path/to/venv

# Add packages to virtual environment
mspyl venv add packages # add single or multiple packages this command install the packages and add it to requirements.txt

# Update packages in virtual environment
mspyl venv update packages

# Update all packages in virtual environment
mspyl venv update --all

# Activate a virtual environment
mspyl venv activate

# Deactivate a virtual environment
mspyl venv deactivate

# Remove a virtual environment
mspyl venv remove --venv

# Remove packages from virtual environment
mspyl venv remove packages

# List installed packages
mspyl venv list --packages

# List dependencies
mspyl venv list --deps

# List outdated packages
mspyl venv list --outdated

# List everything
mspyl venv list --all
```

### 6. Project Management
```bash
# Create a new project
mspyl create /path/to/project

# Delete the entire project
mspyl delete /path/to/project
```

### 7. Build Package
```bash
# Build both sdist and wheel
mspyl build

# Build only sdist
mspyl build --sdist

# Build only wheel
mspyl build --wheel
```

### 8. Publish
```bash
# Publish to PyPI and Test PyPI
mspyl publish --all

# Publish to Test PyPI
mspyl publish --test-pypi

# Publish to PyPI only
mspyl publish --pypi
```


## Dependencies
- UV: For package management operations
- Click: For command-line interface
- Other dependencies

For more information about UV commands, visit the [UV documentation](https://docs.astral.sh/uv/).

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Credits

See [CREDITS](CREDITS) file for a list of dependencies and their licenses.
