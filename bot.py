import asyncio
import logging
import re
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, ADMIN_IDS, DATABASE_NAME
import database as db

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Состояния FSM
class RecipeForm(StatesGroup):
    waiting_name = State()
    waiting_ingredients = State()
    waiting_instructions = State()

# Обработчики команд
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "🍳 Kitchen TTK Bot\n\n"
        "📝 /search_картошка_лук - поиск рецептов\n"
        "📋 /list - все рецепты\n"
        "/help - справка"
    )

@dp.message(Command("help"))
async def cmd_help(message: Message):
    help_text = (
        "🍳 Kitchen TTK - команды:\n\n"
        "🔍 Поиск: /search_картошка_лук_масло\n"
        "📋 Список: /list\n"
        "➕ Добавить (админ): /add\n"
        "❌ Удалить (админ): /delete [id]\n\n"
        "💡 Пиши ингредиенты через _ вместо пробелов!"
    )
    await message.answer(help_text)

@dp.message(Command("list"))
async def cmd_list(message: Message):
    recipes = await db.get_all_recipes()
    if not recipes:
        await message.answer("📭 Рецепты не найдены")
        return
    
    text = "📋 Все рецепты:\n\n"
    for recipe in recipes:
        text += f"🆔 {recipe['id']}\n"
        text += f"🍲 {recipe['name']}\n"
        text += f"🥘 {recipe['ingredients'][:100]}...\n\n"
    
    await message.answer(text[:4000])

@dp.message(Command("search"))
async def cmd_search(message: Message):
    query = message.text.replace('/search_', '').strip()
    if not query:
        await message.answer("❓ Укажите ингредиенты: /search_картошка_лук")
        return
    
    ingredients = [ing.strip() for ing in query.split('_')]
    recipes = await db.search_recipes(ingredients)
    
    if not recipes:
        await message.answer(f"😔 Рецепты с {query} не найдены")
        return
    
    text = f"🍳 Найдено {len(recipes)} рецептов для {query}:\n\n"
    for recipe in recipes[:5]:  # Первые 5
        text += f"🆔 {recipe['id']}\n"
        text += f"🍲 {recipe['name']}\n"
        text += f"🥘 {recipe['ingredients'][:80]}...\n\n"
    
    await message.answer(text)

# Админские команды
if ADMIN_IDS:
    @dp.message(Command("add"))
    async def cmd_add(message: Message, state: FSMContext):
        if message.from_user.id not in ADMIN_IDS:
            await message.answer("🚫 Только для админов")
            return
        
        await message.answer("🍲 Название рецепта:")
        await state.set_state(RecipeForm.waiting_name)

    @dp.message(Command("delete"))
    async def cmd_delete(message: Message):
        if message.from_user.id not in ADMIN_IDS:
            await message.answer("🚫 Только для админов")
            return
        
        try:
            recipe_id = int(message.text.split()[1])
            deleted = await db.delete_recipe(recipe_id)
            status = "✅ Удалено!" if deleted else "❌ Рецепт не найден"
            await message.answer(status)
        except (IndexError, ValueError):
            await message.answer("❓ Используйте: /delete 123")

# FSM обработчики
@dp.message(RecipeForm.waiting_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await message.answer("🥘 Ингредиенты (через запятую):")
    await state.set_state(RecipeForm.waiting_ingredients)

@dp.message(RecipeForm.waiting_ingredients)
async def process_ingredients(message: Message, state: FSMContext):
    await state.update_data(ingredients=message.text.strip())
    await message.answer("📝 Инструкция:")
    await state.set_state(RecipeForm.waiting_instructions)

@dp.message(RecipeForm.waiting_instructions)
async def process_instructions(message: Message, state: FSMContext):
    user_data = await state.get_data()
    
    recipe = {
        'name': user_data['name'],
        'ingredients': user_data['ingredients'],
        'instructions': message.text.strip()
    }
    
    recipe_id = await db.add_recipe(recipe)
    await message.answer(f"✅ Рецепт добавлен! ID: {recipe_id}")
    await state.clear()

# Запуск поиска без команды (по ингредиентам)
@dp.message(F.text)
async def auto_search(message: Message):
    ingredients = re.findall(r'\w+', message.text.lower())
    if len(ingredients) >= 2 and '_' not in message.text:
        query = '_'.join(ingredients[:3])
        await cmd_search(Message(text=f"/search_{query}", from_user=message.from_user))

async def main():
    # Инициализация БД
    await db.init_db()
    print("✅ База данных готова")
    
    # Запуск бота
    print("🚀 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
