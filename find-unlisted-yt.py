#!/bin/python

import pytube
import random
import string
import time
import whisper

# https://towardsdatascience.com/speech-to-text-with-openais-whisper-53d5cea9005e
# ex: https://www.youtube.com/watch?v=lVMx4tgZcuk
# ex: 5hfYJsQAhl0

VIDEO_URL_PREFIX = 'https://www.youtube.com/watch?v='
video_id_elements = string.ascii_letters + string.digits + '-' + '_'
# video_id_elements = video_id_elements.replace('O', '')

def generate_video_id(length):
    random_id = ''.join(random.choice(video_id_elements) for i in range(length))
    return random_id

def is_unlisted(video_id):
    video_url = VIDEO_URL_PREFIX + video_id

    data = pytube.YouTube(video_url)
    if 'contents' not in data.initial_data \
        or 'contents' not in data.initial_data['contents']['twoColumnWatchNextResults']['results']['results']:
        return False

    info_list = data.initial_data['contents']['twoColumnWatchNextResults']['results']['results']['contents']
    for info in info_list:
        if 'videoPrimaryInfoRenderer' in info:
            for element in info['videoPrimaryInfoRenderer']:
                if element == 'badges':
                    badges = info['videoPrimaryInfoRenderer'][element]
                    for badge in badges:
                        if badge['metadataBadgeRenderer']['label'] == 'Unlisted':
                            return True
    return False

while True:
    video_id = generate_video_id(11)
    print('{}: '.format(video_id), end='')
    print(is_unlisted(video_id))
    time.sleep(1)

