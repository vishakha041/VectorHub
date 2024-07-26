import os
import json
import requests

from tqdm.auto import tqdm

from urllib.parse import urljoin

DUB_CO_API_TOKEN = os.getenv("DUB_CO_API_TOKEN")

class DubLink:
    def __init__(self, id, url, short_url) -> None:
        self.id = id
        self.url = url
        self.short_url = short_url
        self.count = -1

    def set_click_cnt(self, count) -> None:
        self.count = count

    def __str__(self) -> str:
        return str(self.id)

BASE_URL = "https://api.dub.co"
headers = {
    'Authorization': f'Bearer {DUB_CO_API_TOKEN}',
    'Content-Type': 'application/json'
}

def get_shortened_url_objs() -> list:
    global headers, DUB_CO_API_TOKEN, BASE_URL

    print('Fetching list of shortened URLs', flush=True)
    
    url_objs = []

    req = requests.get(urljoin(BASE_URL, "links"), headers=headers)
    if req.status_code < 300:
        data = req.json()
        for row in data:
            url_objs.append(
                DubLink(
                    id=row['id'],
                    url=row['url'],
                    short_url=row['shortLink']
                )
            )
    
    print(f'Found {len(url_objs)} links', flush=True)

    return url_objs


def get_link_click_cnt(linkId) -> int:
    global headers, DUB_CO_API_TOKEN, BASE_URL

    params = {
        'linkId': f'{linkId}',
    }

    req = requests.get(urljoin(BASE_URL, "analytics"), headers=headers, params=params)
    if req.status_code < 300:
        data = req.json()
        return data['clicks']
    
    return 0

def get_links_clicks(url_objs) -> list:
    print('Fetching click count for every URL', flush=True)

    for obj in tqdm(url_objs):
        obj.set_click_cnt(get_link_click_cnt(obj.id))
    
    for obj in url_objs:
        print(obj.count)

shortened_url_objs = get_shortened_url_objs()
get_links_clicks(shortened_url_objs)