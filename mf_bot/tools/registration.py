from typing import LiteralString

from mf_bot import texts 
from mf_bot.tools import (
    is_in_mode, 
    is_beatmaker, 
    insert_in_mode,
    nums_to_beatmakers_id,
    insert_in_beatmaker, 
    remove_from_beatmaker, 
)
from mf_bot.tools.battle import get_current_battle_id, battle_is_open
from mf_bot.settings import ADMIN_PASSWORD
  

async def registration_as_beatmaker(user_id: int, user_name: LiteralString):
    battle_id = await get_current_battle_id()
    if not await battle_is_open():
        return texts.VOTE_TIME
    if await is_beatmaker(user_id=user_id, battle_id=battle_id):
        return texts.IS_ALREADY_BEATMAKER
    await insert_in_beatmaker(
        user_id=user_id, user_name=user_name, battle_id=battle_id
    )
    return texts.IS_BEATMAKER


async def unregistration_as_beatmaker(users_num: list):
    battle_id = await get_current_battle_id()
    users_id = await nums_to_beatmakers_id(users_num)
    if users_id is None:
        return texts.INVALID_ARGS
    for user_id in users_id:
        if not await is_beatmaker(user_id=user_id, battle_id=battle_id):
            return texts.NOT_FOUND
        await remove_from_beatmaker(
            user_id=user_id, battle_id=battle_id
        )
    return texts.DONE


async def registration_as_admin(user_id: int, password: str):
    if not password:
        return texts.INVALID_ARGS
    if password != ADMIN_PASSWORD:
        return texts.INVALID_PASSWORD
    mode = 'admin'
    if await is_in_mode(user_id=user_id, mode=mode):
        return texts.IS_ALREADY_LOGGED
    await insert_in_mode(user_id=user_id, mode=mode)
    return texts.IS_LOGGED

