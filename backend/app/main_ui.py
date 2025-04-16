from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import csv
import os

# Инициализация приложения
app = FastAPI()

# Пути к шаблонам, статике и CSV
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")
CSV_PATH = os.path.join(BASE_DIR, "..", "Baza", "translations", "phrasal_verbs_all_fixed_final.csv")

# Подключение шаблонов и статики
templates = Jinja2Templates(directory=TEMPLATE_DIR)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Загрузка данных из CSV в словарь
phrasal_dict = {}
print(f"[INFO] Загружаем фразовые глаголы из: {CSV_PATH}")
with open(CSV_PATH, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        verb = row["phrasal_verb"].strip().lower()
        phrasal_dict[verb] = {
            "translation": row["translation"].strip(),
            "example_en": row["example_en"].strip(),
            "example_ru": row["example_ru"].strip()
        }
print(f"[INFO] Загружено {len(phrasal_dict)} фразовых глаголов")

# Главная страница
@app.get("/", response_class=HTMLResponse)
@app.get("/translate", response_class=HTMLResponse)
async def read_translate_page(request: Request):
    return templates.TemplateResponse("translate.html", {"request": request, "result": None})

# Обработка перевода
@app.post("/translate", response_class=HTMLResponse)
async def post_translate(request: Request, word: str = Form(...)):
    query = word.strip().lower()
    result = phrasal_dict.get(query)
    if not result:
        result = {
            "word": query,
            "translation": "перевод не найден — может, ты выдумываешь?",
            "example_en": "",
            "example_ru": ""
        }
    else:
        result["word"] = query
    return templates.TemplateResponse("translate_result.html", {"request": request, "result": result})