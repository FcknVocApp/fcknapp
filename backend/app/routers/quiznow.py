from fastapi import APIRouter

router = APIRouter()

@router.get("/quiznow/ping")
def quiz_ping():
    return {"message": "Quiz router is working!"}