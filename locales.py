"""
Localization module — O'zbek, Rus, Ingliz tillarida xabarlar.
"""

MESSAGES = {
    "uz": {
        "welcome": (
            "🎬 <b>Assalomu alaykum!</b>\n\n"
            "Men Instagram video, reels va story'larni yuklab beruvchi botman.\n\n"
            "📎 Menga Instagram havolasini yuboring va men sizga videoni yuklab beraman!\n\n"
            "🌐 Tilni o'zgartirish: /lang\n"
            "❓ Yordam: /help"
        ),
        "help": (
            "📖 <b>Foydalanish yo'riqnomasi</b>\n\n"
            "1️⃣ Instagram'dan video, reel yoki story havolasini nusxalang\n"
            "2️⃣ Havolani menga yuboring\n"
            "3️⃣ Men videoni yuklab, sizga qaytaraman\n\n"
            "📌 <b>Qo'llab-quvvatlanadigan formatlar:</b>\n"
            "• Video postlar\n"
            "• Reels\n"
            "• Stories\n"
            "• IGTV\n\n"
            "⚠️ <b>Cheklovlar:</b>\n"
            "• Faqat ochiq (public) kontentlar yuklanadi\n"
            "• Maksimal fayl hajmi: 50MB (Telegram limiti)\n\n"
            "🌐 Tilni o'zgartirish: /lang\n\n"
            "👨‍💻 <b>Bot yaratuvchisi:</b> @parvizkarimov"
        ),
        "choose_lang": (
            "🌐 <b>Tilni tanlang / Выберите язык / Choose language:</b>"
        ),
        "lang_changed": "✅ Til o'zbekchaga o'zgartirildi!",
        "downloading": "⏳ Yuklab olinmoqda... Iltimos, kuting.",
        "processing": "🔄 Video qayta ishlanmoqda...",
        "success": "✅ Mana sizning videongiz!",
        "error_invalid_url": (
            "❌ Noto'g'ri havola!\n\n"
            "Iltimos, Instagram video, reel yoki story havolasini yuboring.\n\n"
            "📎 Namuna:\n"
            "<code>https://www.instagram.com/reel/ABC123/</code>"
        ),
        "error_download": (
            "❌ Yuklab olishda xatolik yuz berdi.\n\n"
            "Mumkin bo'lgan sabablar:\n"
            "• Havola noto'g'ri yoki eskirgan\n"
            "• Kontent yopiq (private) hisobga tegishli\n"
            "• Story muddati tugagan\n\n"
            "Iltimos, havolani tekshirib, qayta urinib ko'ring."
        ),
        "error_file_too_large": (
            "❌ Fayl hajmi juda katta (50MB dan oshadi).\n\n"
            "Telegram cheklovi tufayli bu videoni yuborib bo'lmaydi."
        ),
        "error_generic": "❌ Kutilmagan xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring.",
    },
    "ru": {
        "welcome": (
            "🎬 <b>Здравствуйте!</b>\n\n"
            "Я бот для скачивания видео, reels и stories из Instagram.\n\n"
            "📎 Отправьте мне ссылку из Instagram, и я скачаю для вас видео!\n\n"
            "🌐 Сменить язык: /lang\n"
            "❓ Помощь: /help"
        ),
        "help": (
            "📖 <b>Инструкция по использованию</b>\n\n"
            "1️⃣ Скопируйте ссылку на видео, reel или story из Instagram\n"
            "2️⃣ Отправьте ссылку мне\n"
            "3️⃣ Я скачаю видео и отправлю вам\n\n"
            "📌 <b>Поддерживаемые форматы:</b>\n"
            "• Видео посты\n"
            "• Reels\n"
            "• Stories\n"
            "• IGTV\n\n"
            "⚠️ <b>Ограничения:</b>\n"
            "• Скачиваются только открытые (публичные) материалы\n"
            "• Максимальный размер файла: 50MB (лимит Telegram)\n\n"
            "🌐 Сменить язык: /lang\n\n"
            "👨‍💻 <b>Создатель бота:</b> @parvizkarimov"
        ),
        "choose_lang": (
            "🌐 <b>Tilni tanlang / Выберите язык / Choose language:</b>"
        ),
        "lang_changed": "✅ Язык изменён на русский!",
        "downloading": "⏳ Скачиваю... Пожалуйста, подождите.",
        "processing": "🔄 Обработка видео...",
        "success": "✅ Вот ваше видео!",
        "error_invalid_url": (
            "❌ Неверная ссылка!\n\n"
            "Пожалуйста, отправьте ссылку на видео, reel или story из Instagram.\n\n"
            "📎 Пример:\n"
            "<code>https://www.instagram.com/reel/ABC123/</code>"
        ),
        "error_download": (
            "❌ Ошибка при скачивании.\n\n"
            "Возможные причины:\n"
            "• Ссылка неверна или устарела\n"
            "• Контент принадлежит закрытому (private) аккаунту\n"
            "• Срок действия story истёк\n\n"
            "Пожалуйста, проверьте ссылку и попробуйте снова."
        ),
        "error_file_too_large": (
            "❌ Файл слишком большой (более 50MB).\n\n"
            "Из-за ограничений Telegram это видео невозможно отправить."
        ),
        "error_generic": "❌ Произошла непредвиденная ошибка. Попробуйте позже.",
    },
    "en": {
        "welcome": (
            "🎬 <b>Welcome!</b>\n\n"
            "I'm a bot that downloads videos, reels and stories from Instagram.\n\n"
            "📎 Send me an Instagram link and I'll download the video for you!\n\n"
            "🌐 Change language: /lang\n"
            "❓ Help: /help"
        ),
        "help": (
            "📖 <b>How to use</b>\n\n"
            "1️⃣ Copy a video, reel or story link from Instagram\n"
            "2️⃣ Send the link to me\n"
            "3️⃣ I'll download the video and send it back to you\n\n"
            "📌 <b>Supported formats:</b>\n"
            "• Video posts\n"
            "• Reels\n"
            "• Stories\n"
            "• IGTV\n\n"
            "⚠️ <b>Limitations:</b>\n"
            "• Only public content can be downloaded\n"
            "• Maximum file size: 50MB (Telegram limit)\n\n"
            "🌐 Change language: /lang\n\n"
            "👨‍💻 <b>Bot creator:</b> @parvizkarimov"
        ),
        "choose_lang": (
            "🌐 <b>Tilni tanlang / Выберите язык / Choose language:</b>"
        ),
        "lang_changed": "✅ Language changed to English!",
        "downloading": "⏳ Downloading... Please wait.",
        "processing": "🔄 Processing video...",
        "success": "✅ Here's your video!",
        "error_invalid_url": (
            "❌ Invalid link!\n\n"
            "Please send an Instagram video, reel or story link.\n\n"
            "📎 Example:\n"
            "<code>https://www.instagram.com/reel/ABC123/</code>"
        ),
        "error_download": (
            "❌ Download failed.\n\n"
            "Possible reasons:\n"
            "• The link is invalid or expired\n"
            "• The content belongs to a private account\n"
            "• The story has expired\n\n"
            "Please check the link and try again."
        ),
        "error_file_too_large": (
            "❌ File is too large (over 50MB).\n\n"
            "Due to Telegram's limits, this video cannot be sent."
        ),
        "error_generic": "❌ An unexpected error occurred. Please try again later.",
    },
}


# Language display names and flags
LANGUAGE_OPTIONS = {
    "uz": "🇺🇿 O'zbekcha",
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
}


def get_message(lang: str, key: str) -> str:
    """Get a localized message by language code and message key."""
    return MESSAGES.get(lang, MESSAGES["uz"]).get(key, MESSAGES["uz"].get(key, ""))
