#!/usr/bin/env python3

import os
import sys
import json
import yt_dlp
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
        output_format = 'MP3',
        output_dir = 'tmp/',
    )
    separator.load_model(model_filename = 'htdemucs_6s.yaml')

    output_names = {
        'Vocals': 'vocals',
        'Drums': 'drums',
        'Bass': 'bass',
        'Other': 'other',
        'Guitar': 'guitar',
        'Piano': 'piano',
    }
    output_files = separator.separate('tmp/yt.mp3', output_names)

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
    finally:
        tmp_files = [
            'tmp/yt.mp3',
            'tmp/vocals.mp3',
            'tmp/drums.mp3',
            'tmp/bass.mp3',
            'tmp/other.mp3',
            'tmp/guitar.mp3',
            'tmp/piano.mp3',
        ]

        for f in tmp_files:
            if os.path.exists(f):
                os.remove(f)

if __name__ == '__main__':
    main()
