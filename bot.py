import logging
import nest_asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update

logging.basicConfig(level=logging.INFO)

nest_asyncio.apply()

TOKEN = '__'

user_list = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.username:
        user_list.add(user.username)
    await context.bot.send_message(chat_id=update.effective_chat.id, text='مرحبًا!')

async def tag_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not user_list:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='لا يوجد مستخدمون مسجلون بعد.')
        return
    mentions = ' '.join([f"@{username}" for username in user_list])
    await context.bot.send_message(chat_id=update.effective_chat.id, text=mentions)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.username:
        user_list.add(user.username)

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("all", tag_all))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

print("Bot is running...")
app.run_polling(drop_pending_updates=True)


