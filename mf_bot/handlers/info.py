from telegram import Update
from telegram.ext import ContextTypes

from mf_bot.texts import START, HELP, MENU


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=START)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=HELP)


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=MENU)

