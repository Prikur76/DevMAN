import argparse
import logging
import os
import time
from datetime import datetime

import requests
from dotenv import load_dotenv
from telegram import Bot

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

logger = logging.getLogger(__name__)


def convert_datetime_to_string(isoformat_date):
    """Возвращает """
    return datetime.fromisoformat(isoformat_date).strftime("%d.%m.%Y %H:%M")


def get_message_for_chat(result_code_review):
    """Готовит информацию для публикации в tg"""
    message = "🔔🔔🔔\n" \
              "😊 Ура! 🎊 Преподаватель проверил вашу работу!🎉\n" \
             f"📃 Урок '{result_code_review['lesson_title']}' сдан!💪\n" \
             f"👀 Перейти к уроку: {result_code_review['lesson_url']}.\n" \
             f"🕦 {convert_datetime_to_string(result_code_review['submitted_at'])}"
    if result_code_review['is_negative']:
        message = f"🔔🔔🔔\n" \
                  f"😞 К сожалению, урок '{result_code_review['lesson_title']}' не пройден.👎\n" \
                  f"👀 Посмотрите код-ревью преподавателя: " \
                  f"{result_code_review['lesson_url']}.\n" \
                  f"🕦 {convert_datetime_to_string(result_code_review['submitted_at'])}"
    return message


def main():
    load_dotenv()
    dvmn_token = os.environ.get('DEVMAN_TOKEN')
    tg_token = os.environ.get('TG_TOKEN')
    chat_id = os.environ.get('CHAT_ID')

    long_polling_url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {dvmn_token}'}
    payload = {'timestamp': ''}

    bot = Bot(token=tg_token)

    parser = argparse.ArgumentParser(description='Получение уведомлений с сайта dvmn.org')
    parser.add_argument('chat_id', nargs='?', type=int, default=int(chat_id), help='Ввести chat_id')
    args = parser.parse_args()
    user_id = args.chat_id

    while True:
        try:
            response = requests.get(url=long_polling_url, params=payload, headers=headers, timeout=95)
            if response.json()['status'] == 'found':
                payload['timestamp'] = response.json()['last_attempt_timestamp']
                code_review = response.json()['new_attempts'][0]
                answer = get_message_for_chat(code_review)
                bot.sendMessage(chat_id=user_id, text=answer)

        except requests.exceptions.ConnectionError as connection_err:
            logger.error(f"No HTTP connection\n{connection_err}\n")
            time.sleep(60)
        except requests.exceptions.ReadTimeout as timeout_err:
            logger.error(f"Timeout error\n{timeout_err}\n")
            time.sleep(60)


if __name__ == '__main__':
    main()
