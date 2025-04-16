#!/bin/bash

# Запуск FastAPI в фоне
uvicorn app.__init__:app --reload &

# Ждём немного, чтобы FastAPI успел запуститься
sleep 2

# Запускаем ngrok
ngrok http 8000