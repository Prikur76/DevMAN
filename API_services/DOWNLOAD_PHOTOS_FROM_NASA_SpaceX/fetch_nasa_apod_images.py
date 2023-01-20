import argparse
import os

import requests
from dotenv import load_dotenv

import tools


def fetch_nasa_apod_images(api_key, image_directory, count=1):
    """Скачиваем фотографии APOD с сайта NASA"""
    nasa_apod_url = 'https://api.nasa.gov/planetary/apod'
    payload = {
        'api_key': api_key,
        'count': count,
    }
    response = requests.get(url=nasa_apod_url, params=payload)
    response.raise_for_status()
    mediafiles = response.json()
    for image_number, image in enumerate(mediafiles, start=1):
        if image['media_type'] == 'image':
            file_extension = tools.fetch_file_extension_from_url(image['url'])
            tools.fetch_image_from_url(image['url'], image_directory, f'nasa_apod_{image_number}{file_extension}')

    return


def main():
    load_dotenv()
    api_key = os.environ.get('NASA_API_KEY')
    image_directory = './images'
    parser = argparse.ArgumentParser(description='Принимает количество загружаемых файлов')
    parser.add_argument('-c', '--count', help='Количество файлов для загрузки', type=int, default=1)
    args = parser.parse_args()
    user_count = args.count
    return fetch_nasa_apod_images(api_key, image_directory, count=user_count)


if __name__ == '__main__':
    main()
