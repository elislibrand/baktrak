#!/usr/bin/env python3

import os
import sys
import json
import yt_dlp
import logging
from pydub import AudioSegment
#from pydub.effects import normalize
from audio_separator.separator import Separator

ydl_opts = {
    'noplaylist': True,
    'outtmpl': f'tmp/yt.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }],
    'quiet': True,
}

def get_info_from_yt(source):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(source, download = False)

        return json.dumps(ydl.sanitize_info(info))

def download_from_yt(source):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        err = ydl.download(source)

def split_into_stems():
    separator = Separator(
        log_formatter = logging.Formatter('[%(module)s] %(message)s'),
        output_format = 'MP3',
        output_dir = 'tmp/',
    )
    separator.load_model(model_filename = 'htdemucs_6s.yaml')

    output_names = {
        'Vocals': 'stem-vocals',
        'Drums': 'stem-drums',
        'Bass': 'stem-bass',
        'Other': 'stem-other',
        'Guitar': 'stem-guitar',
        'Piano': 'stem-piano',
    }
    output_files = separator.separate('tmp/yt.mp3', output_names)

def bounce_stems():
    ms = len(AudioSegment.from_mp3('tmp/yt.mp3'))
    mix = AudioSegment.silent(duration = ms)

    ignored_stems = [
        'stem-bass.mp3',
        'stem-guitar.mp3',
    ]

    for f in os.listdir('tmp/'):
        if f.lower().startswith('stem-') and f.lower().endswith('.mp3'):
            if f in ignored_stems:
                continue

            stem = AudioSegment.from_mp3(f'tmp/{f}')
            mix = mix.overlay(stem, position = 0)

    mix.export('output/backing-track.mp3', format = 'mp3')

def main():
    source = input('URL or search term: ')

    if not source.startswith('http'):
        source = f'ytsearch:{source}'

        info = json.loads(get_info_from_yt(source))

        print(f"Found video with title '{info['entries'][0]['title']}'")
        #input('Is this correct? [y/n] ')

    try:
        os.makedirs('tmp', exist_ok = True)
        os.makedirs('output', exist_ok = True)

        download_from_yt(source)

        split_into_stems()
        bounce_stems()
    finally:
        tmp_files = [
            'tmp/yt.mp3',
            'tmp/stem-vocals.mp3',
            'tmp/stem-drums.mp3',
            'tmp/stem-bass.mp3',
            'tmp/stem-other.mp3',
            'tmp/stem-guitar.mp3',
            'tmp/stem-piano.mp3',
        ]

        for f in tmp_files:
            if os.path.exists(f):
                os.remove(f)

if __name__ == '__main__':
    main()
