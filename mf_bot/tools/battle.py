from mf_bot.db import fetch_one, execute


async def get_current_battle_id() -> int:
    battle_id = await fetch_one(
            f'SELECT MAX(battle_id) FROM battle WHERE is_open = 1'
    )
    return battle_id['MAX(battle_id)'] 


async def battle_is_open() -> bool:
    battle = await fetch_one(
        f"SELECT is_open FROM battle ORDER BY id DESC LIMIT 1"
    )
    return battle['is_open'] == 1 


async def start_new_battle(user_id: int) -> None:
    current_battle_id = await get_current_battle_id()
    if not current_battle_id:
        current_battle_id = 0
    await execute(
        f'''
        INSERT OR IGNORE INTO battle (beatmaker_host_id, battle_id, is_open) 
        VALUES (:beatmaker_host_id, :battle_id, :is_open)
        ''',
        {
            'beatmaker_host_id': user_id,
            'battle_id': current_battle_id + 1,
            'is_open': 1,
        },
    )

