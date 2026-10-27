import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import storage
from face_engine import extract_single_embedding, is_same_person

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

BOT_TOKEN = os.environ["BOT_TOKEN"]
PUBLIC_URL = os.environ["PUBLIC_URL"]   # Render-in verdiyi URL, məs: https://face-bot.onrender.com
PORT = int(os.environ.get("PORT", "10000"))

WELCOME = (
    "Salam! Bu bot yalnız öz üzünüzü qeydiyyatdan keçirmək və "
    "öz şəklinizlə yoxlama aparmaq üçündür.\n\n"
    "/register - öz üzünüzü qeydiyyatdan keçirin\n"
    "/verify - öz şəklinizlə yoxlayın\n"
    "/delete - məlumatınızı silin\n\n"
    "Şəkil göndərdikdə onun sizə aid olduğunu təsdiqləyirsiniz."
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME)


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mode"] = "register"
    await update.message.reply_text(
        "Zəhmət olmasa təkcə öz üzünüzün göründüyü aydın bir şəkil göndərin.\n"
        "Şəkil saxlanılmır, yalnız rəqəmsal üz xüsusiyyətləri saxlanılır."
    )


async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mode"] = "verify"
    await update.message.reply_text("Öz şəklinizi göndərin.")


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    removed = storage.delete_embedding(update.effective_user.id)
    msg = "Məlumatınız silindi." if removed else "Silinəcək məlumat tapılmadı."
    await update.message.reply_text(msg)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    mode = context.user_data.get("mode")

    if mode not in ("register", "verify"):
        await update.message.reply_text("Əvvəl /register və ya /verify əmri yazın.")
        return

    photo = update.message.photo[-1]
    file = await photo.get_file()
    image_bytes = bytes(await file.download_as_bytearray())

    embedding, err = extract_single_embedding(image_bytes)
    if err:
        await update.message.reply_text(err)
        return

    if mode == "register":
        storage.save_embedding(user_id, embedding)
        context.user_data["mode"] = None
        await update.message.reply_text("Qeydiyyat tamamlandı. Şəkil saxlanılmadı.")
        return

    # verify
    stored = storage.get_embedding(user_id)
    if stored is None:
        await update.message.reply_text("Əvvəl /register ilə qeydiyyatdan keçin.")
        return

    ok, dist = is_same_person(stored, embedding)
    context.user_data["mode"] = None
    if ok:
        await update.message.reply_text("Təsdiqləndi: şəkil qeydiyyatlı şəxsə aiddir.")
    else:
        await update.message.reply_text("Uyğunluq tapılmadı.")
    log.info("verify user=%s dist=%.3f ok=%s", user_id, dist, ok)


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("verify", verify))
    app.add_handler(CommandHandler("delete", delete))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Render üçün webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=f"{PUBLIC_URL}/{BOT_TOKEN}",
    )


if __name__ == "__main__":
    main()
