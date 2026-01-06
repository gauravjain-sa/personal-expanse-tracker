"""
Build Script for Expense Tracker
Creates a standalone executable using PyInstaller
"""
import subprocess
import sys
import os
from pathlib import Path
import shutil

def clean_build_folders():
    """Remove old build artifacts"""
    print("Cleaning old build artifacts...")
    folders_to_remove = ['build', 'dist']
    for folder in folders_to_remove:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"  Removed {folder}/")

def install_pyinstaller():
    """Ensure PyInstaller is installed"""
    print("Checking PyInstaller installation...")
    try:
        import PyInstaller
        print(f"  PyInstaller {PyInstaller.__version__} is installed")
    except ImportError:
        print("  Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def create_icon():
    """Create a simple icon file if it doesn't exist"""
    icon_path = Path("resources/icon.ico")
    if not icon_path.exists():
        print("\nNote: No icon file found at resources/icon.ico")
        print("The application will use the default Python icon.")
        print("To add a custom icon, place a .ico file at resources/icon.ico")
        return None
    return str(icon_path)

def build_executable():
    """Build the executable using PyInstaller"""
    print("\nBuilding executable with PyInstaller...")

    icon_path = create_icon()

    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--name=ExpenseTracker",
        "--windowed",  # No console window
        "--onedir",  # Create a directory with dependencies
        "--clean",
        "--noconfirm",
    ]

    # Add icon if available
    if icon_path:
        cmd.extend(["--icon", icon_path])

    # Add hidden imports for dependencies that might not be auto-detected
    hidden_imports = [
        "customtkinter",
        "tkcalendar",
        "sqlalchemy",
        "openpyxl",
        "babel.numbers",
        "PIL._tkinter_finder",
    ]

    for imp in hidden_imports:
        cmd.extend(["--hidden-import", imp])

    # Add data files (excluding test files and migration scripts)
    cmd.extend([
        "--add-data", "config.py;.",
        "--add-data", "models;models",
        "--add-data", "services;services",
        "--add-data", "repositories;repositories",
        "--add-data", "ui;ui",
        # Add database files individually to exclude migration scripts
        "--add-data", "database/__init__.py;database",
        "--add-data", "database/connection.py;database",
        "--add-data", "database/init_db.py;database",
        "--add-data", "database/seed_data.py;database",
    ])

    # Exclude test files and migration scripts
    cmd.extend([
        "--exclude-module", "test_excel_workflow",
        "--exclude-module", "pytest",
        "--exclude-module", "unittest",
    ])

    # Main entry point
    cmd.append("main.py")

    print(f"Running: {' '.join(cmd)}")
    subprocess.check_call(cmd)

    print("\n✓ Executable built successfully!")
    print(f"  Output location: {Path('dist/ExpenseTracker').absolute()}")

def create_readme():
    """Create a README file for the distribution"""
    readme_content = """# Expense Tracker

## Installation Instructions

1. Extract all files to a location of your choice (e.g., C:\\Program Files\\ExpenseTracker)
2. Run ExpenseTracker.exe

## First Run

On first run, the application will:
- Create a database in your user folder
- Set up default categories
- Open the main window

## Data Location

Your data is stored in:
%APPDATA%\\ExpenseTracker\\expanse_tracker.db

## Backup Your Data

To backup your financial data:
1. Close the application
2. Copy the file: %APPDATA%\\ExpenseTracker\\expanse_tracker.db
3. Store it safely

To restore:
1. Close the application
2. Replace the database file with your backup

## System Requirements

- Windows 10 or later
- 100 MB free disk space
- 2 GB RAM (minimum)

## Support

For issues or questions, please visit:
https://github.com/yourusername/expanse-tracker/issues

## Version

Version 1.0.0
Built with Python and CustomTkinter
"""

    dist_path = Path("dist/ExpenseTracker")
    if dist_path.exists():
        with open(dist_path / "README.txt", "w") as f:
            f.write(readme_content)
        print("\n✓ Created README.txt in distribution folder")

def main():
    """Main build process"""
    print("=" * 60)
    print("Expense Tracker - Build Script")
    print("=" * 60)

    try:
        # Step 1: Clean old builds
        clean_build_folders()

        # Step 2: Install PyInstaller
        install_pyinstaller()

        # Step 3: Build executable
        build_executable()

        # Step 4: Create README
        create_readme()

        print("\n" + "=" * 60)
        print("BUILD COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"\nYour application is ready in: {Path('dist/ExpenseTracker').absolute()}")
        print("\nNext steps:")
        print("1. Test the application by running dist/ExpenseTracker/ExpenseTracker.exe")
        print("2. Create an installer using Inno Setup (run: iscc installer.iss)")
        print("3. Distribute the installer to users")

    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed with error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
