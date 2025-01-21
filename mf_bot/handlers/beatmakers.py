from telegram import Update
from telegram.ext import ContextTypes

from mf_bot.settings import CHAT_FOR_BEATS_ID
from mf_bot.tools import (
    validate_user,
    is_channel, 
    registration_as_beatmaker, 
    unregistration_as_beatmaker, 
    get_betmakers_list_as_string,
) 


async def is_battled(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    if not await is_channel(user_id) and chat_id == CHAT_FOR_BEATS_ID:
        reply_text = await registration_as_beatmaker(
            user_id=user_id,
            user_name=update.effective_user.full_name
        )
        await context.bot.send_message(chat_id=user_id,
                                       text=reply_text)


@validate_user(mode='admin')
async def insert_beatmaker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id, user_name = context.args[:2]
    reply_text = await registration_as_beatmaker(
        user_id=user_id,
        user_name=user_name
    ) 
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text=reply_text
    ) 


@validate_user(mode='admin')
async def remove_beatmaker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    users_num = [int(num) for num in context.args]
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text=await unregistration_as_beatmaker(users_num)
    )
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text=await get_betmakers_list_as_string()
    ) 


async def beatmakers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_text = await get_betmakers_list_as_string()
    await update.message.reply_text(text=reply_text)
  
