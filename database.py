import aiosqlite
import asyncio
from typing import List, Dict

async def init_db():
    async with aiosqlite.connect('kitchen_ttk.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                ingredients TEXT NOT NULL,
                instructions TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()

async def add_recipe(recipe: Dict) -> int:
    async with aiosqlite.connect('kitchen_ttk.db') as db:
        cursor = await db.execute(
            'INSERT INTO recipes (name, ingredients, instructions) VALUES (?, ?, ?)',
            (recipe['name'], recipe['ingredients'], recipe['instructions'])
        )
        await db.commit()
        return cursor.lastrowid

async def get_all_recipes() -> List[Dict]:
    async with aiosqlite.connect('kitchen_ttk.db') as db:
        cursor = await db.execute('SELECT * FROM recipes ORDER BY created_at DESC')
        return await cursor.fetchall()

async def search_recipes(ingredients: List[str]) -> List[Dict]:
    async with aiosqlite.connect('kitchen_ttk.db') as db:
        placeholders = ','.join(['?' for _ in ingredients])
        query = f'''
            SELECT * FROM recipes 
            WHERE LOWER(ingredients) LIKE LOWER('%{ingredients[0]}%')
            ORDER BY id DESC LIMIT 10
        '''
        cursor = await db.execute(query, ingredients)
        return await cursor.fetchall()

async def delete_recipe(recipe_id: int) -> bool:
    async with aiosqlite.connect('kitchen_ttk.db') as db:
        cursor = await db.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
        await db.commit()
        return cursor.rowcount > 0
