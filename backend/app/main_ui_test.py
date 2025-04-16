from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Тестовый UI</title>
    </head>
    <body>
        <h1 style="font-family: sans-serif; color: green;">🎉 Привет, это UI! Всё работает!</h1>
    </body>
    </html>
    """