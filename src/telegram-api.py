import logging
import json
from telegram import Update
from inference import main
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


async def get_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_file = await context.bot.get_file(update.message.photo[-1].file_id)
    image_hash = abs(hash(update.message.photo[-1].file_id))
    input_name = f"{image_hash}.jpeg"
    await new_file.download_to_drive(custom_path=f"inputs/{image_hash}.jpeg")
    main(input_name)
    output_name = f"results/restored_imgs/{image_hash}.jpeg"
    await context.bot.send_document(chat_id=update.effective_chat.id, document=output_name)


with open('token.json', 'r') as f:
    creds = json.load(f)

application = ApplicationBuilder().token(creds["token"]).build()

start_handler = CommandHandler('start', start)
application.add_handler(start_handler)

photo_handler = MessageHandler(filters.PHOTO, get_photo)
application.add_handler(photo_handler)

unknown_handler = MessageHandler(filters.COMMAND, unknown)
application.add_handler(unknown_handler)

application.run_polling()
