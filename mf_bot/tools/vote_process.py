from typing import List

from mf_bot.db import execute, fetch_all
from mf_bot import texts
from mf_bot.tools.battle import battle_is_open, get_current_battle_id
from mf_bot.tools.beatmakers import (
    beatmakers_did_vote,
    enumerate_beatmakers, 
    nums_to_beatmakers_id,
    get_betmakers_list_as_string,
    get_beatmakers_from_last_battle
)
from mf_bot.settings import EXPECTED_VOTE_ARGS_LEN, POINTS
 

async def expected_args_len(reality: int) -> bool:
    return EXPECTED_VOTE_ARGS_LEN == reality


async def has_duplicate(args) -> bool:
    return len(tuple(args)) != len(args)


async def self_vote(user_id, beatmakers_id) -> bool:
    return user_id in beatmakers_id


async def vote_in_beatmakers_range(args) -> bool:
    args_max = max([int(arg) - 1 for arg in args]) 
    beatmakers_max_i = max(
        [int(num) for num in await enumerate_beatmakers()]
    )
    return args_max <= beatmakers_max_i


async def start_new_vote(user_id: int) -> None:
    await execute(
        f'''
        INSERT OR IGNORE INTO battle (beatmaker_host_id, is_open) 
        VALUES (:beatmaker_host_id, :is_open)
        ''',
        {
            'beatmaker_host_id': user_id,
            'is_open': 0,
        },
    )


async def start_new_vote_process(user_id):
    if not battle_is_open():
        return texts.VOTE_IS_ALEREADY_OPEN
    await start_new_vote(user_id=user_id)
    return texts.VOTE_START + f'\n{await get_betmakers_list_as_string()}'


async def set_vote(user_id: int, beatmakers: list) -> None:
    first_beatmaker, second_beatmaker, third_beatmaker = beatmakers[:3]
    sql = ''' 
        INSERT OR REPLACE INTO vote
            (battle_id, user_id, first_beatmaker, second_beatmaker, third_beatmaker)
        VALUES (:battle_id, :user_id, :first_beatmaker, :second_beatmaker, :third_beatmaker)
       
        '''
    await execute(
        sql,
        {
            'battle_id': await get_current_battle_id(), 
            'user_id': user_id,
            'first_beatmaker': first_beatmaker,
            'second_beatmaker': second_beatmaker,
            'third_beatmaker': third_beatmaker,
        }
    )


async def set_vote_process(args: List[str], user_id: int) -> str:
    if await battle_is_open():
        return texts.BATTLE_TIME
    if not args or not await expected_args_len(len(args)):
        return texts.INVALID_ARGS
    if await has_duplicate(args): 
        return texts.HAS_DUPLICATE
    if not await vote_in_beatmakers_range(args=args):
        return texts.OUT_OF_RANGE
    beatmakers_id = await nums_to_beatmakers_id(args)
    if await self_vote(user_id, beatmakers_id):
        return texts.SELF_VOTE
    await set_vote(user_id=user_id, beatmakers=beatmakers_id)
    return texts.VOTE_ACCEPTED


async def get_votes_from_last_battle():
    sql = '''
        SELECT v.battle_id, v.user_id,
           b1.user_id AS first_beatmaker_id, b1.user_name AS first_beatmaker_name,
           b2.user_id AS second_beatmaker_id, b2.user_name AS second_beatmaker_name,
           b3.user_id AS third_beatmaker_id, b3.user_name AS third_beatmaker_name,
           b4.user_name AS user_name
        FROM vote v
        INNER JOIN 
            beatmaker b1 ON v.first_beatmaker = b1.user_id AND v.battle_id = b1.battle_id
        INNER JOIN 
            beatmaker b2 ON v.second_beatmaker = b2.user_id AND v.battle_id = b2.battle_id
        INNER JOIN 
            beatmaker b3 ON v.third_beatmaker = b3.user_id AND v.battle_id = b3.battle_id
        INNER JOIN 
            beatmaker b4 ON v.user_id = b4.user_id AND v.battle_id = b4.battle_id
        WHERE v.battle_id = :battle_id 
        ORDER BY v.id
        '''
    votes = await fetch_all(
        sql, {'battle_id': await get_current_battle_id()}
    )
    return votes 


async def who_did_not_vote_text(did_vote) -> str:
    return texts.SOME_BEATMAKER_DID_NOT_VOTE + '\n'.join(
        f'{i}. {"<s>" + name + "</s>" if vote_status else name}'
        for i, (name, vote_status) in enumerate(did_vote.items(), start=1)
    )


async def update_rank(votes, rank) -> None:
    for vote in votes:
        for key in ['first_beatmaker_name', 'second_beatmaker_name', 
                    'third_beatmaker_name']:
            rank[vote[key]] += POINTS[key]
    return rank


async def count_vote_process():

    if await battle_is_open():
        return texts.BATTLE_TIME

    votes = await get_votes_from_last_battle()
    did_vote = await beatmakers_did_vote(votes)

    if False in did_vote.values():
       return await who_did_not_vote_text(did_vote) 
    
    beatmakers = await get_beatmakers_from_last_battle()

    rank = {beatmaker['user_name']: 0 for beatmaker in beatmakers}
    rank = await update_rank(votes=votes, rank=rank) 
       
    return texts.COUNTED_VOTES + '\n'.join(
        [f'{name}: {points}' for name, points 
         in sorted(rank.items(), key=lambda item: item[1], reverse=True)]
    )

