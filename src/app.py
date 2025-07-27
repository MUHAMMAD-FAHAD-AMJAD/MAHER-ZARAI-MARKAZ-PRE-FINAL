#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MAHER ZARAI MARKAZ - Agricultural Supply Shop Management System
Main entry point for the application
"""

import os
import sys
import logging
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt


def setup_logging():
    """Set up logging configuration"""
    os.makedirs("data", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(os.path.join("data", "app.log")),
            logging.StreamHandler(),
        ],
    )
    return logging.getLogger("main")


def main():
    """Main application entry point"""
    # Set up logging
    logger = setup_logging()
    logger.info("Starting application...")

    try:
        # Create directories if they don't exist
        for directory in ["data", "assets", "receipts", "backups"]:
            os.makedirs(directory, exist_ok=True)

        # Create QApplication instance
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
        app = QApplication(sys.argv)

        # Import main module
        # Add the parent directory to Python path
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if project_root not in sys.path:
            sys.path.append(project_root)

        from src.main import LoginWindow, MainWindow, Database, APP_NAME

        # Set application properties
        app.setApplicationName(APP_NAME)
        app.setStyle("Fusion")

        # Initialize database
        logger.info("Initializing database...")
        db = Database()

        # Create and show login window
        logger.info("Creating login window...")
        login_window = LoginWindow(db)
        login_window.resize(750, 500)  # Set smaller default size
        login_window.center_on_screen()  # Center the window
        login_window.setWindowState(Qt.WindowActive)
        login_window.show()
        login_window.raise_()
        login_window.activateWindow()

        # Start event loop and wait for login result
        if login_window.exec() == 1:
            logger.info("Login successful")
            user_data = login_window.get_user_data()

            # Create and show main window
            logger.info("Creating main window...")
            main_window = MainWindow(user_data)
            main_window.resize(950, 700)  # Set smaller default size
            main_window.center_on_screen()  # Center the window
            main_window.setWindowState(Qt.WindowActive)
            main_window.show()
            main_window.raise_()
            main_window.activateWindow()

            # Start the main event loop
            return app.exec()
        else:
            logger.info("Login cancelled")
            return 0

    except Exception as e:
        logger.exception("Fatal error occurred")
        print(f"Fatal error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
