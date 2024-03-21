import logging

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
)

from mf_bot import settings, handlers 
from mf_bot.db import close_db


COMMAND_HANDLERS = {
    "start": handlers.start, 
    "help": handlers.help,
    "menu": handlers.menu,
    "login": handlers.login,
    "beatmakers": handlers.beatmakers,  
    'insert': handlers.insert_beatmaker,
    "start_battle": handlers.start_battle, 
    "start_vote": handlers.start_vote, 
    "count": handlers.count_vote, 
    "vote": handlers.vote,
}


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


if not settings.TELEGRAM_TOKEN or not settings.BATTLE_CHANNEL_ID:
    raise ValueError(
        "TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID env variables "
        "wasn't implemented in .env (both should be initialized)."
    )

def main():

    application = ApplicationBuilder().token(settings.TELEGRAM_TOKEN).build()

    for command_name, command_handler in COMMAND_HANDLERS.items():
        application.add_handler(CommandHandler(command_name, command_handler))

    application.add_handler(
        MessageHandler(filters.AUDIO & filters.ChatType.GROUPS, handlers.is_battled)
    )

    application.run_polling()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback
        logger.warning(traceback.format_exc())
    finally:
        close_db()
