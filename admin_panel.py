@router.message(lambda m: m.text == "📊 Статистика" and m.from_user.id in ADMINS)
async def admin_stats(message: Message):
    async with async_session() as session:
        # Подсчет пользователей
        users_count = await session.execute(
            select(func.count(User.id))
        )
        
        # Популярные рецепты
        popular = await session.execute(
            select(Recipe)
            .order_by(Recipe.views.desc())
            .limit(5)
        )
        
        stats_text = f"""
📈 СТАТИСТИКА БОТА

👥 Пользователей: {users_count.scalar()}
🍽️ Рецептов: 47
🔥 Самые популярные:
"""
        
        for i, recipe in enumerate(popular.scalars(), 1):
            stats_text += f"{i}. {recipe.name} - {recipe.views} просмотров\n"
    
    await message.answer(stats_text)

@router.message(F.text.startswith("/broadcast"))
async def broadcast_message(message: Message):
    if message.from_user.id not in ADMINS:
        return
    
    users_count = await async_session.execute(
        select(func.count(User.id))
    )
    
    await message.answer(f"📢 Рассылка доступна для {users_count.scalar()} пользователей")
