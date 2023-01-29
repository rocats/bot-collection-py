#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import logging
import os
import random
from typing import Optional

from telegram import Bot, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CallbackContext, CommandHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


async def error(update: Update, context: CallbackContext) -> None:
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    print(context.error)


async def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    await context.bot.send_message(chat_id, '`好`', parse_mode=ParseMode.MARKDOWN_V2)


async def ok(update: Update, context: CallbackContext, name: Optional[str] = None) -> None:
    text = random.choice(("好的", "行", "可以", "完全同意", "OK", "我觉得好", "好吧", "嗯！"))
    if name is not None:
        await update.message.reply_text(f'{name}: {text}')
    else:
        chat_id = update.message.chat_id
        reply_to_message_id = update.message.reply_to_message.message_id \
            if update.message.reply_to_message else None
        await context.bot.send_message(chat_id, text=text, reply_to_message_id=reply_to_message_id)


async def study(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    reply_to_message_id = update.message.reply_to_message.message_id \
        if update.message.reply_to_message else None
    text = random.choice(("快去学习", "今天学了吗?", "今天学习了吗?", "啥时候学习?", "忘记学习了吗?", "快去学习啊"))
    await context.bot.send_message(chat_id, text=text, reply_to_message_id=reply_to_message_id)


async def assign(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    if update.message.reply_to_message is not None:
        reply_to_message_id = update.message.reply_to_message.message_id
        await context.bot.send_message(chat_id, '交 给 你 了', reply_to_message_id=reply_to_message_id)
        await ok(update, context, update.message.reply_to_message.from_user.full_name)
    else:
        await context.bot.send_message(chat_id, f'{update.message.from_user.full_name}: 交 给 我 了',
                                       message_thread_id=update.message.message_thread_id)


async def unassign(update: Update, context: CallbackContext) -> None:
    name = update.message.reply_to_message.from_user.full_name \
        if update.message.reply_to_message is not None \
        else update.message.from_user.full_name
    await update.message.reply_text(f'{name}: 不 干 了')


def main():

    async def set_commands(app: Application):
        await app.bot.set_my_commands([
            ('assign', '交给你了'),
            ('unassign', '不干了'),
            ('ok', '好的，没问题'),
            ('study', '快去学习')
        ])

    token = os.getenv('TELEGRAM_APITOKEN')
    app = Application.builder().token(token) \
        .post_init(set_commands) \
        .build()



    # log all errors
    app.add_error_handler(error)

    # add handler
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ok", ok))
    app.add_handler(CommandHandler("study", study))
    app.add_handler(CommandHandler("assign", assign))
    app.add_handler(CommandHandler("unassign", unassign))

    # Start the Bot
    app.run_polling()


if __name__ == '__main__':
    main()
