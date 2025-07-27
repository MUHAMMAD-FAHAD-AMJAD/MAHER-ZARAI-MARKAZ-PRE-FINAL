#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def create_splash_screen():
    """Create a beautiful splash screen image"""
    # Create a new image with gradient background
    width, height = 1000, 600  # Larger splash screen
    img = Image.new('RGB', (width, height), color=(0, 100, 0))
    
    # Create gradient from dark green to lighter green
    for y in range(height):
        r = int(0)
        g = int(100 + (y / height) * 50)
        b = int(0)
        for x in range(width):
            img.putpixel((x, y), (r, g, b))
    
    # Add subtle pattern
    draw = ImageDraw.Draw(img)
    for i in range(0, width, 20):
        for j in range(0, height, 20):
            if (i + j) % 40 == 0:
                draw.rectangle([i, j, i+10, j+10], fill=(0, min(g+10, 255), 0))
    
    # Try to add logo if it exists
    try:
        logo_path = os.path.join('assets', 'logo.png')
        if os.path.exists(logo_path):
            logo = Image.open(logo_path)
            logo = logo.resize((200, 200), Image.LANCZOS)
            
            # Create circular mask for logo
            mask = Image.new('L', logo.size, 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse((0, 0, logo.size[0], logo.size[1]), fill=255)
            
            # Apply some glow effect
            mask = mask.filter(ImageFilter.GaussianBlur(5))
            
            # Paste logo with mask
            logo_x = (width - logo.size[0]) // 2
            logo_y = 50
            img.paste(logo, (logo_x, logo_y), mask=logo.split()[3] if 'A' in logo.getbands() else None)
    except Exception as e:
        print(f"Could not add logo to splash: {e}")
    
    # Add a decorative line
    draw.line([(50, height-100), (width-50, height-100)], fill=(255, 255, 255, 128), width=2)
    
    # Save the image
    os.makedirs('assets', exist_ok=True)
    img.save(os.path.join('assets', 'splash.png'))
    print("Splash screen created successfully")

if __name__ == "__main__":
    create_splash_screen()
    print("Splash screen image created in assets directory") 