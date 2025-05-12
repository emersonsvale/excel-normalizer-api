from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.main import app as main_app

app = FastAPI()

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

# Importando todas as rotas do app principal
app.mount("/", main_app)

# This is the entry point for Vercel 