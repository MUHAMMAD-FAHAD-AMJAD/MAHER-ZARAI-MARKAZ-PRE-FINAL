#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to generate sidebar icons for MAHER ZARAI MARKAZ application
"""

import os
from PIL import Image, ImageDraw

def create_icon(name, color, size=64, output_dir='assets'):
    """Create a simple icon and save it as PNG"""
    # Create a transparent image
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw icon based on name
    if name == 'home':
        # Home icon
        # Roof
        draw.polygon([(size//2, size//5), (size//5, size//2), (4*size//5, size//2)], fill=color)
        # House
        draw.rectangle([size//5, size//2, 4*size//5, 4*size//5], fill=color)
        # Door
        draw.rectangle([2*size//5, 3*size//5, 3*size//5, 4*size//5], fill=(255, 255, 255, 200))
    
    elif name == 'billing':
        # Billing icon (receipt)
        # Paper
        draw.rectangle([size//5, size//6, 4*size//5, 5*size//6], fill=color)
        # Lines
        for i in range(3):
            y = size//3 + i * size//6
            draw.line([(size//3, y), (3*size//4, y)], fill=(255, 255, 255, 200), width=2)
    
    elif name == 'inventory':
        # Inventory icon (boxes)
        # Bottom box
        draw.rectangle([size//5, size//2, 4*size//5, 4*size//5], fill=color)
        # Top box
        draw.rectangle([size//3, size//5, 2*size//3, size//2], fill=color)
    
    elif name == 'customers':
        # Customer icon (person)
        # Head
        draw.ellipse([size//3, size//5, 2*size//3, size//2], fill=color)
        # Body
        draw.polygon([
            (size//3, size//2),
            (2*size//3, size//2),
            (3*size//4, 4*size//5),
            (size//4, 4*size//5)
        ], fill=color)
    
    elif name == 'reports':
        # Reports icon (chart)
        # Paper
        draw.rectangle([size//5, size//6, 4*size//5, 5*size//6], fill=color)
        # Bar chart
        bar_width = size//10
        for i, height in enumerate([size//4, size//3, size//6, size//2]):
            x = size//3 + i * bar_width * 1.5
            y = 4*size//6
            draw.rectangle([x, y - height, x + bar_width, y], fill=(255, 255, 255, 200))
    
    elif name == 'settings':
        # Settings icon (gear)
        # Outer circle
        draw.ellipse([size//4, size//4, 3*size//4, 3*size//4], fill=color)
        # Inner circle
        draw.ellipse([2*size//5, 2*size//5, 3*size//5, 3*size//5], fill=(255, 255, 255, 200))
        # Gear teeth
        for i in range(8):
            angle = i * 45
            x = size//2
            y = size//2
            if angle == 0:
                draw.rectangle([x - size//10, y - 3*size//8, x + size//10, y - size//4], fill=color)
            elif angle == 45:
                draw.polygon([(x + size//4, y - size//4), (x + 3*size//8, y - 3*size//8), (x + size//4, y - size//8)], fill=color)
            elif angle == 90:
                draw.rectangle([x + size//4, y - size//10, x + 3*size//8, y + size//10], fill=color)
            elif angle == 135:
                draw.polygon([(x + size//4, y + size//4), (x + 3*size//8, y + 3*size//8), (x + size//4, y + size//8)], fill=color)
            elif angle == 180:
                draw.rectangle([x - size//10, y + size//4, x + size//10, y + 3*size//8], fill=color)
            elif angle == 225:
                draw.polygon([(x - size//4, y + size//4), (x - 3*size//8, y + 3*size//8), (x - size//4, y + size//8)], fill=color)
            elif angle == 270:
                draw.rectangle([x - 3*size//8, y - size//10, x - size//4, y + size//10], fill=color)
            elif angle == 315:
                draw.polygon([(x - size//4, y - size//4), (x - 3*size//8, y - 3*size//8), (x - size//4, y - size//8)], fill=color)
    
    elif name == 'logout':
        # Logout icon (door with arrow)
        # Door
        draw.rectangle([size//5, size//6, 3*size//5, 5*size//6], fill=color)
        # Arrow
        draw.line([(3*size//5, size//2), (4*size//5, size//2)], fill=color, width=4)
        draw.polygon([
            (3*size//4, size//3),
            (4*size//5, size//2),
            (3*size//4, 2*size//3)
        ], fill=color)
    
    elif name == 'sale':
        # Sale icon (shopping cart)
        # Cart
        draw.rectangle([size//5, size//2, 4*size//5, 3*size//4], fill=color)
        # Wheels
        draw.ellipse([size//4, 3*size//4, size//3, 5*size//6], fill=(255, 255, 255, 200))
        draw.ellipse([2*size//3, 3*size//4, 3*size//4, 5*size//6], fill=(255, 255, 255, 200))
        # Handle
        draw.line([(4*size//5, size//3), (4*size//5, size//2)], fill=color, width=4)
        draw.line([(3*size//5, size//3), (4*size//5, size//3)], fill=color, width=4)
        # Items in cart
        draw.ellipse([size//3, size//3, size//2, size//2], fill=(255, 255, 255, 200))
    
    # Save the image
    os.makedirs(output_dir, exist_ok=True)
    img.save(os.path.join(output_dir, f"{name}_icon.png"))
    print(f"Created {name}_icon.png")

def main():
    """Create all icons"""
    # Create assets directory if it doesn't exist
    os.makedirs('assets', exist_ok=True)
    
    # Define colors
    white = (255, 255, 255, 255)
    green = (27, 94, 32, 255)  # Dark green
    gold = (251, 192, 45, 255)  # Golden yellow
    red = (229, 57, 53, 255)    # Flat red
    
    # Create icons
    create_icon('home', white)
    create_icon('billing', white)
    create_icon('inventory', white)
    create_icon('customers', white)
    create_icon('reports', white)
    create_icon('settings', white)
    create_icon('logout', white)
    create_icon('sale', green)
    
    print("All icons created successfully!")

if __name__ == "__main__":
    main() 