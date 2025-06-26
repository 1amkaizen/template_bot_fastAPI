# setup.py
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
)

from telecore.config import BOT_TOKEN,WEBHOOK_URL
from handlers.user.start import button_callback
from handlers.user.start import get_handler as get_start_handlers
import bot_app



async def setup_bot():
    bot_app.application = ApplicationBuilder().token(BOT_TOKEN).build()

    for handler in get_start_handlers():
        bot_app.application.add_handler(handler)

    bot_app.application.add_handler(CallbackQueryHandler(button_callback))

    await bot_app.application.initialize()
    await bot_app.application.start()

    # 🕒 Scheduler
    setup_scheduler()

    # 🌐 Set webhook
    await bot_app.application.bot.set_webhook(url=WEBHOOK_URL)
    print(f"🌐 Webhook diset ke: {WEBHOOK_URL}")

    print("✅ Bot started.")
    bot_app.startup_event.set()
