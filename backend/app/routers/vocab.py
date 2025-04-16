
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
import random
from pydantic import BaseModel

router = APIRouter(tags=["vocab"])
get_db = database.get_db

# 🔁 Реакции
success_responses = [
    "Ничоси. Удивил(а).",
    "Ну ты знаток, однако.",
    "Это было слишком легко для тебя, да?",
    "Уважаю. Мозги работают."
]
fail_responses = [
    "Нет, ну ты серьёзно?",
    "Вот это позорище...",
    "Где твои мозги были, когда ты отвечал(а)?",
    "Промах. Залетай ещё раз."
]

def generate_options(correct: str, all_translations: list, count=4):
    options = set()
    while len(options) < count - 1:
        opt = random.choice(all_translations)
        if opt != correct:
            options.add(opt)
    options = list(options)
    options.append(correct)
    random.shuffle(options)
    return options

@router.post("/quiznow")
def quiz_now(data: schemas.QuizRequest, db: Session = Depends(get_db)):
    query = db.query(models.WordEntry)
    if data.only_mistakes:
        query = query.filter(models.WordEntry.mistakes > 0)
    words = query.order_by(models.WordEntry.created_at.desc()).limit(data.count).all()
    all_translations = [w.translation for w in db.query(models.WordEntry).all()]
    result = []
    for w in words:
        result.append({
            "id": w.id,
            "word": w.word,
            "options": generate_options(w.translation, all_translations),
            "correct": w.translation
        })
    return result

class QuizCheck(BaseModel):
    id: int
    answer: str

@router.post("/quiznow/check")
def check_quiz_answer(data: QuizCheck, db: Session = Depends(get_db)):
    word = db.query(models.WordEntry).filter(models.WordEntry.id == data.id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Слово не найдено")

    if data.answer.strip().lower() == word.translation.strip().lower():
        return {
            "result": "✅ Верно",
            "reaction": random.choice(success_responses)
        }
    else:
        word.mistakes += 1
        db.commit()
        return {
            "result": "❌ Ошибка",
            "correct": f"{word.word} — {word.translation}",
            "reaction": random.choice(fail_responses)
        }
@router.get("/quizweek")
def quiz_week(db: Session = Depends(get_db)):
    words = db.query(models.Word).filter(models.Word.mistakes > 0).all()
    return words