#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Startup script for MAHER ZARAI MARKAZ application
This script handles the imports and runs the main.py file
"""

import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Run the main module
from main import main

if __name__ == "__main__":
    sys.exit(main()) 