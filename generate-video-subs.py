#!/bin/python

import pytube
import sys
import whisper

# https://towardsdatascience.com/speech-to-text-with-openais-whisper-53d5cea9005e
# ex: https://www.youtube.com/watch?v=5hfYJsQAhl0

VIDEO_URL_PREFIX = 'https://www.youtube.com/watch?v='

# parse user input
video_url = sys.argv[1]
if not video_url.startswith(VIDEO_URL_PREFIX):
    video_url = VIDEO_URL_PREFIX + video_url

# get video info
print('Downloading video: ' + video_url)
data = pytube.YouTube(video_url)
filename = data.title + '.mp4'

# download video's audio
audio = data.streams.get_audio_only()
audio.download()

# load model, transcribe audio 
model = whisper.load_model('tiny')
text = model.transcribe(filename)

# print the transcription
print("Subtitles:")
print(text['text'].strip())

