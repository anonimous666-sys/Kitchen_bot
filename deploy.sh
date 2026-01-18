#!/bin/bash
echo "🚀 Деплой Kitchen TTK Bot"
pip install -r requirements.txt
cp .env.example .env
echo "✅ Готово! Отредактируйте .env и запустите python bot.py"
