# bot_app.py
from telegram.ext import Application
import asyncio

application: Application = None
startup_event = asyncio.Event()  # ⬅️ tambahkan ini

