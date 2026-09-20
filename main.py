import os
import re
import time
import asyncio
import logging
from pathlib import Path

import yt_dlp
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import (
    BOT_TOKEN,
    ADMIN_ID,
    COOKIES_PATH,
    DOWNLOAD_DIR,
    MAX_FILE_SIZE,
    INSTAGRAM_URL_PATTERNS,
)
from locales import get_message, LANGUAGE_OPTIONS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Bot and Dispatcher
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# In-memory user language preferences (user_id -> lang_code)
user_languages: dict[int, str] = {}


def get_user_lang(user_id: int) -> str:
    """Get the user's preferred language, defaulting to Uzbek."""
    return user_languages.get(user_id, "uz")


def is_instagram_url(text: str) -> bool:
    """Check if the given text contains a valid Instagram URL."""
    for pattern in INSTAGRAM_URL_PATTERNS:
        if re.search(pattern, text):
            return True
    return False


def extract_instagram_url(text: str) -> str | None:
    """Extract an Instagram URL from text."""
    for pattern in INSTAGRAM_URL_PATTERNS:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    return None


async def download_instagram(url: str, user_id: int) -> dict:
    """
    Download Instagram content (video or photo) using yt-dlp.
    Returns a dict with 'files' (list of tuples: (path, media_type)),
    'title', 'filesize' on success.
    """
    timestamp = int(time.time())
    prefix = f"{user_id}_{timestamp}"
    output_template = os.path.join(DOWNLOAD_DIR, f"{prefix}_%(no)s.%(ext)s")

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": output_template,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "socket_timeout": 30,
        "retries": 5,
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        },
    }

    # Add cookies if available
    if os.path.exists(COOKIES_PATH) and os.path.getsize(COOKIES_PATH) > 0:
        ydl_opts["cookiefile"] = COOKIES_PATH
        logger.info("Using cookies from %s", COOKIES_PATH)

    def _download():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if info is None:
                raise ValueError("Could not extract media info")

            # Look for all downloaded files matching prefix
            downloaded_items = []
            dir_path = Path(DOWNLOAD_DIR)
            found_files = sorted(dir_path.glob(f"{prefix}_*"))

            # Fallback if outtmpl didn't use _%(no)s or single file
            if not found_files:
                found_files = sorted(dir_path.glob(f"{prefix}.*"))

            total_size = 0
            for fpath in found_files:
                fstr = str(fpath)
                ext = fpath.suffix.lower()
                size = os.path.getsize(fstr)
                total_size += size

                if ext in [".mp4", ".mov", ".mkv", ".webm", ".avi"]:
                    downloaded_items.append((fstr, "video"))
                elif ext in [".jpg", ".jpeg", ".png", ".webp"]:
                    downloaded_items.append((fstr, "photo"))

            return {
                "items": downloaded_items,
                "title": info.get("title", "Instagram Post"),
                "filesize": total_size,
            }

    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _download)


def cleanup_files(*filepaths: str) -> None:
    """Remove temporary files."""
    for filepath in filepaths:
        try:
            if filepath and os.path.exists(filepath):
                os.remove(filepath)
                logger.info("Cleaned up: %s", filepath)
        except OSError as e:
            logger.warning("Failed to clean up %s: %s", filepath, e)


# ─── Handlers ────────────────────────────────────────────────


@dp.message(CommandStart())
async def cmd_start(message: Message):
    """Handle /start command."""
    lang = get_user_lang(message.from_user.id)
    await message.answer(get_message(lang, "welcome"))


@dp.message(Command("help"))
async def cmd_help(message: Message):
    """Handle /help command."""
    lang = get_user_lang(message.from_user.id)
    await message.answer(get_message(lang, "help"))


@dp.message(Command("lang"))
async def cmd_lang(message: Message):
    """Handle /lang command — show language selection keyboard."""
    lang = get_user_lang(message.from_user.id)

    builder = InlineKeyboardBuilder()
    for code, name in LANGUAGE_OPTIONS.items():
        builder.button(text=name, callback_data=f"lang:{code}")
    builder.adjust(3)

    await message.answer(
        get_message(lang, "choose_lang"),
        reply_markup=builder.as_markup(),
    )


