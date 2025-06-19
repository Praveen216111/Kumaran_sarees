from PIL import Image
import os

input_dir = 'static/images/products'
output_dir = 'static/images/products/resized'
target_size = (300, 400)  # Width x Height

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for filename in os.listdir(input_dir):
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        img_path = os.path.join(input_dir, filename)
        img = Image.open(img_path)
        img = img.resize(target_size, Image.LANCZOS)  # High-quality resizing
        output_path = os.path.join(output_dir, filename)
        img.save(output_path, quality=85)
        print(f"Resized {filename} to {target_size}")