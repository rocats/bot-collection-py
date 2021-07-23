#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import random

from telegram import Bot, Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext import (Updater, CommandHandler)

token = os.getenv('TELEGRAM_APITOKEN')
bot = Bot(token=token)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    print(context.error)


def start(update: Update, context: CallbackContext):
    update.message.reply_text('跟我们走一趟')


def question(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    reply_to_message_id = update.message.reply_to_message.message_id \
        if update.message.reply_to_message else None
    text = random.choice((
        "你发这些什么目的？",
        "谁指使你的？",
        "你的动机是什么？",
        "你取得有关部门许可了吗 ？",
        "法律法规容许你发了吗？",
        "你背后是谁？",
        "发这些想干什么？",
        "你想颠覆什么？",
        "你要破坏什么？"
    ))
    context.bot.send_message(chat_id, text=text, reply_to_message_id=reply_to_message_id)


def main():
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    # log all errors
    dp.add_error_handler(error)

    # add handler
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("question", question))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
