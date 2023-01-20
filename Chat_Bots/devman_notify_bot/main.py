import os
import requests
import argparse

from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

def shorten_link(token, url):
    """Возвращает короткую ссылку"""
    headers = {
        'Authorization': f'Bearer {token}',
    }
    bitly_url = 'https://api-ssl.bitly.com/v4/shorten'
    payload = {
        'long_url': url,
    }
    response = requests.post(bitly_url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()['link']


def count_clicks(token, url):
    """Возвращает количество кликов за весь период"""
    link_parts = urlparse(url)
    bitlink = f'{link_parts.netloc}{link_parts.path}'
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    params = (
        ('unit', 'day'),
        ('units', '-1'),
    )
    response = requests.get(url=url, headers=headers, params=params)
    response.raise_for_status()
    clicks_count = response.json()['total_clicks']
    return clicks_count


def is_bitlink(token, url):
    """Возвращает True или False проверки битлинка"""
    headers = {
        'Authorization': f'Bearer {token}',
    }
    link_parts = urlparse(url)
    bitlink_id = f'{link_parts.netloc}{link_parts.path}'
    bitly_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink_id}'
    response = requests.get(bitly_url, headers=headers)
    return response.ok


def main():
    token = os.environ.get('BITLY_TOKEN')
    # user_input = input('Введите ссылку: ').strip()
    parser = argparse.ArgumentParser(description='Принимает url для проверки')
    parser.add_argument('link', help='Ввод URL')
    args = parser.parse_args()
    user_input = args.link

    try:
        if is_bitlink(token, user_input):
            print(f'Количество переходов по ссылке: {count_clicks(token, user_input)}')
        else:
            print(shorten_link(token, user_input))
    except requests.exceptions.HTTPError as error:
        print(f'Недействительная ссылка: {user_input}\n{error}')


if __name__ == "__main__":
    main()
