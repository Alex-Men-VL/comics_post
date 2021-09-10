import logging
import os
from random import randint

import comics_processing
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, HTTPError, InvalidURL
from vk_post import post_comics_in_group


def main():
    load_dotenv()
    group_id = os.getenv('GROUP_ID')
    access_token = os.getenv('VK_TOKEN')
    api_version = 5.131

    try:
        comics_quantity = comics_processing.get_comics_quantity()
        comics_number = randint(1, comics_quantity)

        comics = comics_processing.download_comics(comics_number)
        comics_name = comics_processing.get_img_name(comics['img'])
        comics_comment = comics['alt']

        comics_processing.download_image(comics['img'], comics_name)
    except (ConnectionError, InvalidURL, HTTPError) as error:
        logging.error(f"{error}\nCan't get data from xkcd.com.")
    
    try:
        post_comics_in_group(comics_name, comics_comment, group_id,
                             access_token, api_version)
    except (ConnectionError, InvalidURL, HTTPError) as error:
        logging.error(f"{error}\nCan't get data from api.vk.com")
    finally:
        os.remove(comics_name)


if __name__ == '__main__':
    main()
