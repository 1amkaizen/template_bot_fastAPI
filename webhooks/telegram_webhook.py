# webhooks/telegram_webhook.py

import logging
from fastapi import APIRouter, Request, Response
from telegram import Update
import colorlog
import json
from telecore.logging.logger import get_logger

# Router FastAPI
router = APIRouter()

logger = colorlog.getLogger("webhooks.telegram_webhook")

@router.post("/telegram_webhook")
async def telegram_webhook(request: Request):
    from bot_app import application

    if application is None:
        logger.error("❌ BOT belum diinisialisasi (application is None)")
        return Response(status_code=503, content="Bot not initialized yet")

    try:
        data = await request.json()
        logger.debug(f"📦 Raw update:\n{json.dumps(data, indent=2)}")

        update = Update.de_json(data, application.bot)

        if update.message:
            user = update.message.from_user
            chat = update.message.chat
            logger.info("\n📩 [MESSAGE RECEIVED]\n"
                        f"  - user_id     : {user.id}\n"
                        f"  - username    : @{user.username or '-'}\n"
                        f"  - full_name   : {user.full_name or '-'}\n"
                        f"  - language    : {user.language_code or '-'}\n"
                        f"  - is_bot      : {user.is_bot}\n"
                        f"  - chat_id     : {chat.id}\n"
                        f"  - chat_type   : {chat.type}\n"
                        f"  - text        : {update.message.text}")

        elif update.callback_query:
            user = update.callback_query.from_user
            msg = update.callback_query.message
            logger.info("\n🔘 [CALLBACK RECEIVED]\n"
                        f"  - user_id     : {user.id}\n"
                        f"  - username    : @{user.username or '-'}\n"
                        f"  - full_name   : {user.full_name or '-'}\n"
                        f"  - chat_id     : {msg.chat.id}\n"
                        f"  - chat_type   : {msg.chat.type}\n"
                        f"  - data        : {update.callback_query.data}")

        elif update.my_chat_member:
            chat = update.my_chat_member.chat
            new = update.my_chat_member.new_chat_member
            old = update.my_chat_member.old_chat_member
            from_user = update.my_chat_member.from_user
            logger.info("\n➕ [BOT CHAT MEMBER UPDATE]\n"
                        f"  - chat_id       : {chat.id}\n"
                        f"  - chat_title    : {chat.title or '-'}\n"
                        f"  - chat_type     : {chat.type}\n"
                        f"  - added_by_id   : {from_user.id}\n"
                        f"  - added_by_name : {from_user.full_name}\n"
                        f"  - status_before : {old.status}\n"
                        f"  - status_after  : {new.status}")

        else:
            logger.warning("\n⚠️ [UNHANDLED UPDATE TYPE]\n"
                           f"  - Data: {json.dumps(data, indent=2)}")

        await application.process_update(update)
        return Response(status_code=200)

    except Exception as e:
        logger.exception(f"❌ Error saat proses update:\n{e}")
        return Response(status_code=500, content="Internal Server Error")

