from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

os.makedirs('samples', exist_ok=True)

# Sample 1: Geometric & Texture test image 512x512
size = (512, 512)
x = np.linspace(-10, 10, 512)
y = np.linspace(-10, 10, 512)
xx, yy = np.meshgrid(x, y)
r = np.sqrt(xx**2 + yy**2)
pattern1 = (np.sin(r) * 127 + 128).astype(np.uint8)
pattern2 = (np.cos(xx*0.8) * np.sin(yy*0.8) * 127 + 128).astype(np.uint8)
pattern3 = (np.sin(xx*1.5 + yy*1.5) * 127 + 128).astype(np.uint8)
synth_rgb = np.stack([pattern1, pattern2, pattern3], axis=2)
synth_img = Image.fromarray(synth_rgb)
# Add some shapes and text
draw = ImageDraw.Draw(synth_img)
draw.rectangle([60, 60, 452, 452], outline=(255, 255, 200), width=4)
draw.ellipse([150, 150, 362, 362], outline=(100, 240, 255), width=5)
synth_img.save('samples/sample_geometric.png')

# Sample 2: Second sample watermark (Shield copyright badge 32x32)
wm2 = Image.new('RGB', (32, 32), color=(20, 30, 50))
d2 = ImageDraw.Draw(wm2)
d2.polygon([(16, 2), (29, 8), (27, 24), (16, 30), (5, 24), (3, 8)], outline=(0, 240, 255), fill=(10, 100, 180))
d2.ellipse([10, 10, 22, 22], outline=(255, 255, 255), fill=(255, 200, 0))
wm2.save('samples/watermark_badge.png')

# Sample 3: Text watermark "COPYRIGHT ©" 32x32
wm3 = Image.new('RGB', (32, 32), color=(0, 0, 0))
d3 = ImageDraw.Draw(wm3)
d3.ellipse([3, 3, 28, 28], outline=(255, 60, 120), width=2)
d3.rectangle([11, 10, 21, 22], fill=(255, 255, 255))
d3.rectangle([13, 12, 19, 20], fill=(0, 0, 0))
wm3.save('samples/watermark_logo.png')

print("Sample assets generated successfully!")
