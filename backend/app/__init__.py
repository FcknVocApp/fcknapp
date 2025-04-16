from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import csv  # ✅ добавь вот это

from datetime import datetime

app = FastAPI()

# Указываем путь до шаблонов
templates = Jinja2Templates(directory="app/templates")

# 📌 Главная страница
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ⬇️ Получаем путь на один уровень выше, чтобы уйти из backend/
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
STATIC_DIR = os.path.join(BASE_DIR, "frontend", "public")

print("Статика из папки:", STATIC_DIR)

app.mount("/public", StaticFiles(directory=STATIC_DIR), name="public")

templates = Jinja2Templates(directory="app/templates")

# ⬅️ Потом можно прописывать маршруты
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Путь к CSV с фразовыми глаголами
CSV_PATH = os.path.join(os.path.dirname(__file__), "phrasal_verbs.csv")

# Словарь с фразовыми глаголами
phrasal_dict = {}
with open(CSV_PATH, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        verb = row["phrasal_verb"].strip().lower()
        phrasal_dict[verb] = {
            "translation": row["translation"].strip(),
            "example_en": row["example_en"].strip(),
            "example_ru": row["example_ru"].strip(),
        }

# Временное хранилище добавленных слов
user_words = []

# 🔹 Главная страница
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 🔹 Заглушка для Quiz Now
@app.get("/quiznow", response_class=HTMLResponse)
async def quiz_now(request: Request):
    return templates.TemplateResponse("quiznow.html", {"request": request})

# 🔹 Заглушка для Quiz Week
@app.get("/quizweek", response_class=HTMLResponse)
async def quiz_week(request: Request):
    return templates.TemplateResponse("quizweek.html", {"request": request})

# 🔹 Страница перевода
@app.get("/translate", response_class=HTMLResponse)
async def get_translate(request: Request):
    return templates.TemplateResponse("translate.html", {"request": request, "result": None, "added": False})

@app.post("/translate", response_class=HTMLResponse)
async def post_translate(request: Request, word: str = Form(...)):
    word = word.strip().lower()
    result = phrasal_dict.get(word)
    if result:
        result["word"] = word
    else:
        result = {
            "word": word,
            "translation": "перевод не найден — может, ты выдумываешь?",
            "example_en": "",
            "example_ru": ""
        }
    return templates.TemplateResponse("translate.html", {"request": request, "result": result, "added": False})

# 🔹 Добавление слова в словарь
@app.post("/add_word", response_class=HTMLResponse)
async def add_word(
    word: str = Form(...),
    translation: str = Form(...),
    example_en: str = Form(...),
    example_ru: str = Form(...)
):
    user_words.append({
        "word": word,
        "translation": translation,
        "example_en": example_en,
        "example_ru": example_ru,
        "added": datetime.now().isoformat()
    })
    return """
    <div id="add-button-container">
        <button disabled class='bg-green-500 text-white font-semibold px-6 py-3 rounded w-full text-xl transition'>
            ✅ Добавлено в словарь
        </button>
    </div>
    """