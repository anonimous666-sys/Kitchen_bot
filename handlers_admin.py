# handlers_admin.py
@router.message(F.photo | F.video)
async def handle_media(message: Message, state: FSMContext):
    user_id = message.from_user.id
    
    if user_id not in ADMINS:
        await message.answer("❌ Доступ запрещен")
        return
    
    photo = message.photo[-1] if message.photo else None
    video = message.video if message.video else None
    
    if photo:
        file = await bot.get_file(photo.file_id)
        photo_path = f"media/recipe_{int(time.time())}.jpg"
        await bot.download_file(file.file_path, photo_path)
        await state.update_data(photo_path=photo_path)
        await message.answer(f"✅ Фото сохранено: {photo_path}")
    
    if video:
        file = await bot.get_file(video.file_id)
        video_path = f"media/recipe_{int(time.time())}.mp4"
        await bot.download_file(file.file_path, video_path)
        await state.update_data(video_path=video_path)
        await message.answer(f"✅ Видео сохранено: {video_path}")
