import requests


def get_upload_url(group_id, access_token, api_version):
    vk_url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'group_id': group_id,
        'access_token': access_token,
        'v': api_version,
    }
    response = requests.get(vk_url, params=params)
    response.raise_for_status()

    upload_url = response.json()['response']['upload_url']
    return upload_url


def upload_comics_on_server(comics_name, upload_url):
    with open(comics_name, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
        response.raise_for_status()

    server, photo, image_hash = list(response.json().values())
    return server, photo, image_hash


def save_comics_in_album(
        server, photo, image_hash, group_id,
        access_token, api_version):
    vk_url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'group_id': group_id,
        'access_token': access_token,
        'server': server,
        'photo': photo,
        'hash': image_hash,
        'v': api_version,
    }
    response = requests.post(vk_url, params=params)
    response.raise_for_status()

    response_raw = response.json()['response'][0]
    media_id, owner_id = response_raw['id'], response_raw['owner_id']
    return media_id, owner_id


def publish_comics(comment, group_id, access_token, api_version,
                   media_id, owner_id):
    vk_url = 'https://api.vk.com/method/wall.post'
    attachments = f'photo{owner_id}_{media_id}'
    params = {
        'access_token': access_token,
        'owner_id': f'-{group_id}',
        'from_group': 1,  # publish on behalf of the group
        'attachments': attachments,
        'message': comment,
        'v': api_version,
    }
    response = requests.post(vk_url, params=params)
    response.raise_for_status()


def post_comics_in_group(comics_name, comics_comment, group_id, access_token,
                         api_version):
    upload_url = get_upload_url(group_id, access_token, api_version)
    server, photo, image_hash = upload_comics_on_server(
        comics_name, upload_url)
    media_id, owner_id = save_comics_in_album(server, photo, image_hash,
                                              group_id, access_token,
                                              api_version)

    publish_comics(comics_comment, group_id, access_token, api_version,
                   media_id, owner_id)
