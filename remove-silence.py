#!/usr/bin/env python

from pydub import AudioSegment, silence
import sys

filename = sys.argv[1]

wav_file = AudioSegment.from_wav(filename)

silences = silence.detect_nonsilent(wav_file, min_silence_len=1000, silence_thresh=-16)

new_wav_file = AudioSegment.empty()
for start, stop in silences:
    new_wav_file += wav_file[(start - 500):(stop + 500)]

new_wav_file.export('{}.out'.format(filename))

