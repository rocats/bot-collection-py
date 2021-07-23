#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import random

from telegram import Bot, Update, ParseMode
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
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id, '`好`', parse_mode=ParseMode.MARKDOWN_V2)


def ok(update: Update, context: CallbackContext, name: str = None):
    text = random.choice(("好的", "行", "可以", "完全同意", "OK", "我觉得好", "好吧", "嗯！"))
    if name is not None:
        update.message.reply_text(f'{name}: {text}')
    else:
        chat_id = update.message.chat_id
        reply_to_message_id = update.message.reply_to_message.message_id \
            if update.message.reply_to_message else None
        context.bot.send_message(chat_id, text=text, reply_to_message_id=reply_to_message_id)


def study(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    reply_to_message_id = update.message.reply_to_message.message_id \
        if update.message.reply_to_message else None
    text = random.choice(("快去学习", "今天学了吗?", "今天学习了吗?", "啥时候学习?", "忘记学习了吗?", "快去学习啊"))
    context.bot.send_message(chat_id, text=text, reply_to_message_id=reply_to_message_id)


def assign(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if update.message.reply_to_message is not None:
        reply_to_message_id = update.message.reply_to_message.message_id
        context.bot.send_message(chat_id, '交 给 你 了', reply_to_message_id=reply_to_message_id)
        ok(update, context, update.message.reply_to_message.from_user.full_name)
    else:
        context.bot.send_message(chat_id, f'{update.message.from_user.full_name}: 交 给 我 了')


def unassign(update: Update, context: CallbackContext):
    name = update.message.reply_to_message.from_user.full_name \
        if update.message.reply_to_message is not None \
        else update.message.from_user.full_name
    update.message.reply_text(f'{name}: 不 干 了')


def main():
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    # log all errors
    dp.add_error_handler(error)

    # add handler
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ok", ok))
    dp.add_handler(CommandHandler("study", study))
    dp.add_handler(CommandHandler("assign", assign))
    dp.add_handler(CommandHandler("unassign", unassign))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
