#!/usr/bin/env python

# Download a Spotify podcast episode without having a Spotify account.
#
# Requirements:
# pip install BeautifulSoup4
#
# Usage:
# ./spotify-dl.py https://open.spotify.com/episode/7kGhXnkQfjhLo204mADOxw
# ./spotify-dl.py 7kGhXnkQfjhLo204mADOxw

from bs4 import BeautifulSoup
import json
import re
import requests
import sys
from urllib.parse import urlparse

def validate_url(user_input):
    try:
        result = urlparse(user_input)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False

def parse_input():
    user_input = sys.argv[1]

    if validate_url(user_input):
        return user_input.split('/')[-1]

    return user_input

def scrape(episode_id):
    response = requests.get('https://open.spotify.com/embed-podcast/episode/{}'.format(episode_id))

    page_data = BeautifulSoup(response.text, 'html.parser').find_all('script')[-1].string

    data_json = page_data.replace('window.__PRELOADED_STATE__ = ', '')
    data = json.loads(data_json)

    result = {
        'filename': data['data']['name'],
        'url': data['data']['unencryptedAudioUrl']
    }

    return result

def download(episode_metadata):
    chars_to_remove = [';', '/']
    episode_metadata['filename'] = re.sub('|'.join(chars_to_remove), '', episode_metadata['filename'])

    episode_file = requests.get(episode_metadata['url'])
    open('{}.mp3'.format(episode_metadata['filename']), 'wb').write(episode_file.content)

if __name__ == '__main__':
    episode_id = parse_input()

    episode_metadata = scrape(episode_id)

    print('Filename: {}.mp3'.format(episode_metadata['filename']))
    print('File URL: {}'.format(episode_metadata['url']))

    print('Downloading...')
    download(episode_metadata)
    print('Done!')
