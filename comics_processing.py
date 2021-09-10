import os
import urllib.parse

import requests


def download_comics(comics_number):
    url = f'https://xkcd.com/{comics_number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()

    return response.json()


def get_img_name(url):
    image_path = urllib.parse.unquote(urllib.parse.urlsplit(url).path)
    image_name = os.path.split(image_path)[-1]
    return image_name


def get_img(url, name, path):
    response = requests.get(url)
    response.raise_for_status()

    img_raw = response.content
    with open(f'{path}/{name}', 'wb') as file:
        file.write(img_raw)


def get_comics_quantity():
    last_comics_url = 'https://xkcd.com/info.0.json'
    response = requests.get(last_comics_url)
    response.raise_for_status()

    comics_quantity = response.json()['num']
    return comics_quantity
