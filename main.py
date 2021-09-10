import argparse
import logging
import os
import shutil
from pathlib import Path
from random import randint

import comics_processing
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, HTTPError, InvalidURL
from vk_post import publish_comics


def parse_arguments():
    parser = argparse.ArgumentParser(description='Post comics in the vk group.')
    parser.add_argument('--path', '-p',
                        help='Enter the path to the folder where '
                             'the images will be saved.',
                        default='images')
    return parser.parse_args()


def main():
    load_dotenv()
    group_id = os.getenv('GROUP_ID')
    access_token = os.getenv('VK_TOKEN')
    api_version = 5.131

    path = parse_arguments().path
    Path(path).mkdir(parents=True, exist_ok=True)

    try:
        comics_quantity = comics_processing.get_comics_quantity()
        comics_number = randint(1, comics_quantity)

        comics = comics_processing.download_comics(comics_number)
        comics_name = comics_processing.get_img_name(comics['img'])
        comics_comment = comics['alt']

        comics_processing.get_img(comics['img'], comics_name, path)
    except (ConnectionError, InvalidURL, HTTPError) as error:
        logging.error(f"{error}\nCan't get data from xkcd.com.")
    
    try:
        publish_comics(comics_name, path, comics_comment, group_id,
                       access_token, api_version)
    except (ConnectionError, InvalidURL, HTTPError) as error:
        logging.error(f"{error}Can't get data from api.vk.com")

    shutil.rmtree(path)


if __name__ == '__main__':
    main()
