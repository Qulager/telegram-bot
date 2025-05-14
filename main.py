import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes

# Получение токена из переменной окружения
TOKEN = '8122607442:AAHdSnMj1ONIWEk8qTOdj4pE2hHAbvjQ47M'
CHANNEL_ID = '@qulager_director'

logging.basicConfig(level=logging.INFO)

# Выводим значение переменной окружения PORT
print(f"PORT = {os.getenv('PORT')}")

async def publish_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        await update.message.reply_text("Эта команда работает только в личке.")
        return

    if context.args:
        task_text = ' '.join(context.args)
    else:
        await update.message.reply_text("Укажи текст задания, например: /publish Сделать отчёт")
        return

    keyboard = [[InlineKeyboardButton("Выполнить", callback_data='execute_task')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=f"📝 *Задание:*\n{task_text}",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user.full_name

    await query.answer("Отмечено как выполнено!")
    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=f"✅ Задание выполнено: *{user}*",
        parse_mode='Markdown'
    )
    await query.edit_message_reply_markup(reply_markup=None)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("publish", publish_task))
    app.add_handler(CallbackQueryHandler(button_handler))
    logging.info("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
