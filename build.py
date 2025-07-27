import os
import shutil
import PyInstaller.__main__


def build_exe():
    """Build the executable for MAHER ZARAI MARKAZ application."""
    print("Starting build process...")

    # Clean previous build and dist folders
    for folder in ["build", "dist"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)

    # Define PyInstaller arguments
    args = [
        "src/app.py",  # Your main script
        "--name=MAHER ZARAI MARKAZ",  # Name of the executable
        "--onedir",  # Create a directory containing the exe
        "--windowed",  # Use the Windows subsystem executable
        "--icon=assets/logo.ico",  # Application icon
        "--add-data=assets;assets",  # Include assets folder
        "--add-data=data;data",  # Include data folder
        "--hidden-import=PyQt5",
        "--hidden-import=sqlite3",
        "--hidden-import=bcrypt",
        "--hidden-import=datetime",
        "--clean",  # Clean PyInstaller cache
        "--noconfirm",  # Replace output directory without asking
    ]

    print("Building executable...")
    PyInstaller.__main__.run(args)

    print("\nBuild completed!")
    print("You can find the executable in the 'dist/MAHER ZARAI MARKAZ' folder")
    print(
        "\nNote: After making changes to the source code, run this script again to rebuild the executable."
    )


if __name__ == "__main__":
    build_exe()
