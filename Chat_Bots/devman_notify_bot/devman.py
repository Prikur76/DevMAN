import os
import sys
from datetime import datetime
import logging

import requests
from dotenv import load_dotenv
import time

from telegram import Update, Bot
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    CallbackQueryHandler
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hello, {user.mention_markdown_v2()}\!',
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Используйте /start для теста бота')


def get_message_for_chat(result_code_review):
    """Готовит информацию для публикации в tg"""
    answer = 'урок пройден'
    if result_code_review['is_negative']:
        answer = 'урок не пройден, есть улучшения.'

    message = f"Урок: {result_code_review['lesson_title']}\n" \
              f"Дата: {result_code_review['submitted_at']}\n" \
              f"Результат: {answer}.\n"
    return message

def bop(bot, update):
    message = get_message_for_chat(result_code_review)
    chat_id = update.message.chat_id
    bot.sendMessage(chat_id=chat_id, text=message)


def get_current_timestamp():
    """Возвращает текущую дату/время в формате timestamp"""
    current_date = datetime.now()
    return datetime.timestamp(current_date)


def get_all_reviews_from_dvmn(token, page=1):
    """Возвращает список проверок с сайта с обычным запросом"""
    url_reviews = 'https://dvmn.org/api/user_reviews/'
    payload = {
        'page': page
    }
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(url=url_reviews, headers=headers, params=payload)
    response.raise_for_status()
    return response.json()


# def get_long_polling(token):
#     """Возвращает список проверок через Long Polling
#
#     Пример ответа:
#     [{'submitted_at': '2023-02-20T13:32:53.152523+03:00',
#     'timestamp': 1676889173.152523,
#     'is_negative': True,
#     'lesson_title': 'Отправляем уведомления о проверке работ',
#     'lesson_url': 'https://dvmn.org/modules/chat-bots/lesson/devman-bot/'}]
#     """
#     long_polling_url = 'https://dvmn.org/api/long_polling/'
#     headers = {'Authorization': f'Token {token}'}
#     payload = {'timestamp': ''}
#
#     while True:
#         try:
#             response = requests.get(url=long_polling_url, params=payload, headers=headers, timeout=95)
#             if response.json()['status'] == 'found':
#                 payload['timestamp'] = response.json()['last_attempt_timestamp']
#                 result_code_review = response.json()['new_attempts'][0]
#                 # print(result_code_review)
#                 # return result_code_review
#         except requests.exceptions.ConnectionError as connection_err:
#             logger.error(f"No HTTP connection\n{connection_err}\n")
#             time.sleep(60)
#         except requests.exceptions.ReadTimeout as timeout_err:
#             logger.error(f"Timeout error\n{timeout_err}\n")
#             time.sleep(60)
#
#
#     updater = Updater(token=tg_token)
#     dispatcher = updater.dispatcher
#     dispatcher.add_handler(CommandHandler("start", start))
#     dispatcher.add_handler(CommandHandler("help", help_command))
#
#     updater.start_polling()
#     updater.idle()


def main():
    load_dotenv()

    dvmn_token = os.environ.get('DEVMAN_TOKEN')
    long_polling_url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {dvmn_token}'}
    payload = {'timestamp': ''}

    tg_token = os.environ.get('TG_TOKEN')
    bot = Bot(token=tg_token)
    updater = Updater(token=tg_token)
    dispatcher = updater.dispatcher
    # chat_id = update.message.chat_id

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # result_code_review = ''
    # bot.sendMessage(chat_id=283111606, text=get_message_for_chat(result_code_review))

    while True:

        try:
            response = requests.get(url=long_polling_url, params=payload, headers=headers, timeout=95)
            if response.json()['status'] == 'found':
                payload['timestamp'] = response.json()['last_attempt_timestamp']
                answer = get_message_for_chat(response.json()['new_attempts'][0])
                bot.sendMessage(chat_id=283111606, text=answer)

        except requests.exceptions.ConnectionError as connection_err:
            logger.error(f"No HTTP connection\n{connection_err}\n")
            time.sleep(60)
        except requests.exceptions.ReadTimeout as timeout_err:
            logger.error(f"Timeout error\n{timeout_err}\n")
            time.sleep(60)

        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
   main()
