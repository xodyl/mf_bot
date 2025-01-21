from telegram import Update
from telegram.ext import ContextTypes

from mf_bot.tools import start_new_battle, validate_user
from mf_bot.texts import BATTLE_START


@validate_user(mode='admin')
async def start_battle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    await start_new_battle(user_id=user_id)
    await update.message.reply_text(BATTLE_START)

