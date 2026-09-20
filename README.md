# 🎬 Instagram Downloader Telegram Bot

Instagram'dan video, reels va story'larni yuklab beruvchi Telegram bot.

## ✨ Xususiyatlari

- 📥 Instagram video, reels, stories va IGTV yuklab olish
- 🌐 3 tilda ishlaydi: O'zbekcha, Русский, English
- 🔐 Cookies orqali autentifikatsiya
- 🚀 Railway.app da deploy qilish mumkin

## 🛠 O'rnatish

### 1. Dependencies o'rnatish

```bash
pip install -e .
```

### 2. Bot Token olish

1. Telegram'da [@BotFather](https://t.me/BotFather) ga yozing
2. `/newbot` buyrug'ini yuboring
3. Bot nomi va username ni kiriting
4. Berilgan tokenni saqlang

### 3. Cookies tayyorlash

Instagram cookies kerak bo'ladi (anonim yuklab olish cheklangan):

1. Chrome brauzerda [Instagram.com](https://instagram.com) ga kiring
2. **"Get cookies.txt LOCALLY"** kengaytmasini o'rnating:
   - [Chrome Web Store](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
3. Instagram sahifasida kengaytmani bosib, cookies'ni export qiling
4. `cookies.txt` faylini loyiha papkasiga saqlang

### 4. Botni ishga tushirish

```bash
# Environment variable sifatida token berish
set BOT_TOKEN=your_bot_token_here
python main.py
```

## 🚀 Railway.app da Deploy

### Environment Variables

Railway dashboard'da quyidagi environment variable'larni sozlang:

| Variable | Tavsif | Majburiy |
|----------|--------|----------|
| `BOT_TOKEN` | Telegram bot token (BotFather'dan) | ✅ |
| `COOKIES_CONTENT` | cookies.txt fayl mazmuni | ✅ |
| `COOKIES_PATH` | Cookies fayl yo'li (default: `cookies.txt`) | ❌ |
| `DOWNLOAD_DIR` | Yuklab olish papkasi (default: `downloads`) | ❌ |

### Deploy qadamlari

1. GitHub'ga push qiling
2. [Railway.app](https://railway.app) da yangi loyiha yarating
3. GitHub repo'ni ulang
4. Environment variable'larni sozlang
5. Deploy tugashini kuting

> **⚠️ Muhim:** `COOKIES_CONTENT` ga cookies.txt faylining to'liq mazmunini qo'ying. Bot ishga tushganda uni avtomatik `cookies.txt` fayliga yozadi.

## 📱 Bot buyruqlari

| Buyruq | Tavsif |
|--------|--------|
| `/start` | Botni ishga tushirish |
| `/help` | Yordam ko'rsatmasi |
| `/lang` | Tilni o'zgartirish (UZ/RU/EN) |

## 📝 Foydalanish

1. Telegram'da botni oching
2. `/start` buyrug'ini yuboring
3. Instagram'dan video/reel/story havolasini nusxalang
4. Havolani botga yuboring
5. Bot videoni yuklab, sizga qaytaradi

## ⚠️ Cheklovlar

- Faqat **ochiq (public)** kontentlar yuklanadi
- Maksimal fayl hajmi: **50MB** (Telegram limiti)
- Stories vaqt o'tgach o'chib ketadi — tezroq yuklang
- Instagram vaqti-vaqti bilan API'ni o'zgartiradi — `yt-dlp` ni yangilab turing

## 📄 Litsenziya

MIT
