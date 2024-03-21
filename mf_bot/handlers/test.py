from telegram import Update
from telegram.ext import ContextTypes


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    print(f'\n\nUSER ID: {user_id}\n\n')
    print(f'\n\nCHAT ID: {chat_id}\n\n')
    await update.message.reply_text(text=f'user_id: {user_id} CHAT ID: {chat_id}')

