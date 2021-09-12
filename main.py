import logging
import os
from random import randint

import comics_processing
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, HTTPError, InvalidURL
from vk_post import post_comics_in_group, VkApiError


def main():
    load_dotenv()
    group_id = os.getenv('GROUP_ID')
    access_token = os.getenv('VK_TOKEN')
    api_version = 5.131

    try:
        comics_quantity = comics_processing.get_comics_quantity()
        comics_number = randint(1, comics_quantity)
    except (ConnectionError, InvalidURL, HTTPError) as err:
        logging.error(f"{err}\nCan't get data from "
                      "https://xkcd.com/info.0.json.")

    try:
        comics = comics_processing.get_comics(comics_number)
        comics_name = comics_processing.get_image_name(comics['img'])
        comics_comment = comics['alt']
        image_url = comics['img']
    except (ConnectionError, InvalidURL, HTTPError) as err:
        logging.error(f"{err}\nCan't get data from "
                      f"https://xkcd.com/{comics_number}/info.0.json.")

    try:
        comics_processing.download_image(image_url, comics_name)
    except (ConnectionError, InvalidURL, HTTPError) as err:
        logging.error(f"{err}\nCan't load image from {image_url}.")
        return

    try:
        post_comics_in_group(comics_name, comics_comment, group_id,
                             access_token, api_version)
    except (ConnectionError, InvalidURL, HTTPError) as err:
        logging.error(f"{err}\nCan't get data from api.vk.com")
    except VkApiError as err:
        logging.error(err)
    finally:
        os.remove(comics_name)


if __name__ == '__main__':
    main()
