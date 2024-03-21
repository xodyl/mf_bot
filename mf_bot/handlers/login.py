from telegram import Update
from telegram.ext import ContextTypes

from mf_bot.tools import registration_as_admin
from mf_bot.texts import INVALID_ARGS


async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(INVALID_ARGS)
        return 
    password = context.args[0]
    reply_text = await registration_as_admin(
        user_id=update.effective_user.id,
        password=password
    ) 
    await update.message.reply_text(reply_text)

