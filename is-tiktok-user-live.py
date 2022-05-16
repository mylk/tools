#!/usr/bin/env python

import sys

from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import ConnectEvent
from TikTokLive.types.errors import LiveNotFound, FailedConnection

# https://www.youtube.com/watch?v=gubvklbZFTU
client: TikTokLiveClient = TikTokLiveClient(unique_id=sys.argv[1])

@client.on('connect')
def on_connect(_: ConnectEvent):
    print('User is live!')
    sys.exit(0)

if __name__ == '__main__':
    try:
        client.run()
    except Exception:
        print('Offline.')
        sys.exit(1)

