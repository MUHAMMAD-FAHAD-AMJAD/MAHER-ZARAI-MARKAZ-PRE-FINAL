#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import subprocess
import platform
import time
from datetime import datetime

def print_header(message):
    """Print a formatted header message"""
    print("\n" + "=" * 80)
    print(f" {message}")
    print("=" * 80)

def clean_build_directories():
    """Remove previous build artifacts"""
    print_header("Cleaning build directories")
    
    directories = ["build", "dist"]
    for directory in directories:
        if os.path.exists(directory):
            print(f"Removing {directory}/")
            try:
                shutil.rmtree(directory)
                print(f"✓ Successfully removed {directory}/")
            except Exception as e:
                print(f"× Error removing {directory}/: {e}")
    
    spec_files = [f for f in os.listdir(".") if f.endswith(".spec")]
    for file in spec_files:
        try:
            print(f"Removing {file}")
            os.remove(file)
            print(f"✓ Successfully removed {file}")
        except Exception as e:
            print(f"× Error removing {file}: {e}")
    
    print("✓ Build directories cleaned.")

def create_version_file():
    """Create a version file with build timestamp"""
    print_header("Creating version file")
    
    version = "1.0.0"
    build_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    os.makedirs("src", exist_ok=True)
    
    with open("src/version.py", "w", encoding="utf-8") as f:
        f.write(f'"""Version information"""\n\n')
        f.write(f'VERSION = "{version}"\n')
        f.write(f'BUILD_DATE = "{build_date}"\n')
    
    print(f"✓ Version file created: {version} ({build_date})")
    return version

