# Arachnida

Two small cybersecurity tools built for the 42 School curriculum: one scrapes images from websites, the other reads their metadata.

---

## Setup

```bash
bash setup.sh
```

Detects your OS (Linux 42 Campus, WSL, or other), creates a virtual environment in the right place, and installs dependencies. To start fresh:

```bash
bash setup.sh clean
```

Manual setup if you prefer:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## spider.py

Crawls a URL and downloads all images with supported extensions (`.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`).

```
./spider.py [OPTIONS] URL
```

| Flag | Default | Description |
|---|---|---|
| `-r` | — | Recursive crawl |
| `-l DEPTH` | `5` | Max recursion depth |
| `-p PATH` | `~/Desktop/spyder/` | Save directory |

```bash
./spider.py https://example.com
./spider.py -r -l 2 -p ./images https://example.com
```

At the end it prints a summary: time elapsed, pages scanned, images downloaded, total size, failed downloads, and a breakdown of pages visited per depth level.

---

## scorpion.py

Reads one or more image files and prints their metadata.

```
./scorpion.py FILE1 [FILE2 ...]
```

Supported formats: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`

For each file it shows:

- **System metadata** — size, creation and modification timestamps
- **Image metadata** — format, color mode, dimensions
- **EXIF data** — camera info, capture date, GPS, exposure settings, etc. If none is found, it says so.

---

## Dependencies

| Package | Purpose |
|---|---|
| `requests` | HTTP requests |
| `beautifulsoup4` | HTML parsing |
| `Pillow` | Image reading and EXIF extraction |


