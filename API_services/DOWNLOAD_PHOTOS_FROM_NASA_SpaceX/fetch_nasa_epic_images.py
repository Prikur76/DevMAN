import argparse
import os

import requests
from dotenv import load_dotenv

import tools


def get_nasa_epic_last_date(api_key):
    """Возвращает последнюю доступную дату"""
    payload = {
        'api_key': api_key
    }
    response = requests.get('https://api.nasa.gov/EPIC/api/natural/all', params=payload)
    response.raise_for_status()
    epic_dates = response.json()
    return epic_dates[0]['date']


def fetch_nasa_epic_images_ids(api_key, epic_date):
    """Собрать все id снимков в кортеж по дате формата YYYY-MM-dd"""
    payload = {
        'api_key': api_key
    }
    images_ids = []
    response = requests.get(f"https://api.nasa.gov/EPIC/api/natural/date/{epic_date}", params=payload)
    response.raise_for_status()
    epic_cards = response.json()
    for card in epic_cards:
        images_ids.append(card['image'])
    return images_ids


def get_nasa_epic_images_urls(images_ids):
    """Собираеn все ссылки в один кортеж, без атрибутов params"""
    epic_images_urls = []
    for image_id in images_ids:
        image_date = image_id.split('_')[-1]
        date_for_url = f"{image_date[0:4]}/{image_date[4:6]}/{image_date[6:8]}"
        image_url = f"https://api.nasa.gov/EPIC/archive/natural/{date_for_url}/png/{image_id}.png"
        epic_images_urls.append(image_url)
    return epic_images_urls


def fetch_nasa_epic_images(api_key, image_directory, epic_date=''):
    """Извлекаем фотографии Земли из NASA EPIC по дате"""
    if not epic_date:
        epic_date = get_nasa_epic_last_date(api_key)
    payload = {
        'api_key': api_key
    }
    images_ids = fetch_nasa_epic_images_ids(api_key, epic_date)
    epic_images_urls = get_nasa_epic_images_urls(images_ids)
    for image_number, image_url in enumerate(epic_images_urls, start=1):
        file_extension = tools.fetch_file_extension_from_url(image_url)
        tools.fetch_image_from_url(image_url,
                                   image_directory,
                                   f'nasa_epic_{image_number}{file_extension}',
                                   params=payload)
    return


def main():
    load_dotenv()
    api_key = os.environ.get('NASA_API_KEY')
    image_directory = './images'
    parser = argparse.ArgumentParser(description='Принимает количество загружаемых файлов')
    parser.add_argument('-ed', '--epic_date', help='Дата для загрузки в формате YYYY-MM-dd')
    args = parser.parse_args()
    user_epic_date = args.epic_date
    return fetch_nasa_epic_images(api_key, image_directory, epic_date=user_epic_date)


if __name__ == '__main__':
    main()
