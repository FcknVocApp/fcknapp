from fastapi import APIRouter
import requests
import pandas as pd
from pydantic import BaseModel

# Создание маршрута
router = APIRouter()

# API ключ и папка для Yandex Translate
API_KEY = 'YOUR_API_KEY'
FOLDER_ID = 'YOUR_FOLDER_ID'

# Функция перевода через Yandex API
def translate_text_yandex(text):
    if pd.isna(text) or text.strip() == '':
        return ''
    try:
        response = requests.post(
            'https://translate.api.cloud.yandex.net/translate/v2/translate',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Api-Key {API_KEY}'
            },
            json={
                'folderId': FOLDER_ID,
                'texts': [text],
                'sourceLanguageCode': 'en',
                'targetLanguageCode': 'ru'
            }
        )
        response.raise_for_status()
        translated = response.json()['translations'][0]['text']
        return translated
    except Exception as e:
        print(f"Ошибка при переводе: {e}")
        return ''

# Модель для запроса
class TranslateRequest(BaseModel):
    word: str
    tox_level: str

# Модель для ответа
class TranslateResponse(BaseModel):
    translation: str
    example_en: str
    example_ru: str

# Маршрут для перевода слова
@router.post("/translate", response_model=TranslateResponse)
async def translate(request: TranslateRequest):
    word = request.word
    tox_level = request.tox_level

    # Логирование запроса
    print(f"Получен запрос на перевод: слово '{word}', токсичность '{tox_level}'")

    # Перевод
    translated = translate_text_yandex(word)
    print(f"Переведено: {translated}")

    example_en = f"This is an example of the word '{word}'."  # Пример на английском
    example_ru = f"Это пример использования слова '{word}'."  # Пример на русском

    return {
        "translation": translated,
        "example_en": example_en,
        "example_ru": example_ru
    }