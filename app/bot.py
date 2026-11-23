import os
import asyncio
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpx2").setLevel(logging.WARNING)

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    TypeHandler,
    ApplicationHandlerStop,
)

from app.agent import ask_agent
from app.tools import format_system_status
from app.tools import format_system_status, get_docker_status

from app.memory import (
    initialize_database,
    get_history,
    save_turn,
    clear_history,
)

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN belum dikonfigurasi")

async def authorize_update(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user = update.effective_user
    message = update.effective_message

    if not user or not message:
        return

    # Izinkan command /id untuk mengambil Telegram User ID
    if message.text and message.text.split()[0].split("@")[0] == "/id":
        return

    allowed_ids = {
        int(value.strip())
        for value in os.getenv("TELEGRAM_ALLOWED_USER_IDS", "").split(",")
        if value.strip().isdigit()
    }

    if user.id not in allowed_ids:
        await message.reply_text("Akses ditolak. User ID Anda belum diizinkan.")
        raise ApplicationHandlerStop

async def id_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user_id = update.effective_user.id
    await update.message.reply_text(
        f"Telegram User ID: {user_id}"
    )

# Memory sementara per chat
# chat_histories: dict[int, list[dict[str, str]]] = {}


async def post_init(application: Application):
    commands = [
        ("start", "Mulai AI Agent"),
        ("help", "Bantuan penggunaan"),
        ("clear", "Hapus riwayat percakapan"),
        ("status", "Lihat kondisi server WSL2"),
        ("docker", "Lihat status Docker containers"),
    ]

    await application.bot.set_my_commands(commands)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hermes AI Support\n\n"
        "/start - Mulai bot\n"
        "/help - Bantuan\n"
        "/clear - Hapus riwayat percakapan"
    )


async def clear_command(update, context):
    clear_history(update.effective_chat.id)
    await update.message.reply_text(
        "Riwayat percakapan berhasil dibersihkan."
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo! Saya AI Technical Support Agent.\n"
        "Silakan kirim pertanyaan teknis kamu."
    )



async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    chat_id = update.effective_chat.id
    user_message = update.message.text

    history = chat_histories.setdefault(chat_id, [])

    logger.info("Pesan diterima: %s", user_message[:100])

    try:
        await update.message.chat.send_action("typing")

        logger.info("Memanggil Gemini melalui LangGraph...")

        answer = await asyncio.to_thread(
            ask_agent,
            user_message,
            history,
        )

        logger.info(
            "Gemini selesai. Panjang jawaban: %d karakter",
            len(answer),
        )

        history.extend([
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": answer},
        ])

        chat_histories[chat_id] = history[-20:]

        logger.info("Mengirim jawaban ke Telegram...")

        await update.message.reply_text(clean_response(answer))

        logger.info("Jawaban berhasil dikirim ke Telegram.")

    except Exception:
        logger.exception("Gagal memproses pesan dari Telegram")

        await update.message.reply_text(
            "Agent gagal memproses permintaan. Silakan periksa log aplikasi."
        )


async def status_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    status = format_system_status()
    await update.message.reply_text(status)

def run_bot():
    initialize_database()

    application = (
        Application.builder()
        .token(TOKEN)
        .post_init(post_init)
        .build()
    )

    # Semua handler yang sudah ada tetap di sini
    application.add_handler(
        TypeHandler(Update, authorize_update),
        group=-1,
    )

    application.add_handler(CommandHandler("id", id_command))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("clear", clear_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("docker", docker_command))

    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("Telegram AI Agent started...")
    application.run_polling()

async def docker_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    result = await asyncio.to_thread(get_docker_status)
    await update.message.reply_text(result)

def clean_response(text: str) -> str:
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = text.replace("```", "")
    text = text.replace("`", "")
    return text.strip()