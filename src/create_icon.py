#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PIL import Image

def create_icon_from_png():
    """Create an icon file from the PNG logo"""
    try:
        # Input and output paths
        png_path = os.path.join('assets', 'logo.png')
        ico_path = os.path.join('assets', 'logo.ico')
        
        if not os.path.exists(png_path):
            print(f"Error: Logo file not found at {png_path}")
            return False
        
        # Open the PNG image
        img = Image.open(png_path)
        
        # Resize to common icon sizes
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        img.save(ico_path, format='ICO', sizes=sizes)
        
        print(f"Icon created successfully at {ico_path}")
        return True
    
    except Exception as e:
        print(f"Error creating icon: {e}")
        return False

if __name__ == "__main__":
    create_icon_from_png() 