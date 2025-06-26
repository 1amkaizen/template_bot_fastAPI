# handlers/user/vip.py

from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telecore.midtrans.client import MidtransClient
#from telecore.midtrans.client import get_customer_from_user  # Ambil dari core
from telecore.settings.config_db import get_vip_price
from telecore.supabase.save_transaction import save_transaction  # ✅ sesuai struktur kamu
from telecore.telegram.buttons import vip_menu_buttons
from datetime import datetime
import logging
from telecore.midtrans.client import MidtransClient


logger = logging.getLogger(__name__)


async def vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    vip_price = get_vip_price()

    text = (
        "✅ *BENEFIT JOIN VIP MICINDOTID*\n\n"
        "1️⃣ 📈 Dapat 5–10 sinyal memecoin cuan harian\n"
        "2️⃣ 🔍 Diajari cara screening koin micin potensial sampai 100%++\n"
        "3️⃣ 🤝 Live trading bareng komunitas, 3-5x seminggu\n"
        "4️⃣ 🎓 Akses modul edukasi lengkap & update terus\n"
        "5️⃣ 🧠 Panduan money management & strategi scalping\n"
        "6️⃣ 💬 Komunitas aktif & ramah buat pemula sampai pro\n\n"
        f"💸 Harga sekali bayar *Rp {int(vip_price):,}* — seumur hidup cuan bareng!\n\n"
        "Klik *Bayar Sekarang* untuk aktivasi VIP kamu. 👇"
    )

    markup = InlineKeyboardMarkup(vip_menu_buttons())

    if update.message:
        await update.message.reply_text(text, reply_markup=markup, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=markup, parse_mode="Markdown")


async def handle_payment_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user

    try:
        client = MidtransClient()
        vip_price = get_vip_price()
        order_id = client.generate_order_id(prefix="VIP")
        customer = MidtransClient.get_customer_from_user(user)
        response = await client.create_qris_payment(order_id, vip_price, customer)

        await save_transaction({
            "order_id": order_id,
            "user_id": user.id,
            "username": user.username or "",
            "full_name": user.full_name,
            "transaction_id": response.get("transaction_id"),
            "payment_type": response.get("payment_type"),
            "gross_amount": response.get("gross_amount"),
            "currency": response.get("currency"),
            "transaction_time": response.get("transaction_time") or datetime.utcnow().isoformat(),
            "status_message": response.get("status_message"),
            "transaction_status": response.get("transaction_status", "pending"),
            "fraud_status": response.get("fraud_status", ""),
            "signature_key": response.get("signature_key", ""),
            "merchant_id": response.get("merchant_id", ""),
        })

        snap_url = response.get("redirect_url", "[tidak tersedia]")
        await query.edit_message_text(
            text=f"✅ Transaksi berhasil dibuat!\n\nKlik link berikut untuk bayar:\n{snap_url}"
        )

    except Exception:
        logger.exception("❌ Gagal proses pembayaran VIP")
        await query.edit_message_text("❌ Terjadi kesalahan saat memproses pembayaran.")

