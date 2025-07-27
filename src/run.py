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

# Add src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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


if __name__ == "__main__":
    # Set up logging
    logger = setup_logging()
    logger.info("Starting application...")

    try:
        # Create directories if they don't exist
        for directory in ["data", "assets", "receipts", "backups"]:
            os.makedirs(directory, exist_ok=True)

        # Create QApplication instance
        app = QApplication(sys.argv)
        app.setAttribute(Qt.AA_EnableHighDpiScaling)
        app.setAttribute(Qt.AA_UseHighDpiPixmaps)

        # Import main after QApplication creation
        from src.main import main

        # Run the application
        logger.info("Initializing main application...")
        exit_code = main()
        logger.info(f"Application exited with code: {exit_code}")
        sys.exit(exit_code)

    except Exception as e:
        logger.exception("Fatal error occurred")
        print(f"Fatal error: {str(e)}")
        sys.exit(1)
