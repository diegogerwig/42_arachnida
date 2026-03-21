#!/usr/bin/env python3
import os
import argparse
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

def is_valid_extension(url):
    """Checks if the image URL ends with an allowed extension."""
    return url.lower().split('?')[0].endswith(ALLOWED_EXTENSIONS)

def download_image(img_url, save_path, stats):
    """Downloads an individual image and updates the stats counter."""
    try:
        response = requests.get(img_url, stream=True, timeout=10)
        if response.status_code == 200:
            filename = os.path.basename(urlparse(img_url).path)
            if not filename:
                filename = "unnamed_image"
            
            filepath = os.path.join(save_path, filename)
            
            # Avoid overwriting images with the same name
            base, ext = os.path.splitext(filepath)
            counter = 1
            while os.path.exists(filepath):
                filepath = f"{base}_{counter}{ext}"
                counter += 1

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(1024):
                    if chunk:
                        f.write(chunk)
                        stats['total_bytes'] += len(chunk) # Sumar el tamaño
                        
            print(f"✅ Downloaded: {filepath}")
            stats['downloaded'] += 1
        else:
            stats['failed'] += 1
    except Exception as e:
        print(f"❌ Error downloading {img_url}: {e}")
        stats['failed'] += 1

def scrape_url(url, is_recursive, max_depth, current_depth, save_path, visited_urls, base_domain, stats):
    """Main recursive function to extract images."""
    if current_depth > max_depth or url in visited_urls:
        return
    
    visited_urls.add(url)
    print(f"\n🔍 [{current_depth}/{max_depth}] Scanning: {url}")

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return
    except Exception as e:
        print(f"⚠️  Could not access {url}: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    for img_tag in soup.find_all('img'):
        img_src = img_tag.get('src')
        if img_src:
            img_url = urljoin(url, img_src)
            if is_valid_extension(img_url):
                download_image(img_url, save_path, stats)

    if is_recursive and current_depth < max_depth:
        for a_tag in soup.find_all('a'):
            link = a_tag.get('href')
            if link:
                next_url = urljoin(url, link)
                if urlparse(next_url).netloc == base_domain:
                    next_url = next_url.split('#')[0]
                    scrape_url(next_url, is_recursive, max_depth, current_depth + 1, save_path, visited_urls, base_domain, stats)

def main():
    parser = argparse.ArgumentParser(description="Spider: Web image extractor.")
    parser.add_argument("-r", action="store_true", help="Recursively downloads the images in a URL.")
    parser.add_argument("-l", nargs='?', const=5, default=5, type=int, help="Maximum depth level of the recursive download (default: 5).")
    parser.add_argument("-p", nargs='?', const="./data/", default="./data/", type=str, help="Path where downloaded files will be saved (default: ./data/).")
    parser.add_argument("URL", type=str, help="Base URL to scan.")
    
    args = parser.parse_args()

    if not os.path.exists(args.p):
        os.makedirs(args.p)

    base_domain = urlparse(args.URL).netloc
    visited_urls = set()
    
    stats = {'downloaded': 0, 'failed': 0, 'total_bytes': 0}
    
    print("\n🕸️  Starting Spider...")
    start_time = time.time() 
    
    scrape_url(args.URL, args.r, args.l, 0, args.p, visited_urls, base_domain, stats)
    
    end_time = time.time() 
    
    # Cálculos para el resumen
    elapsed_time = end_time - start_time
    total_mb = stats['total_bytes'] / (1024 * 1024)
    
    # ==========================================
    # FINAL SUMMARY
    # ==========================================
    print("\n" + "═"*50)
    print("📊 SPIDER EXECUTION SUMMARY")
    print("═"*50)
    print(f"⏱️  Time elapsed       : {elapsed_time:.2f} seconds")
    print(f"🔗 Web pages scanned  : {len(visited_urls)}")
    print(f"📁 Destination folder : {args.p}")
    print(f"📥 Images downloaded  : {stats['downloaded']}")
    print(f"💾 Total size         : {total_mb:.2f} MB")
    if stats['failed'] > 0:
        print(f"⚠️  Failed downloads   : {stats['failed']}")
    print("═"*50 + "\n")

if __name__ == "__main__":
    main()