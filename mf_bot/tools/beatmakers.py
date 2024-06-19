from typing import LiteralString

from mf_bot import texts
from mf_bot.db import fetch_all, execute, fetch_one
from mf_bot.tools.battle import get_current_battle_id


async def get_beatmakers_from_last_battle():
    sql = ''' 
        SELECT battle_id, user_id, user_name
        FROM beatmaker 
        WHERE battle_id = :battle_id 
        AND EXISTS (
            SELECT 1 FROM beatmaker WHERE battle_id = :battle_id
        )
        ORDER BY id
        '''
    beatmakers = await fetch_all(
        sql, {'battle_id': await get_current_battle_id()}
    )
    return beatmakers 


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


async def beatmakers_did_vote(votes):
    beatmakers = [
        beatmaker['user_name'] for beatmaker 
        in await get_beatmakers_from_last_battle() 
    ]
    did_vote = {beatmaker: False for beatmaker in beatmakers}
    for vote in votes:
        if vote['user_name'] in beatmakers:
            did_vote[vote['user_name']] = True
    return did_vote 


async def enumerate_beatmakers() -> dict:
    beatmakers = await get_beatmakers_from_last_battle()
    enumerated_beatmakers = {} 
    for index, beatmaker in enumerate(beatmakers):
        enumerated_beatmakers[int(index)] = beatmaker
    return enumerated_beatmakers


async def get_betmakers_list_as_string():
    beatmakers = await enumerate_beatmakers()
    if not beatmakers:
        return texts.BEATMAKERS_LIST_IS_EMPTY 
    return texts.BEATMAKERS_LIST + '\n'.join(
        [
            f"{int(num) + 1}. {beatmaker['user_name']}" 
            for num, beatmaker in beatmakers.items()
        ]
    )


async def nums_to_beatmakers_id(nums: list) -> list | None:
    print(f'\n\n nums: {nums}')
    if not nums or 0 in nums:
        return None
    enumerated_beatmakers = await enumerate_beatmakers() 
    beatmakers_id = []
    for num in nums:
        num = int(num) - 1
        if num < 0 or num > max(enumerated_beatmakers.keys()):
            return None
        beatmaker_user_id = enumerated_beatmakers[num]['user_id']
        beatmakers_id.append(beatmaker_user_id)
    return beatmakers_id

