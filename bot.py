import os
import logging
import nest_asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, ChatMemberHandler, filters, ContextTypes
from telegram import Update, ChatMember
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

nest_asyncio.apply()

TOKEN = os.getenv("TOKEN_API")

user_list = set()

# start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.username:
        user_list.add(user.username)
    await update.message.reply_text("مرحبًا!")

# tagging all collected users
async def tag_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not user_list:
        await update.message.reply_text("لا يوجد مستخدمون مسجلون بعد.")
        return
    mentions = ' '.join([f"@{username}" for username in user_list])
    await update.message.reply_text(mentions)

# collecting usernames when sending messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    print(user.username)
    if user.username:
        user_list.add(user.username)

# collecting username when a user is added
async def chat_member_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_member: ChatMember = update.chat_member.new_chat_member
    user = chat_member.user
    if user.username:
        user_list.add(user.username)

app = Application.builder().token(TOKEN).build()

# command handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("all", tag_all))
app.add_handler(MessageHandler(filters.ALL, handle_message))
app.add_handler(ChatMemberHandler(chat_member_update, ChatMemberHandler.CHAT_MEMBER))

# running bot
print("Bot is running...")
app.run_polling(drop_pending_updates=True)


