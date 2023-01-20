import os
import random
import urllib

import requests


def fetch_image_from_url(image_link, image_directory, image_name, params=None):
    """Скачивает картинку с интернета по ссылке по GET-запросу"""
    if params is None:
        params = {}
    if not os.path.exists(image_directory):
        os.makedirs(image_directory)
    response = requests.get(url=image_link, params=params)
    if response.ok:
        with open(os.path.join(os.path.abspath(image_directory), image_name), 'wb') as f:
            f.write(response.content)
    return


def fetch_file_extension_from_url(link):
    """Возвращает расширение файла из ссылки"""
    path = urllib.parse.urlsplit(link).path
    return os.path.splitext(path)[1]


def get_image_path_with_random_choice(path):
    """Возвращает случайный файл из папки"""
    photos_catalog = os.listdir(path)
    photo = random.choice(photos_catalog)
    return os.path.join(str(path), photo)
