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
    Download Instagram content using yt-dlp.
    Returns a dict with 'filepath', 'title', 'thumbnail' keys on success,
    or raises an exception on failure.
    """
    timestamp = int(time.time())
    output_template = os.path.join(DOWNLOAD_DIR, f"{user_id}_{timestamp}.%(ext)s")

    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": output_template,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "socket_timeout": 30,
        "retries": 3,
        "merge_output_format": "mp4",
    }

    # Add cookies if available
    if os.path.exists(COOKIES_PATH):
        ydl_opts["cookiefile"] = COOKIES_PATH
        logger.info("Using cookies from %s", COOKIES_PATH)

    def _download():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if info is None:
                raise ValueError("Could not extract video info")

            # Find the downloaded file
            filename = ydl.prepare_filename(info)
            # yt-dlp may change the extension
            if not os.path.exists(filename):
                # Try with .mp4 extension
                base = os.path.splitext(filename)[0]
                for ext in [".mp4", ".webm", ".mkv", ".mov"]:
                    candidate = base + ext
                    if os.path.exists(candidate):
                        filename = candidate
                        break

            return {
                "filepath": filename,
                "title": info.get("title", "Instagram Video"),
                "thumbnail": info.get("thumbnail"),
                "duration": info.get("duration"),
                "filesize": os.path.getsize(filename) if os.path.exists(filename) else 0,
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

    filepath = None
    try:
        # Download the content
        result = await download_instagram(url, message.from_user.id)
        filepath = result["filepath"]

        # Check file size
        if result["filesize"] > MAX_FILE_SIZE:
            await status_msg.edit_text(get_message(lang, "error_file_too_large"))
            return

        # Check if file exists
        if not filepath or not os.path.exists(filepath):
            await status_msg.edit_text(get_message(lang, "error_download"))
            return

        # Update status
        await status_msg.edit_text(get_message(lang, "processing"))

        # Send the video
        video = FSInputFile(filepath)
        await message.answer_video(
            video,
            caption=get_message(lang, "success"),
            supports_streaming=True,
        )

        # Delete the status message
        await status_msg.delete()

    except Exception as e:
        logger.error("Download error for URL %s: %s", url, str(e))
        try:
            await status_msg.edit_text(get_message(lang, "error_download"))
        except Exception:
            await message.answer(get_message(lang, "error_download"))

    finally:
        # Cleanup downloaded files
        if filepath:
            cleanup_files(filepath)
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

    # Check cookies status
    if os.path.exists(COOKIES_PATH):
        logger.info("✅ Cookies file found at: %s", COOKIES_PATH)
    else:
        logger.warning(
            "⚠️  No cookies file found at: %s — "
            "Instagram downloads may fail without authentication. "
            "Set COOKIES_CONTENT env var or provide cookies.txt file.",
            COOKIES_PATH,
        )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
