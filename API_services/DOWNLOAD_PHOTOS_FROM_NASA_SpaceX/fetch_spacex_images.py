import argparse

import requests

import tools


def fetch_spacex_images(image_directory, launch_id=''):
    """Скачиваем последние доступные фото с запуска SpaceX"""
    spacex_url = 'https://api.spacexdata.com/v5/launches/'
    response = requests.get(url=spacex_url)
    response.raise_for_status()
    launches = response.json()
    flights = []
    for launch in launches[::-1]:
        if launch['links']['flickr']['original']:
            flights.append(
                {
                    'launch_id': launch['id'],
                    'image_links': launch['links']['flickr']['original']
                }
            )
    if launch_id:
        for flight in flights:
            if launch_id == flight['launch_id']:
                for image_number, image_link in enumerate(flight['image_links'], start=1):
                    tools.fetch_image_from_url(image_link, image_directory, f'spacex_{image_number}.jpg')
    else:
        for image_number, image_link in enumerate(flights[0]['image_links'], start=1):
            tools.fetch_image_from_url(image_link, image_directory, f'spacex_{image_number}.jpg')
    return


def main():
    image_directory = './images'
    parser = argparse.ArgumentParser(description='Принимает id запуска SpaceX для загрузки изображения')
    parser.add_argument('-l', '--launch_id', help='Ввод ID')
    args = parser.parse_args()
    user_launch_id = args.launch_id
    return fetch_spacex_images(image_directory, launch_id=user_launch_id)


if __name__ == '__main__':
    main()
