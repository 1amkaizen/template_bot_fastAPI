# main.py

import os
from fastapi import FastAPI
from dotenv import load_dotenv

# Load variabel lingkungan dari .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

from setup import setup_bot
from webhooks.telegram_webhook import router as telegram_router

# Inisialisasi FastAPI app
app = FastAPI()

# Tambahkan router untuk endpoint Telegram webhook
app.include_router(telegram_router)


# Eksekusi saat startup
@app.on_event("startup")
async def on_startup():
    await setup_bot()

