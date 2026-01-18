# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ID администратора
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))

# База данных
DATABASE_PATH = "recipes.db"

# Магазин
SHOP_ITEMS = {
    "premium": {
        "name": "🥇 Premium",
        "price": 299,
        "description": "Безлимит + история"
    }
}

# Проверки
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден в .env файле!")
