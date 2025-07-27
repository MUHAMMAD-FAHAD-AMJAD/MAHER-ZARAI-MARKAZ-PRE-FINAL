#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import platform
import time

def print_header(message):
    """Print a formatted header message"""
    print("\n" + "=" * 80)
    print(f" {message}")
    print("=" * 80)

def check_python_version():
    """Check if Python version is 3.7 or higher"""
    print_header("Checking Python version")
    
    version_info = sys.version_info
    if version_info.major < 3 or (version_info.major == 3 and version_info.minor < 7):
        print("Error: Python 3.7 or higher is required.")
        print(f"Current Python version: {sys.version}")
        return False
    
    print(f"Python version: {sys.version}")
    print("✓ Python version check passed.")
    return True

def install_package(package_name, version=None):
    """Install a Python package"""
    package_spec = package_name
    if version:
        package_spec += f"=={version}"
    
    try:
        print(f"Installing {package_spec}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_spec])
        print(f"✓ {package_name} installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"× Error installing {package_name}: {e}")
        return False

def install_dependencies():
    """Install required packages from requirements.txt"""
    print_header("Installing dependencies")
    
    # List of core dependencies
    dependencies = [
        # Core dependencies
        ("PyQt5", "5.15.9"),
        ("reportlab", "3.6.12"),
        ("pyttsx3", "2.90"),
        ("Pillow", "9.5.0"),
        ("qrcode", "7.4.2"),
        ("bcrypt", "4.0.1"),
        ("pandas", "2.0.3"),
        ("openpyxl", "3.1.2"),
        
        # Voice recognition dependencies
        ("vosk", "0.3.45"),
        ("sounddevice", "0.4.6"),
        ("numpy", "1.24.3"),
        
        # Packaging dependencies
        ("pyinstaller", "5.13.0")
    ]
    
    # Upgrade pip first
    try:
        print("Upgrading pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("✓ Pip upgraded successfully.")
    except Exception as e:
        print(f"× Warning: Could not upgrade pip: {e}")
    
    # Install each dependency
    success_count = 0
    failure_count = 0
    
    for package, version in dependencies:
        if install_package(package, version):
            success_count += 1
        else:
            failure_count += 1
    
    print(f"\nInstallation complete. Successful: {success_count}, Failed: {failure_count}")
    
    return failure_count == 0

def create_directories():
    """Create required directories if they don't exist"""
    print_header("Creating directories")
    
    directories = ["data", "assets", "assets/vosk_models", "receipts", "backups", "src"]
    
    for directory in directories:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
                print(f"Created directory: {directory}")
            except Exception as e:
                print(f"× Error creating directory {directory}: {e}")
        else:
            print(f"Directory already exists: {directory}")
    
    print("✓ Directory structure verified.")

def check_for_database():
    """Check if database module exists and is importable"""
    print_header("Checking database module")
    
    db_path = os.path.join("src", "database.py")
    
    if not os.path.exists(db_path):
        print(f"× Database module not found at {db_path}")
        print("  Please make sure all source files are present.")
        return False
    
    try:
        sys.path.append("src")
        import database
        print("✓ Database module found and importable.")
        return True
    except ImportError as e:
        print(f"× Error importing database module: {e}")
        return False

def check_for_vosk_models():
    """Check if Vosk models are downloaded"""
    print_header("Checking for Vosk models")
    
    model_dirs = [
        os.path.join("assets", "vosk_models", "vosk-model-small-en-us-0.15"),
        os.path.join("assets", "vosk_models", "vosk-model-small-ur-0.4"),
        os.path.join("assets", "vosk_models", "vosk-model-small-pa-0.4")
    ]
    
    missing_models = []
    
    for model_dir in model_dirs:
        if not os.path.exists(model_dir):
            missing_models.append(model_dir)
    
    if missing_models:
        print("The following Vosk models are missing:")
        for model in missing_models:
            print(f"  - {model}")
        
        print("\nTo enable voice commands, download the models from:")
        print("https://alphacephei.com/vosk/models")
        print("and place them in the assets/vosk_models/ directory.")
        print("\nNote: The application will still work without these models,")
        print("but voice commands will not be available.")
    else:
        print("✓ All Vosk models found.")
    
    # Always return True since Vosk models are optional
    return True

def main():
    """Main installation function"""
    start_time = time.time()
    
    print_header("MAHER ZARAI MARKAZ Desktop Application - Dependency Installation")
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create required directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        print("× Warning: Some dependencies could not be installed.")
        print("  The application may not function correctly.")
    
    # Check for database module
    check_for_database()
    
    # Check for Vosk models
    check_for_vosk_models()
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print_header("Installation completed!")
    print(f"Time taken: {elapsed_time:.2f} seconds")
    print("\nYou can now run the application using:")
    print(f"  {sys.executable} src/main.py")
    print("\nOr build the executable using:")
    print(f"  {sys.executable} build.py")
    
    return True

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1) 