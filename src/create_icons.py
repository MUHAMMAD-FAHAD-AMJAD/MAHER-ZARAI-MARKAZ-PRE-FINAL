import os
from PIL import Image, ImageDraw

def create_checkmark_icon():
    """Create a white checkmark icon for checkboxes"""
    # Create a transparent image
    img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a white checkmark
    checkmark_points = [(3, 8), (7, 12), (13, 4)]
    draw.line(checkmark_points, fill=(255, 255, 255), width=2)
    
    # Ensure assets directory exists
    os.makedirs('assets', exist_ok=True)
    
    # Save the image
    output_path = os.path.join('assets', 'checkmark_white.png')
    img.save(output_path)
    print(f"Checkmark icon created at {output_path}")

def create_theme_icon():
    """Create a theme/palette icon for the settings page"""
    # Create a transparent image
    img = Image.new('RGBA', (24, 24), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a color palette icon
    colors = [
        (22, 197, 94),   # Green
        (59, 130, 246),  # Blue
        (234, 179, 8),   # Yellow
        (30, 41, 59)     # Dark
    ]
    
    # Draw 4 color squares
    square_size = 10
    positions = [(2, 2), (12, 2), (2, 12), (12, 12)]
    
    for (x, y), color in zip(positions, colors):
        draw.rectangle([x, y, x + square_size, y + square_size], fill=color, outline=(255, 255, 255))
    
    # Ensure assets directory exists
    os.makedirs('assets', exist_ok=True)
    
    # Save the image
    output_path = os.path.join('assets', 'theme_icon.png')
    img.save(output_path)
    print(f"Theme icon created at {output_path}")

if __name__ == "__main__":
    create_checkmark_icon()
    create_theme_icon() 