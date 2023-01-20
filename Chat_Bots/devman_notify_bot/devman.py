import os
import requests

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def get_current_timestamp():
    """Возвращает текущую дату/время в формате timestamp"""
    current_date = datetime.now()
    return datetime.timestamp(current_date)


def get_all_reviews_from_dvmn(token):
    """Возвращает список проверок с сайта"""
    url_reviews = 'https://dvmn.org/api/user_reviews/'
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(url=url_reviews, headers=headers)
    response.raise_for_status()
    return response.json()


def get_long_polling(token):
    """Возвращает список проверок через Long Polling"""
    long_polling_url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {token}'}
    payload = {'timestamp': ''}

    while True:
        try:
            response = requests.get(url=long_polling_url, params=payload, headers=headers, timeout=95)
            if response.json()['status'] == 'found':
                payload['timestamp'] = response.json()['last_attempt_timestamp']
                print(response.json()['new_attempts'])
            else:
                payload['timestamp'] = response.json()['timestamp_to_request']
                # print(payload)
        except requests.exceptions.ConnectionError as connection_err:
            # print(f"No connection: {connection_err}")
            pass
        except requests.exceptions.ReadTimeout as timeout_err:
            print(f"Timeout error: {timeout_err}")


if __name__ == '__main__':
    token = os.environ.get('TOKEN')
    get_long_polling(token)
    