def create_placeholder_icon():
    """Create a placeholder icon if one doesn't exist"""
    print_header("Checking for application icon")
    
    icon_path = os.path.abspath(os.path.join("assets", "logo.ico"))
    png_path = os.path.abspath(os.path.join("assets", "logo.png"))
    
    if os.path.exists(icon_path):
        print(f"✓ Icon already exists at {icon_path}")
        return icon_path
    
    print(f"× Icon not found at {icon_path}")
    
    try:
        from PIL import Image, ImageDraw
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(icon_path), exist_ok=True)
        
        if os.path.exists(png_path):
            print(f"Found logo.png, converting to .ico format")
            img = Image.open(png_path)
        else:
            print("Creating a placeholder logo image")
            # Create a simple colored square as placeholder
            img = Image.new('RGB', (256, 256), color=(0, 100, 0))
            d = ImageDraw.Draw(img)
            d.rectangle([50, 50, 206, 206], fill=(255, 255, 255))
            
            # Save PNG version
            img.save(png_path)
            print(f"✓ Created placeholder PNG at {png_path}")
        
        # Convert to ICO (this requires Pillow)
        img = img.resize((64, 64))  # Resize to standard icon size
        img.save(icon_path)
        
        print(f"✓ Created icon at {icon_path}")
        return icon_path
    
    except ImportError:
        print("× PIL (Pillow) is not installed. Cannot create icon.")
        print("  Using default PyInstaller icon instead.")
        return None
    except Exception as e:
        print(f"× Error creating icon: {e}")
        print("  Using default PyInstaller icon instead.")
        return None

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    print_header("Checking for PyInstaller")
    
    try:
        # Try to import PyInstaller
        import PyInstaller
        print(f"✓ PyInstaller is installed (version: {PyInstaller.__version__})")
        return True
    except ImportError:
        print("× PyInstaller is not installed.")
        
        # Ask to install
        response = input("Do you want to install PyInstaller now? (y/n): ")
        if response.lower() == 'y':
            try:
                print("Installing PyInstaller...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
                print("✓ PyInstaller installed successfully.")
                return True
            except Exception as e:
                print(f"× Error installing PyInstaller: {e}")
                return False
        else:
            print("× PyInstaller is required to build the executable.")
            return False

def run_pyinstaller(app_name, icon_path):
    """Run PyInstaller to create the executable"""
    print_header("Building executable with PyInstaller")
    
    # Import required modules
    import os
    
    # Create PyInstaller command
    pyinstaller_args = [
        "pyinstaller",
        "--name", app_name,
        "--onedir",     # Create a directory with the executable and dependencies
        "--windowed",   # No console window (GUI mode)
        "--noconfirm",  # Overwrite output directory without asking
        "--additional-hooks-dir", ".",  # Look for hook files in current directory
    ]
    
    # Add icon if available
    if icon_path and os.path.exists(icon_path):
        pyinstaller_args.extend(["--icon", icon_path])
    
    # Add data files
    data_files = [
        os.path.join("assets", "*"),
        os.path.join("src", "*.py")
    ]
    
    for data in data_files:
        # Use appropriate path separator based on OS
        if os.path.exists(os.path.dirname(data.replace("*", ""))):
            dest_path = os.path.dirname(data)
            pyinstaller_args.extend(["--add-data", f"{data}{os.pathsep}{dest_path}"])
    
    # Add hidden imports
    hidden_imports = [
        "sqlite3",
        "bcrypt",
        "pandas",
        "reportlab",
        "PyQt5",
        "PyQt5.QtCore",
        "PyQt5.QtGui",
        "PyQt5.QtWidgets",
        "pyttsx3.drivers",
        "pyttsx3.drivers.sapi5",
        "win32api",
        "win32com",
        "pythoncom",
        "pywintypes",
        "win32com.shell",
        "win32com.shell.shell",
        "win32ui",
        "win32trace",
        "win32event",
        "win32pdh",
        "pywin32_system32"
    ]
    
    for imp in hidden_imports:
        pyinstaller_args.extend(["--hidden-import", imp])
        
    # Add binary files for pywin32
    import site
    import os
    import sys
    import glob
    
    # Try multiple approaches to locate pywin32 DLLs
    
    # Approach 1: Check site-packages/pywin32_system32
    site_packages = site.getsitepackages()
    dll_found = False
    
    for site_pkg in site_packages:
        pywin32_path = os.path.join(site_pkg, 'pywin32_system32')
        if os.path.exists(pywin32_path):
            for dll in ['pythoncom310.dll', 'pywintypes310.dll']:
                dll_path = os.path.join(pywin32_path, dll)
                if os.path.exists(dll_path):
                    pyinstaller_args.extend(['--add-binary', f'{dll_path}{os.pathsep}.'])
                    print(f"Found DLL at {dll_path}")
                    dll_found = True
    
    # Approach 2: Check in Python's DLLs directory
    if not dll_found:
        python_dll_dir = os.path.join(os.path.dirname(sys.executable), "DLLs")
        if os.path.exists(python_dll_dir):
            for dll in ['pythoncom310.dll', 'pywintypes310.dll']:
                dll_path = os.path.join(python_dll_dir, dll)
                if os.path.exists(dll_path):
                    pyinstaller_args.extend(['--add-binary', f'{dll_path}{os.pathsep}.'])
                    print(f"Found DLL at {dll_path}")
                    dll_found = True
    
    # Approach 3: Check in win32 package directory
    if not dll_found:
        for site_pkg in site_packages:
            win32_path = os.path.join(site_pkg, 'win32')
            if os.path.exists(win32_path):
                dll_paths = glob.glob(os.path.join(win32_path, '*.dll'))
                for dll_path in dll_paths:
                    if os.path.basename(dll_path) in ['pythoncom310.dll', 'pywintypes310.dll']:
                        pyinstaller_args.extend(['--add-binary', f'{dll_path}{os.pathsep}.'])
                        print(f"Found DLL at {dll_path}")
                        dll_found = True
    
    # Approach 4: Search in sys.path
    if not dll_found:
        for path in sys.path:
            if os.path.isdir(path):
                dll_paths = glob.glob(os.path.join(path, '**', '*.dll'), recursive=True)
                for dll_path in dll_paths:
                    if os.path.basename(dll_path) in ['pythoncom310.dll', 'pywintypes310.dll']:
                        pyinstaller_args.extend(['--add-binary', f'{dll_path}{os.pathsep}.'])
                        print(f"Found DLL at {dll_path}")
                        dll_found = True
    
    if not dll_found:
        print("Warning: Could not find PyWin32 DLLs. The executable may not work correctly.")
    
    # Add main script
    pyinstaller_args.append("src/main.py")
    
    print(f"Running PyInstaller with command: {' '.join(pyinstaller_args)}")
    
    try:
        # Run PyInstaller
        subprocess.check_call(pyinstaller_args)
        print("✓ PyInstaller completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"× Error running PyInstaller: {e}")
        return False
    except Exception as e:
        print(f"× Unexpected error: {e}")
        return False

def copy_additional_files(app_name):
    """Copy additional files to the dist directory"""
    print_header("Copying additional files")
    
    # Ensure dist directory exists
    dist_dir = os.path.join("dist", app_name)
    
    if not os.path.exists(dist_dir):
        print(f"× Build directory not found at {dist_dir}")
        return False
    
    try:
        # Create directories in dist
        for directory in ["data", "receipts", "backups"]:
            dir_path = os.path.join(dist_dir, directory)
            os.makedirs(dir_path, exist_ok=True)
            print(f"✓ Created directory: {dir_path}")
        
        # Copy README and license files if they exist
        for file in ["README.md", "LICENSE"]:
            if os.path.exists(file):
                shutil.copy2(file, os.path.join(dist_dir, file))
                print(f"✓ Copied: {file}")
        
        # Create initial database file using the database module
        try:
            sys.path.append("src")
            from database import Database
            
            db_path = os.path.join(dist_dir, "data", "maher_zarai.db")
            db = Database(db_path)
            db.initialize_db()
            print(f"✓ Created initial database at {db_path}")
        except Exception as e:
            print(f"× Warning: Could not create initial database: {e}")
        
        print("✓ Additional files copied.")
        return True
    
    except Exception as e:
        print(f"× Error copying additional files: {e}")
        return False

def create_windows_installer(app_name, version):
    """Create an installer using Inno Setup (Windows only)"""
    if platform.system() != "Windows":
        print("Skipping installer creation (not on Windows).")
        return False
    
    print_header("Creating installer with Inno Setup")
    
    # Check if Inno Setup is installed
    inno_setup_path = r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
    if not os.path.exists(inno_setup_path):
        print("× Inno Setup not found at expected path.")
        print("  To create an installer, please install Inno Setup from:")
        print("  https://jrsoftware.org/isdl.php")
        return False
    
    try:
        # Create installer directory
        os.makedirs("installer", exist_ok=True)
        
        # Create Inno Setup script
        script_path = "installer_script.iss"
        
        with open(script_path, "w") as f:
            f.write(f"""
[Setup]
AppName={app_name}
AppVersion={version}
DefaultDirName={{pf}}\\{app_name}
DefaultGroupName={app_name}
OutputDir=installer
OutputBaseFilename={app_name}_Setup_{version}
Compression=lzma
SolidCompression=yes
SetupIconFile=assets\\logo.ico

[Dirs]
Name: "{{app}}\\data"
Name: "{{app}}\\receipts"
Name: "{{app}}\\backups"

[Files]
Source: "dist\\{app_name}\\*"; DestDir: "{{app}}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{{group}}\\{app_name}"; Filename: "{{app}}\\{app_name}.exe"
Name: "{{commondesktop}}\\{app_name}"; Filename: "{{app}}\\{app_name}.exe"

[Run]
Filename: "{{app}}\\{app_name}.exe"; Description: "Launch {app_name}"; Flags: nowait postinstall skipifsilent
            """)
        
        # Run Inno Setup compiler
        print(f"Running Inno Setup compiler with script: {script_path}")
        subprocess.check_call([inno_setup_path, script_path])
        
        # Get installer path
        installer_path = os.path.join("installer", f"{app_name}_Setup_{version}.exe")
        
        if os.path.exists(installer_path):
            print(f"✓ Installer created successfully at: {installer_path}")
            return True
        else:
            print(f"× Installer not found at expected path: {installer_path}")
            return False
        
    except Exception as e:
        print(f"× Error creating installer: {e}")
        return False

def main():
    """Main build function"""
    start_time = time.time()
    
    print_header("MAHER ZARAI MARKAZ Desktop Application Build")
    
    app_name = "MAHER ZARAI MARKAZ"
    
    # Clean previous build artifacts
    clean_build_directories()
    
    # Create version file
    version = create_version_file()
    
    # Create icon if needed
    icon_path = create_placeholder_icon()
    
    # Check if PyInstaller is installed
    if not check_pyinstaller():
        print("× Build aborted: PyInstaller is not available.")
        return False
    
    # Run PyInstaller
    if not run_pyinstaller(app_name, icon_path):
        print("× Build aborted: PyInstaller failed.")
        return False
    
    # Copy additional files
    if not copy_additional_files(app_name):
        print("× Warning: Failed to copy some additional files.")
    
    # Create installer (Windows only)
    if platform.system() == "Windows":
        if not create_windows_installer(app_name, version):
            print("× Warning: Failed to create installer.")
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print_header("Build completed successfully!")
    print(f"Time taken: {elapsed_time:.2f} seconds")
    print(f"You can find the built application in the dist/{app_name}/ directory.")
    
    if platform.system() == "Windows":
        print(f"Installer (if created) can be found in the installer/ directory.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 