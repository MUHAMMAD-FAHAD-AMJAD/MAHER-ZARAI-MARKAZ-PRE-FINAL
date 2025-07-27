#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PIL import Image, ImageDraw

def create_voice_icon():
    """Create a simple voice/microphone icon"""
    img = Image.new('RGBA', (200, 200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw microphone body
    draw.rectangle((80, 50, 120, 120), fill=(255, 255, 255))
    draw.ellipse((80, 40, 120, 60), fill=(255, 255, 255))
    
    # Draw microphone stand
    draw.rectangle((90, 120, 110, 150), fill=(255, 255, 255))
    draw.ellipse((70, 150, 130, 170), fill=(255, 255, 255))
    
    # Draw sound waves
    for i in range(3):
        r = 20 + i * 15
        draw.arc((100 - r, 80 - r, 100 + r, 80 + r), 300, 60, fill=(255, 255, 255), width=5)
    
    # Save icon
    os.makedirs('assets', exist_ok=True)
    img.save('assets/voice_icon.png')
    print("Voice icon created successfully")

def create_sale_icon():
    """Create a simple sale/receipt icon"""
    img = Image.new('RGBA', (200, 200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw receipt
    draw.rectangle((60, 40, 140, 160), fill=(255, 255, 255))
    
    # Draw receipt lines
    for i in range(6):
        y = 60 + i * 15
        draw.line((70, y, 130, y), fill=(200, 200, 200), width=2)
    
    # Draw receipt total
    draw.rectangle((70, 140, 130, 150), fill=(240, 240, 240))
    
    # Save icon
    os.makedirs('assets', exist_ok=True)
    img.save('assets/sale_icon.png')
    print("Sale icon created successfully")

def create_logout_icon():
    """Create a simple logout/exit icon"""
    img = Image.new('RGBA', (200, 200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw door
    draw.rectangle((60, 40, 120, 160), fill=(255, 255, 255))
    
    # Draw door handle
    draw.ellipse((100, 90, 115, 105), fill=(200, 200, 200))
    
    # Draw arrow
    points = [(130, 100), (160, 100), (145, 80), (160, 100), (145, 120)]
    draw.line(points, fill=(255, 255, 255), width=5)
    
    # Save icon
    os.makedirs('assets', exist_ok=True)
    img.save('assets/logout_icon.png')
    print("Logout icon created successfully")

if __name__ == "__main__":
    create_voice_icon()
    create_sale_icon()
    create_logout_icon()
    print("All button icons created successfully in the assets directory") 