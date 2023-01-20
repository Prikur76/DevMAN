import argparse
import os
import random
import time

import telegram
from dotenv import load_dotenv
import tools

def publish_text_to_channel(bot, channel_chat_id, text):
    bot.send_message(chat_id=channel_chat_id, text=text)


def publish_image_to_channel_from_url(bot, channel_chat_id, image_url):
    bot.send_document(chat_id=channel_chat_id, document=image_url)


def publish_image_file_to_channel(bot, channel_chat_id, image_path):
    bot.send_document(chat_id=channel_chat_id, document=open(image_path, 'rb'))


def is_image_in_catalog(image_catalog, image_name):
    """Проверяет наличие файла в каталоге, возвращает True или False"""
    images_rosters = os.listdir(image_catalog)
    return image_name in images_rosters


def main():
    load_dotenv()
    token = os.environ.get('TG_TOKEN')
    channel_chat_id = os.environ.get('CHANNEL_CHAT_ID')
    bot = telegram.Bot(token=token)

    parser = argparse.ArgumentParser()
    parser.add_argument('-rs', '--rotation_seconds',
                        help='Количество секунд для ротации выгрузки файлов в канал',
                        type=int, default=14400)
    parser.add_argument('-f', '--file',
                        help='Файл для выгрузки в канал', default=None)
    args = parser.parse_args()
    user_rotation_seconds = args.rotation_seconds
    user_file = args.file

    photos_catalog = 'images'
    photos_rosters = os.listdir(photos_catalog)

    if user_file:
        if is_image_in_catalog(photos_catalog, user_file):
            photo_roster = os.path.join(str(photos_catalog), user_file)
            publish_image_file_to_channel(bot, channel_chat_id, photo_roster)
            time.sleep(user_rotation_seconds)
        else:
            photo_roster = tools.get_image_path_with_random_choice(photos_catalog)
            publish_image_file_to_channel(bot, channel_chat_id, photo_roster)
            time.sleep(user_rotation_seconds)

    while True:
        for photo in photos_rosters:
            photo_roster = os.path.join(str(photos_catalog), photo)
            publish_image_file_to_channel(bot, channel_chat_id, photo_roster)
            time.sleep(user_rotation_seconds)
        random.shuffle(photos_rosters)


if __name__ == '__main__':
    main()
