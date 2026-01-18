# models.py - расширяем Recipe
class Recipe(Base):
    # ... существующие поля ...
    photo_path = Column(String)
    video_path = Column(String)
    prep_time = Column(Integer, default=30)  # минуты
