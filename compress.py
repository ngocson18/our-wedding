import os
import sys
import subprocess

try:
    from PIL import Image
except ImportError:
    print("Thư viện Pillow chưa được cài đặt. Đang tự động tải về, vui lòng đợi vài giây...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image

src_dir = 'gallery_goc'
dst_dir = 'images'
max_dimension = 1600

if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)

for filename in os.listdir(src_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        # Convert spaces to hyphens for web-friendly URLs
        safe_filename = filename.replace(' ', '-')
        src_path = os.path.join(src_dir, filename)
        dst_path = os.path.join(dst_dir, safe_filename)
        
        # Check if already compressed
        if os.path.exists(dst_path):
            print(f"Skipping {filename}, already exists as {safe_filename}.")
            continue
            
        try:
            with Image.open(src_path) as img:
                # Calculate new size while maintaining aspect ratio
                width, height = img.size
                if width > max_dimension or height > max_dimension:
                    if width > height:
                        new_width = max_dimension
                        new_height = int(max_dimension * height / width)
                    else:
                        new_height = max_dimension
                        new_width = int(max_dimension * width / height)
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Auto-orient based on EXIF data if present
                try:
                    from PIL import ImageOps
                    img = ImageOps.exif_transpose(img)
                except Exception:
                    pass

                # Convert to RGB if it's RGBA (for saving as JPEG)
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                    
                # Save with compression
                img.save(dst_path, 'JPEG', quality=85, optimize=True)
                
                orig_size = os.path.getsize(src_path) / (1024 * 1024)
                new_size = os.path.getsize(dst_path) / 1024
                print(f"Compressed {filename}: {orig_size:.1f}MB -> {new_size:.1f}KB")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
