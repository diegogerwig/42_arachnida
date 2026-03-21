# 🕷️ Arachnida

A pair of cybersecurity-oriented command-line tools for web image scraping and image metadata analysis, built as part of the **42 School** curriculum.

---

## 📦 Tools

| Tool | Description |
|---|---|
| `spider.py` | Crawls a website and downloads all images found |
| `scorpion.py` | Analyzes image files and displays their EXIF/metadata |

---

## ⚙️ Setup

The project includes an interactive setup script that handles virtual environment creation and dependency installation automatically.

```bash
bash setup.sh
```

The script will:
- Detect your OS (Linux 42 Campus, WSL/Windows, or other)
- Create a Python virtual environment in the appropriate location
- Upgrade `pip` and install all dependencies from `requirements.txt`
- Drop you into an activated shell session

To clean and recreate the environment from scratch:

```bash
bash setup.sh clean
```

> Type `exit` or press `Ctrl+D` to leave the virtual environment shell.

### Manual installation

If you prefer to manage the environment yourself:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 🕸️ spider.py — Web Image Scraper

Crawls a URL and downloads all images with supported extensions (`.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`).

### Usage

```bash
./spider.py [OPTIONS] URL
```

### Options

| Flag | Default | Description |
|---|---|---|
| `-r` | — | Enable recursive crawling of linked pages |
| `-l DEPTH` | `5` | Maximum recursion depth (only with `-r`) |
| `-p PATH` | `~/Desktop/spyder/` | Directory where images will be saved |

### Examples

Download images from a single page (no recursion):

```bash
./spider.py https://example.com
```

Crawl recursively up to 2 levels deep and save to a custom folder:

```bash
./spider.py -r -l 2 -p ./my_images https://example.com
```

Full recursive crawl with default depth (5):

```bash
./spider.py -r https://example.com
```

### Output

At the end of execution, a summary is printed with:

- Total time elapsed
- Number of web pages scanned
- Destination folder path
- Number of images downloaded
- Total size downloaded (MB)
- Failed downloads (if any)
- Breakdown of pages and images by depth level

---

## 🦂 scorpion.py — Image Metadata Analyzer

Reads one or more image files and displays their system-level metadata and EXIF data.

### Usage

```bash
./scorpion.py FILE1 [FILE2 ...]
```

### Supported formats

`.jpg` / `.jpeg`, `.png`, `.gif`, `.bmp`

### Examples

Analyze a single image:

```bash
./scorpion.py photo.jpg
```

Analyze multiple images at once:

```bash
./scorpion.py img1.jpg img2.png img3.gif
```

### Output

For each file, `scorpion` displays three sections:

**System Metadata**
- File size (bytes)
- Creation timestamp
- Last modification timestamp

**Image Metadata**
- Format (JPEG, PNG, etc.)
- Color mode (RGB, RGBA, L, etc.)
- Dimensions (width × height in pixels)

**EXIF Data**
All EXIF tags embedded in the image, such as:
- Camera make and model
- Date and time of capture
- GPS coordinates (if present)
- Exposure settings, focal length, ISO, etc.

> If no EXIF data is found, a message is shown indicating so.

---

## 📁 Project Structure

```
arachnida/
├── spider.py          # Web image scraper
├── scorpion.py        # Image metadata analyzer
├── requirements.txt   # Python dependencies
├── setup.sh           # Environment setup script
└── README.md
```

---

## 🐍 Dependencies

| Package | Version | Purpose |
|---|---|---|
| `requests` | 2.32.5 | HTTP requests for web scraping |
| `beautifulsoup4` | 4.14.3 | HTML parsing |
| `Pillow` | 12.1.1 | Image reading and EXIF extraction |