#!/usr/bin/env python3
import sys
import os
from datetime import datetime
from PIL import Image, ExifTags

ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

def format_timestamp(ts):
    """Converts a system timestamp to a readable date format."""
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def analyze_image(filepath):
    """Parses an image file for EXIF and basic metadata."""
    print(f"\n{'='*50}")
    print(f"🦂 Analyzing: {filepath}")
    print(f"{'='*50}")

    if not os.path.exists(filepath):
        print("❌ Error: File does not exist.")
        return

    if not filepath.lower().endswith(ALLOWED_EXTENSIONS):
        print(f"⚠️  Warning: Extension not supported by default.")

    try:
        stat = os.stat(filepath)
        print("\n--- SYSTEM METADATA ---")
        print(f"Size:        {stat.st_size} bytes")
        print(f"Creation:    {format_timestamp(stat.st_ctime)} ")
        print(f"Modification:{format_timestamp(stat.st_mtime)}")
    except Exception as e:
        print(f"Error reading system stats: {e}")

    try:
        with Image.open(filepath) as img:
            print("\n--- IMAGE METADATA ---")
            print(f"Format:      {img.format}")
            print(f"Color mode:  {img.mode}")
            print(f"Dimensions:  {img.size[0]}x{img.size[1]} pixels")

            print("\n--- EXIF DATA ---")
            exif_data = img.getexif()
            
            if not exif_data:
                print("No readable EXIF data found in this image.")
            else:
                for tag_id, value in exif_data.items():
                    tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                    
                    if isinstance(value, bytes):
                        if len(value) > 50:
                            value = f"<Binary data of {len(value)} bytes>"
                        else:
                            try:
                                value = value.decode('utf-8', errors='ignore')
                            except:
                                value = "<Unrecognizable binary data>"

                    print(f"{tag_name:25}: {value}")

    except Exception as e:
        print(f"❌ Error processing image with Pillow: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: ./scorpion FILE1 [FILE2 ...]")
        sys.exit(1)

    files = sys.argv[1:]
    for file in files:
        analyze_image(file)

if __name__ == "__main__":
    main()