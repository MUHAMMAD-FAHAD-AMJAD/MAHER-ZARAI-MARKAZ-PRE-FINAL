import os
from PIL import Image, ImageDraw

# Create a transparent image
img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Draw a white checkmark
checkmark_points = [(3, 8), (7, 12), (13, 4)]
draw.line(checkmark_points, fill=(255, 255, 255), width=2)

# Save the image to the assets directory
output_path = os.path.join('assets', 'checkmark_white.png')
img.save(output_path)

print(f"Checkmark icon created at {output_path}") 