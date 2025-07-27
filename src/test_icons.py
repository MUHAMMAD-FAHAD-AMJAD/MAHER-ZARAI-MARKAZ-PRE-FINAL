#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for icon generation
"""

import os
import sys
from create_icons import create_checkmark_icon, create_theme_icon

def main():
    """Main function to test icon generation"""
    print("Testing icon generation...")
    
    # Create assets directory if it doesn't exist
    if not os.path.exists('assets'):
        os.makedirs('assets')
        print("Created assets directory")
    
    # Generate icons
    create_checkmark_icon()
    create_theme_icon()
    
    # Verify icons were created
    checkmark_path = os.path.join('assets', 'checkmark_white.png')
    theme_path = os.path.join('assets', 'theme_icon.png')
    
    if os.path.exists(checkmark_path):
        print(f"✓ Checkmark icon created successfully at {checkmark_path}")
    else:
        print(f"✗ Failed to create checkmark icon at {checkmark_path}")
    
    if os.path.exists(theme_path):
        print(f"✓ Theme icon created successfully at {theme_path}")
    else:
        print(f"✗ Failed to create theme icon at {theme_path}")
    
    print("Icon generation test complete")

if __name__ == "__main__":
    main()