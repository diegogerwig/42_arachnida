#!/usr/bin/env python3
import sys
import os
from datetime import datetime
from PIL import Image, ExifTags

ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

def format_timestamp(ts):
    date_object = datetime.fromtimestamp(ts)
    formatted_string = date_object.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_string

def decode_exif_value(raw_value):
    is_binary_data = isinstance(raw_value, bytes)

    if not is_binary_data:
        return raw_value
        
    data_length = len(raw_value)
    
    if data_length > 50:
        summary_message = f"<Binary data of {data_length} bytes>"
        return summary_message
        
    try:
        decoded_text = raw_value.decode('utf-8', errors='ignore')
        return decoded_text
    except Exception:
        error_message = "<Unrecognizable binary data>"
        return error_message

def analyze_image(filepath):
    
    print(f"\n{'='*80}")
    print(f"🔍 Analyzing: {filepath}")
    print(f"{'='*80}")

    if not os.path.exists(filepath):
        print("❌ Error: File does not exist.")
        return

    filepath_lower = filepath.lower()
    if not filepath_lower.endswith(ALLOWED_EXTENSIONS):
        print(f"❌ Error: Extension not supported by default.")
        return 

    try:
        stat = os.stat(filepath)
        
        creation_time = format_timestamp(stat.st_ctime)
        modification_time = format_timestamp(stat.st_mtime)
        file_size = stat.st_size
        
        print("\n--- SYSTEM METADATA ---")
        print(f"Size:        {file_size} bytes")
        print(f"Creation:    {creation_time} ")
        print(f"Modification:{modification_time}")
    except Exception as e:
        print(f"Error reading system stats: {e}")

    try:
        with Image.open(filepath) as img:
            width = img.size[0]
            height = img.size[1]
            
            print("\n--- IMAGE METADATA ---")
            print(f"Format:      {img.format}")
            print(f"Color mode:  {img.mode}")
            print(f"Dimensions:  {width}x{height} pixels")

            print("\n--- EXIF DATA ---")
            exif_data = img.getexif()
            
            if not exif_data:
                print("No readable EXIF data found in this image.")
                return 

            for tag_id, raw_value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag_id)
                if tag_name is None:
                    tag_name = tag_id
                
                clean_value = decode_exif_value(raw_value)
                
                print(f"{tag_name:25}: {clean_value}")

    except Exception as e:
        print(f"❌ Error processing image with Pillow: {e}")

def main():
    total_arguments = len(sys.argv)
    
    if total_arguments < 2:
        print("Usage: ./scorpion FILE1 [FILE2 ...]")
        sys.exit(1)

    files_to_process = sys.argv[1:]
    
    for file in files_to_process:
        analyze_image(file)

if __name__ == "__main__":
    main()