# handlers_search.py
@router.message(lambda m: m.text == "🔍 По ингредиенту")
async def search_by_ingredient(message: Message, state: FSMContext):
    await message.answer("🍅 Введите ингредиенты через запятую:\n(курица, рис, помидоры)")
    await state.set_state(Search.ingredient)

@router.message(Search.ingredient)
async def process_ingredient_search(message: Message, state: FSMContext):
    ingredients = [i.strip().lower() for i in message.text.split(",")]
    
    # Ищем совпадения в названии и ингредиентах
    query = select(Recipe).join(IngredientRecipe).join(Ingredient).filter(
        or_(
            func.lower(Recipe.name).contains(ingredients[0]),
            Ingredient.name.in_(ingredients)
        )
    )
    
    results = await async_session.execute(query)
    recipes = results.scalars().all()
    
    if recipes:
        text = "🍽️ Найдено по вашим ингредиентам:\n\n"
        for i, recipe in enumerate(recipes[:5], 1):
            text += f"{i}. {recipe.name} ({recipe.prep_time} мин)\n"
        await message.answer(text, reply_markup=get_recipe_keyboard(recipes))
    else:
        await message.answer("😔 По этим ингредиентам ничего не найдено")
    
    await state.clear()
