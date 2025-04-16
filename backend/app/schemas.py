from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Существующие модели
class WordEntryCreate(BaseModel):
    word: str
    translation: str
    example_en: str
    example_ru: str = ""
    mistakes: int = 0

class WordEntryOut(WordEntryCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # заменяет orm_mode для Pydantic v2

class QuizRequest(BaseModel):
    count: int = 5
    only_mistakes: bool = False

# Новая модель для фразовых глаголов
class PhrasalVerb(BaseModel):
    word: str
    translation: str
    example_en: str
    example_ru: str
    id: int
    mistakes: Optional[int] = 0