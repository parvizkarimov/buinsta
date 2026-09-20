import os

# Bot token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set. Please set it in Railway.")

# Cookies configuration
# Option 1: cookies.txt file in project root
COOKIES_PATH = os.getenv("COOKIES_PATH", "cookies.txt")

# Option 2: cookies content from environment variable (for Railway deployment)
COOKIES_CONTENT = os.getenv("COOKIES_CONTENT")

# If COOKIES_CONTENT is set, write it to cookies.txt on startup (always update)
if COOKIES_CONTENT:
    with open(COOKIES_PATH, "w", encoding="utf-8") as f:
        f.write(COOKIES_CONTENT.strip() + "\n")

# Download settings
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "downloads")
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB Telegram limit

# Ensure download directory exists
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Supported Instagram domains
SUPPORTED_DOMAINS = [
    "instagram.com",
    "www.instagram.com",
    "instagr.am",
    "www.instagr.am",
]

# Instagram URL patterns
INSTAGRAM_URL_PATTERNS = [
    r"https?://(?:www\.)?instagram\.com/(?:p|reel|reels|stories|tv)/[\w\-]+",
    r"https?://(?:www\.)?instagram\.com/[\w.]+/(?:p|reel|reels|stories|tv)/[\w\-]+",
    r"https?://(?:www\.)?instagr\.am/(?:p|reel|reels|stories|tv)/[\w\-]+",
]

# Default language
DEFAULT_LANG = "uz"
