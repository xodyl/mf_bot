from typing import LiteralString

from telegram import Update
from telegram.ext import ContextTypes

from mf_bot.db import execute, fetch_one
from mf_bot.tools.battle import get_current_battle_id
from mf_bot.texts import PERMISSION_DENIED
from mf_bot.settings import (
    BATTLE_CHANNEL_ID, 
    BATTLE_CHANNEL_AS_USER, 
)


def validate_user(mode):
    def wrapped(handler):
        async def called(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user_id = update.effective_user.id
            if mode == 'beatmaker':
                battle_id = await get_current_battle_id()
                if not await is_beatmaker(battle_id=battle_id, user_id=user_id):
                    await update.message.reply_text(text=PERMISSION_DENIED)
                    return
            if not await is_in_mode(user_id, mode):
                await update.message.reply_text(text=PERMISSION_DENIED)
                return
            await handler(update, context)
        return called 
    return wrapped



async def is_channel(user_id: int) -> bool:
    EXCEPTIONS = (BATTLE_CHANNEL_AS_USER, BATTLE_CHANNEL_ID)
    return user_id in EXCEPTIONS


async def insert_in_beatmaker(battle_id: int, user_id: int, 
                              user_name: LiteralString) -> None:
    sql = """
        INSERT OR IGNORE INTO beatmaker 
            (battle_id, user_id, user_name)
        VALUES (:battle_id, :user_id, :user_name) 
        """
    args = {
        "battle_id": battle_id,
        "user_id": user_id,
        "user_name": user_name
    }
    await execute(sql, args)


async def remove_from_beatmaker(battle_id: int, user_id: int, 
                              user_name: LiteralString) -> None:
    sql = """
        DELETE OR IGNORE FROM beatmaker 
            (battle_id, user_id, user_name)
        VALUES (:battle_id, :user_id, :user_name) 
        """
    args = {
        "battle_id": battle_id,
        "user_id": user_id,
        "user_name": user_name
    }
    await execute(sql, args)


async def is_beatmaker(battle_id: int, user_id:int) -> bool:
    sql = """
        SELECT 1 FROM beatmaker 
        WHERE battle_id = :battle_id AND user_id = :user_id
        """
    args = {
        "battle_id": battle_id,
        "user_id": user_id,
    }
    user_exists = await fetch_one(sql, args)
    return user_exists is not None


async def is_in_mode(user_id: int, mode: LiteralString) -> bool:
    user_exists = await fetch_one(
        f"SELECT user_id FROM {mode} WHERE user_id=:user_id",
        {"user_id": user_id},
    )
    return user_exists is not None


async def insert_in_mode(user_id: int, mode: LiteralString) -> None:
    await execute(
        f"INSERT OR IGNORE INTO {mode} (user_id) VALUES (:user_id)",
        {"user_id": user_id},
    )


async def remove_from_mode(user_id: int, mode: LiteralString) -> None:
    await execute(
        f"DELETE FROM {mode} WHERE user_id=:user_id",
        {"user_id": user_id},
        autocommit=False,
    )

