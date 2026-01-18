# keyboards.py
def get_filter_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            ["🍲 Супы", "🥩 Мясо"],
            ["🥗 Салаты", "🥖 Выпечка"],
            ["🍝 Паста", "🌮 Быстро"],
            ["🔍 По ингредиенту", "🎲 Рандом"],
            ["📊 Статистика"]
        ],
        resize_keyboard=True
    )

def get_time_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("⏱️ < 30 мин", callback_data="time:<30")],
        [InlineKeyboardButton("⏰ 30-60 мин", callback_data="time:30-60")],
        [InlineKeyboardButton("⏳ > 60 мин", callback_data="time:>60")],
        [InlineKeyboardButton("❌ Закрыть", callback_data="close")]
    ])
