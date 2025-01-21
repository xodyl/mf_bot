from telegram import Update
from telegram.ext import ContextTypes

from mf_bot.tools import validate_user, set_vote_process, count_vote_process


@validate_user(mode='beatmaker')
async def vote(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    reply_text = await set_vote_process(args=args, user_id=user_id, chat_id=chat_id)
    await context.bot.send_message(chat_id=user_id, text=reply_text) 


@validate_user(mode='admin')
async def count_vote(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_text = await count_vote_process() 
    await update.message.reply_text(text=reply_text, parse_mode='HTML') 

