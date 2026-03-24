#!/usr/bin/env python3
import os
import argparse
import requests
import time
import getpass
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

def is_valid_extension(url):
    url_lower = url.lower()
    clean_url = url_lower.split('?')[0]
    is_valid = clean_url.endswith(ALLOWED_EXTENSIONS)
    return is_valid

def download_image(img_url, save_path, stats):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    try:
        response = requests.get(img_url, headers=headers, stream=True, timeout=10)
        
        if response.status_code != 200:
            stats['failed'] += 1
            return None
            
        raw_filename = os.path.basename(urlparse(img_url).path)
        filename = raw_filename or "unnamed_image"
        filepath = os.path.join(save_path, filename)
        
        base_name, extension = os.path.splitext(filepath)
        counter = 1
        while os.path.exists(filepath):
            filepath = f"{base_name}_{counter}{extension}"
            counter += 1

        chunk_size = 1024
        
        with open(filepath, 'wb') as file:
            for chunk in response.iter_content(chunk_size):
                if chunk: 
                    file.write(chunk)
                    stats['total_bytes'] += len(chunk) 
                    
        print(f"✅ Downloaded: {filepath}")
        stats['downloaded'] += 1
        return filepath 
        
    except Exception as e:
        print(f"❌ Error downloading {img_url}: {e}")
        stats['failed'] += 1
        return None

def scrape_url(url, is_recursive, max_depth, current_depth, save_path, visited_urls, base_domain, stats, urls_by_depth, images_by_depth):
    
    url = url.rstrip('/')
    if current_depth > max_depth or url in visited_urls:
        return
    
    visited_urls.add(url)
    print(f"\n🔍 [{current_depth}/{max_depth}] Escaneando: {url}")

    urls_by_depth.setdefault(current_depth, []).append(url)

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code != 200:
            return
            
    except Exception as e:
        print(f"⚠️  No se pudo acceder a {url}: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    for img_tag in soup.find_all('img'):
        img_src = img_tag.get('src')
        
        if not img_src: 
            continue
            
        img_url = urljoin(url, img_src)
        
        if not is_valid_extension(img_url): 
            continue
            
        filepath = download_image(img_url, save_path, stats)
        
        if filepath:
            images_by_depth.setdefault(current_depth, []).append(filepath)

    if is_recursive and current_depth < max_depth:
        for a_tag in soup.find_all('a'):
            link = a_tag.get('href')
            
            if not link: 
                continue
                
            next_url = urljoin(url, link)
            
            next_url = next_url.split('#')[0]
            
            if urlparse(next_url).netloc == base_domain:
                scrape_url(
                    next_url, is_recursive, max_depth, current_depth + 1, 
                    save_path, visited_urls, base_domain, stats, 
                    urls_by_depth, images_by_depth
                )

def resolve_path(raw_path):
    if not raw_path.startswith("~"):
        return os.path.abspath(raw_path)
        
    home_dir = os.path.expanduser("~")
    
    if home_dir == "~":
        user = getpass.getuser() 
        possible_homes = [f"/nfs/homes/{user}", f"/home/{user}", f"/Users/{user}"]
        
        for p in possible_homes:
            if os.path.exists(p):
                home_dir = p
                break
        
        if home_dir == "~":
            home_dir = os.path.abspath(".")
            
    resolved = raw_path.replace("~", home_dir, 1)
    return os.path.abspath(resolved)

def main():
    DEFAULT_PATH = resolve_path("~/Desktop/spyder/")
    
    parser = argparse.ArgumentParser(description="Spider: Web image extractor.")
    parser.add_argument("-r", action="store_true", help="Recursively downloads the images in a URL.")
    parser.add_argument("-l", default=5, type=int, help="Maximum depth level of the recursive download (default: 5).")
    parser.add_argument("-p", default=DEFAULT_PATH, type=str, help=f"Path where downloaded files will be saved (default: {DEFAULT_PATH}).")
    parser.add_argument("URL", type=str, help="Base URL to scan.")
    
    args = parser.parse_args()
    
    save_path = resolve_path(args.p)
    
    try:
        if not os.path.exists(save_path):
            os.makedirs(save_path, exist_ok=True)
    except Exception as e:
        print(f"❌ Error de permisos al crear {save_path}: {e}")
        save_path = os.path.abspath('./spyder_fallback')
        os.makedirs(save_path, exist_ok=True)
        print(f"⚠️  Guardando en directorio alternativo: {save_path}")

    base_domain = urlparse(args.URL).netloc
    visited_urls = set()
    urls_by_depth = {}
    images_by_depth = {}
    stats = {'downloaded': 0, 'failed': 0, 'total_bytes': 0}
    
    print("\n🕷️  Starting Spider...")
    start_time = time.time() 
    
    scrape_url(
        args.URL, args.r, args.l, 0, 
        save_path, visited_urls, base_domain, 
        stats, urls_by_depth, images_by_depth
    )
    
    end_time = time.time() 
    elapsed_time = end_time - start_time
    total_mb = stats['total_bytes'] / (1024 * 1024)
    
    print("\n" + "═"*80)
    print("📊 SPIDER EXECUTION SUMMARY")
    print("═"*80)
    print(f"⏱️  Time elapsed       : {elapsed_time:.2f} seconds")
    print(f"🔗 Web pages scanned  : {len(visited_urls)}")
    print(f"📁 Destination folder : {save_path}")
    print(f"📥 Images downloaded  : {stats['downloaded']}")
    print(f"💾 Total size         : {total_mb:.2f} MB")
    
    if stats['failed'] > 0:
        print(f"⚠️  Failed downloads   : {stats['failed']}")
    
    print("\n" + "─"*80)
    print("📈 INFO BY DEPTH LEVEL")
    print("─"*80)
    
    for depth in range(args.l + 1):
        if depth in urls_by_depth:
            print(f"🔽 LEVEL {depth}")
            print(f"   🔗 Pages scanned ({len(urls_by_depth[depth])}):")
            for u in urls_by_depth[depth]:
                print(f"      - {u}")
                
    print("═"*80 + "\n")

if __name__ == "__main__":
    main()