@dp.callback_query(F.data.startswith("lang:"))
async def callback_lang(callback: CallbackQuery):
    """Handle language selection callback."""
    lang_code = callback.data.split(":")[1]

    if lang_code in LANGUAGE_OPTIONS:
        user_languages[callback.from_user.id] = lang_code
        await callback.message.edit_text(get_message(lang_code, "lang_changed"))
    else:
        await callback.answer("Unknown language")

    await callback.answer()


@dp.message(F.text)
async def handle_text(message: Message):
    """Handle text messages — check for Instagram URLs."""
    lang = get_user_lang(message.from_user.id)

    # Extract Instagram URL from the message
    url = extract_instagram_url(message.text)

    if not url:
        await message.answer(get_message(lang, "error_invalid_url"))
        return

    # Send "downloading" status
    status_msg = await message.answer(get_message(lang, "downloading"))

    downloaded_files = []
    try:
        # Download the content
        result = await download_instagram(url, message.from_user.id)
        items = result.get("items", [])

        if not items:
            await status_msg.edit_text(get_message(lang, "error_download"))
            return

        # Check total file size
        if result["filesize"] > MAX_FILE_SIZE:
            await status_msg.edit_text(get_message(lang, "error_file_too_large"))
            return

        # Update status
        await status_msg.edit_text(get_message(lang, "processing"))

        # Send items (video or photo)
        for filepath, media_type in items:
            downloaded_files.append(filepath)
            media_file = FSInputFile(filepath)

            if media_type == "video":
                await message.answer_video(
                    media_file,
                    caption=get_message(lang, "success"),
                    supports_streaming=True,
                )
            else:
                await message.answer_photo(
                    media_file,
                    caption=get_message(lang, "success"),
                )

        # Delete the status message
        await status_msg.delete()

    except Exception as e:
        logger.error("Download error for URL %s: %s", url, str(e), exc_info=True)
        try:
            await status_msg.edit_text(get_message(lang, "error_download"))
        except Exception:
            await message.answer(get_message(lang, "error_download"))

    finally:
        # Cleanup downloaded files
        for f in downloaded_files:
            cleanup_files(f)
        # Also clean any leftover files for this user in downloads dir
        try:
            for f in Path(DOWNLOAD_DIR).glob(f"{message.from_user.id}_*"):
                cleanup_files(str(f))
        except Exception:
            pass


# ─── Main ────────────────────────────────────────────────────


async def main():
    """Start the bot."""
    logger.info("Bot is starting...")

    cookies_exist = os.path.exists(COOKIES_PATH) and os.path.getsize(COOKIES_PATH) > 0

    # Check cookies status
    if cookies_exist:
        logger.info("✅ Cookies file found at: %s", COOKIES_PATH)
    else:
        logger.warning(
            "⚠️  No cookies file found at: %s — "
            "Instagram downloads may fail without authentication. "
            "Set COOKIES_CONTENT env var or provide cookies.txt file.",
            COOKIES_PATH,
        )

    # Send deploy notification to admin
    if ADMIN_ID:
        try:
            cookies_status = "✅ Faol" if cookies_exist else "⚠️ Cookies o'rnatilmagan"
            msg = (
                "🚀 <b>Bot muvaffaqiyatli ishga tushdi va deploy bo'ldi!</b>\n\n"
                f"🔑 <b>Cookies:</b> {cookies_status}\n"
                f"🕒 <b>Vaqt:</b> {time.strftime('%Y-%m-%d %H:%M:%S')}"
            )
            await bot.send_message(chat_id=int(ADMIN_ID), text=msg)
            logger.info("Admin deploy notification sent to %s", ADMIN_ID)
        except Exception as e:
            logger.warning("Could not send startup message to admin: %s", e)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
