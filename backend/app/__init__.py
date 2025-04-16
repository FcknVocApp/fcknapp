import sys
print("🧪 Python version on Render:", sys.version)

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import os
import csv
import random
from datetime import datetime

# 🔧 Базовая настройка
app = FastAPI()

# 📀 Шаблоны Jinja2
TEMPLATES_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'templates'
))
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# 📁 Статика (лежит в frontend/public)
STATIC_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', 'frontend', 'public'
))

if os.path.exists(STATIC_DIR):
    app.mount("/public", StaticFiles(directory=STATIC_DIR), name="public")
else:
    print(f"⚠️ Статика не найдена по пути: {STATIC_DIR}")

# 📂 CSV с фразовыми глаголами
CSV_PATH = os.path.join(os.path.dirname(__file__), "phrasal_verbs.csv")

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

# 🧐 Временное хранилище
user_words = []
wrong_words = []

# 📍 Главная
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 🔥 Quiz Now
@app.get("/quiznow", response_class=HTMLResponse)
async def quiz_now(request: Request):
    return templates.TemplateResponse("quiznow.html", {"request": request})

# ➞ Следующий вопрос
@app.get("/quiznow/next", response_class=HTMLResponse)
async def quiznow_next(request: Request):
    if not user_words:
        return HTMLResponse("<p>Ты ещё ни одного слова не добавил, ноль усилий — ноль достижений.</p>")

    word = random.choice(user_words)

    distractors = [w["translation"] for w in user_words if w["word"] != word["word"]]
    distractors = list(set(distractors))
    random.shuffle(distractors)

    options = [word["translation"]] + distractors[:2]
    random.shuffle(options)

    return templates.TemplateResponse("quiznow_question.html", {
        "request": request,
        "word": word,
        "options": options
    })

# ✅ Ответ на вопрос
@app.post("/quiznow/answer", response_class=HTMLResponse)
async def quiznow_answer(
    request: Request,
    answer: str = Form(...),
    correct: str = Form(...),
    word: str = Form(...)
):
    if answer == correct:
        message = "😎 Ну не зря дышишь. Правильно!"
    else:
        message = f"💀 Неверно. Правильный перевод: <strong>{correct}</strong>.<br>Позор, запиши 100 раз."
        wrong_words.append(word)

    return HTMLResponse(f"""
        <div class='feedback'>
          <p>{message}</p>
          <button class='btn-soft' hx-get='/quiznow/next' hx-target='#quiz-content' hx-swap='innerHTML' style='margin-top: 1rem;'>Следующее слово</button>
        </div>
    """)

# 📍 Quiz Week
@app.get("/quizweek", response_class=HTMLResponse)
async def quiz_week(request: Request):
    return templates.TemplateResponse("quizweek.html", {"request": request})

# 📍 Страница перевода
@app.get("/translate", response_class=HTMLResponse)
async def get_translate(request: Request):
    return templates.TemplateResponse("translate.html", {"request": request})

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

    return templates.TemplateResponse("translate_result.html", {
        "request": request,
        "result": result
    })

# 📍 Добавление слова в словарь
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
    <div id=\"add-button-container\">
      <button disabled style=\"background-color: #22c55e; color: white; border: none; padding: 0.75rem 1.75rem; font-size: 1rem; font-weight: 600; border-radius: 0.5rem; text-align: center; cursor: default;\">
        ✅ Добавлено в словарь
      </button>
    </div>
    """

# 📍 Страница "Мой словарь"
@app.get("/mywords", response_class=HTMLResponse)
async def get_mywords(request: Request):
    return templates.TemplateResponse("mywords.html", {
        "request": request,
        "words": user_words
    })