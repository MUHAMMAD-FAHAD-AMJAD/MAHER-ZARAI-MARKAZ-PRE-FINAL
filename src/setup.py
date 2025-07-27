#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import shutil
import time
import platform

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
        sys.exit(1)
    
    print(f"Python version: {sys.version}")
    print("✓ Python version check passed.")

def install_dependencies():
    """Install required packages from requirements.txt"""
    print_header("Installing dependencies")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("✓ Pip upgraded successfully.")
        
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

def create_database():
    """Initialize the SQLite database"""
    print_header("Setting up database")
    
    # Import here after dependencies are installed
    try:
        from src.database import Database
        
        db_path = os.path.join("data", "maher_zarai.db")
        if os.path.exists(db_path):
            backup_path = os.path.join("backups", f"maher_zarai_backup_{int(time.time())}.db")
            print(f"Database already exists. Creating backup at {backup_path}")
            shutil.copy2(db_path, backup_path)
        
        db = Database(db_path)
        db.initialize_db()
        print("✓ Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)

def create_directories():
    """Create required directories if they don't exist"""
    print_header("Creating directories")
    
    directories = ["data", "assets", "assets/vosk_models", "receipts", "backups"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
        else:
            print(f"Directory already exists: {directory}")
    
    print("✓ Directory structure verified.")

def check_vosk_models():
    """Check if Vosk models are present and provide download instructions"""
    print_header("Checking Vosk models")
    
    model_paths = {
        "English": os.path.join("assets", "vosk_models", "vosk-model-small-en-us-0.15"),
        "Urdu": os.path.join("assets", "vosk_models", "vosk-model-small-ur-0.4"),
        "Punjabi": os.path.join("assets", "vosk_models", "vosk-model-small-pa-0.4")
    }
    
    missing_models = []
    for language, path in model_paths.items():
        if not os.path.exists(path):
            missing_models.append(language)
    
    if missing_models:
        print("The following Vosk models are missing:")
        for language in missing_models:
            print(f"- {language}")
        
        print("\nTo enable voice commands, download the models from:")
        print("https://alphacephei.com/vosk/models")
        print("and extract them to the assets/vosk_models/ directory.")
    else:
        print("✓ All Vosk models are present.")

def create_shortcut():
    """Create desktop shortcut (Windows only)"""
    if platform.system() != "Windows":
        return
    
    print_header("Creating desktop shortcut")
    
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        path = os.path.join(desktop, "MAHER ZARAI MARKAZ.lnk")
        target = os.path.abspath(os.path.join("src", "main.py"))
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = target
        shortcut.WorkingDirectory = os.path.abspath(".")
        shortcut.IconLocation = os.path.abspath(os.path.join("assets", "logo.png"))
        shortcut.save()
        
        print("✓ Desktop shortcut created.")
    except ImportError:
        print("Skipping shortcut creation. Required packages not installed.")
    except Exception as e:
        print(f"Error creating shortcut: {e}")

def main():
    """Main setup function"""
    print_header("MAHER ZARAI MARKAZ Desktop Application Setup")
    
    check_python_version()
    create_directories()
    install_dependencies()
    create_database()
    check_vosk_models()
    create_shortcut()
    
    print_header("Setup completed successfully!")
    print("You can now run the application using:")
    print(f"  {sys.executable} src/main.py")

if __name__ == "__main__":
    main() 