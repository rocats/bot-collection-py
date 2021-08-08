#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import binascii
import hashlib
import logging
import os
import random

from telegram import Bot, Update, InlineQueryResultArticle, InputTextMessageContent, InlineQueryResult
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext import Updater, CommandHandler, InlineQueryHandler, ChosenInlineResultHandler, PicklePersistence

token = os.getenv('TELEGRAM_APITOKEN')
asset_url = os.getenv('ASSET_URL', 'https://raw.githubusercontent.com/rocats/bot-collection-py/master/asset/shuibiao')
data_path = os.getenv('DATA_PATH', os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'shuibiao'))
questions_file = os.getenv('QUESTIONS_PATH',
                           os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                        'asset', 'shuibiao', 'shuibiao.txt'))
bot = Bot(token=token)

questions_list = []
questions_dict = {}
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def init():
    logger.info(f'Get question list from {questions_file}')
    with open(questions_file) as f:
        for line in f:
            try:
                q = base64.standard_b64decode(line).decode()
                logger.info('Load a question: %s', q)
                questions_list.append(q)
                questions_dict[hashlib.md5(q.encode()).hexdigest()] = q
            except binascii.Error:
                logger.warning('Load question error from \'%s\'', line)


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
    text = random.choice(questions_list)
    context.bot_data[text] = context.bot_data.get(text, 0) + 1
    context.bot.send_message(chat_id, text=text, reply_to_message_id=reply_to_message_id)


def question_inline(update: Update, context: CallbackContext):
    texts = random.sample(questions_list, 3)
    result = [
        InlineQueryResultArticle(
            id=hashlib.md5(text.encode()).hexdigest(),
            title='我们建议你配合调查',
            description=text,
            input_message_content=InputTextMessageContent(text),
            thumb_url=f'{asset_url}/shuibiao.jpg'
        )
        for text in texts
    ]
    update.inline_query.answer(result, cache_time=0)


def chosen_result(update: Update, context: CallbackContext):
    text = questions_dict[update.chosen_inline_result.result_id]
    context.bot_data[text] = context.bot_data.get(text, 0) + 1


def shuibiaostats(update: Update, context: CallbackContext):
    total = sum(context.bot_data.values())
    total_items = len(context.bot_data)
    result = f'据不完全统计，目前全网累计查水表次数: {total} 次。其中排名前 3 的语句为：\n'
    top3 = sorted(list((-v, k) for k, v in context.bot_data.items()))[:min(3, total_items)]
    for count, text in top3:
        result += f"{text}: {-count} 次\n"
    update.message.reply_text(result)


def main():
    persistence = PicklePersistence(filename=data_path)
    updater = Updater(token, use_context=True, persistence=persistence)
    dp = updater.dispatcher

    # log all errors
    dp.add_error_handler(error)

    # add handler
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("question", question))
    dp.add_handler(CommandHandler("shuibiaostats", shuibiaostats))
    dp.add_handler(InlineQueryHandler(question_inline))
    dp.add_handler(ChosenInlineResultHandler(chosen_result))
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    init()
    main()
