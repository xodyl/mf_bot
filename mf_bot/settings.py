import os
from pathlib import Path

from dotenv import load_dotenv 


load_dotenv()


TELEGRAM_TOKEN: str = os.getenv('TELEGRAM_TOKEN')
ADMIN_PASSWORD: str = os.getenv('ADMIN_PASS')

BATTLE_CHANNEL_AS_USER: int = int(os.getenv('BATTLE_CHANNEL_AS_USER'))
BATTLE_CHANNEL_ID: int = int(os.getenv('BATTLE_CHANNEL_ID'))
CHAT_FOR_BEATS_ID: int = int(os.getenv('CHAT_FOR_BEATS_ID'))

ADMIN_MODE: str = 'admin'
BEATMAKER_MODE: str = 'beatmaker'
EXPECTED_VOTE_ARGS_LEN: int = 3

BASE_DIR = Path(__file__).resolve().parent
SQLITE_DB_FILE = BASE_DIR / 'db.sqlite3'

POINTS: dict = {
    'first_beatmaker_name': 5, 
    'second_beatmaker_name': 3, 
    'third_beatmaker_name': 1,
}

