from telegram import Update
from telegram.ext import ContextTypes

from mf_bot.tools import start_new_vote_process, validate_user


@validate_user(mode='admin')
async def start_vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        await start_new_vote_process(user_id=update.effective_user.id)
    )

