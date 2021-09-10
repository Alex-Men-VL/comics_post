import requests


def get_upload_url(group_id, access_token, API_version):
    vk_url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'group_id': group_id,
        'access_token': access_token,
        'v': API_version,
    }
    response = requests.get(vk_url, params=params)
    response.raise_for_status()

    upload_url = response.json()['response']['upload_url']
    return upload_url


def upload_comics_on_server(comics, path, group_id, access_token, API_version):
    upload_url = get_upload_url(group_id, access_token, API_version)
    with open(f'{path}/{comics}', 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
        response.raise_for_status()

        response_fields = list(response.json().values())
        return response_fields


def save_comics_in_album(comics, path, group_id, access_token, API_version):
    server, photo, hash = upload_comics_on_server(comics, path, group_id,
                                                  access_token, API_version)
    vk_url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'group_id': group_id,
        'access_token': access_token,
        'server': server,
        'photo': photo,
        'hash': hash,
        'v': API_version,
    }
    response = requests.post(vk_url, params=params)
    response.raise_for_status()

    response_raw = response.json()['response'][0]
    return response_raw['id'], response_raw['owner_id']


def publish_comics(comics, path, comment, group_id, access_token, API_version):
    media_id, owner_id = save_comics_in_album(comics, path, group_id,
                                              access_token, API_version)
    vk_url = 'https://api.vk.com/method/wall.post'
    attachments = f'photo{owner_id}_{media_id}'
    params = {
        'access_token': access_token,
        'owner_id': f'-{group_id}',
        'from_group': 1,  # publish on behalf of the group
        'attachments': attachments,
        'message': comment,
        'v': API_version,
    }
    response = requests.post(vk_url, params=params)
    response.raise_for_status()
