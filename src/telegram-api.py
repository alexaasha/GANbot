import json
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

from inference import main

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

example_text = "/example"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [[InlineKeyboardButton("example", callback_data=example_text)]]
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, I can improve quality of"
                                                                          " faces on photo! Press button to get "
                                                                          "an example.",
                                   reply_markup=InlineKeyboardMarkup(buttons))


async def get_example(update: Update, context: ContextTypes.DEFAULT_TYPE):
    example_pic = 'inputs/example.jpg'
    if example_text in update.callback_query.data:
        await context.bot.send_document(chat_id=update.effective_chat.id, document=example_pic)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


async def get_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_file = await context.bot.get_file(update.message.photo[-1].file_id)
    image_hash = abs(hash(update.message.photo[-1].file_id))
    input_name = f"{image_hash}.jpeg"
    await new_file.download_to_drive(custom_path=f"inputs/{input_name}")
    main(input_name)
    output_name = f"results/restored_imgs/{input_name}"
    await context.bot.send_document(chat_id=update.effective_chat.id, document=output_name)


with open('src/token.json', 'r') as f:
    creds = json.load(f)

application = ApplicationBuilder().token(creds["token"]).build()

start_handler = CommandHandler('start', start)
application.add_handler(start_handler)

example_handler = CallbackQueryHandler(get_example)
application.add_handler(example_handler)

photo_handler = MessageHandler(filters.PHOTO, get_photo)
application.add_handler(photo_handler)

unknown_handler = MessageHandler(filters.COMMAND, unknown)
application.add_handler(unknown_handler)

application.run_polling()
