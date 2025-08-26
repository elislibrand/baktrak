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
        output_dir = 'tmp',
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

def bounce_stems(stems_dir = 'tmp'):
    ms = len(AudioSegment.from_file('tmp/yt.mp3', format = 'mp3'))
    mix = AudioSegment.silent(duration = ms)

    ignored_stems = [
        'stem-bass.mp3',
        'stem-guitar.mp3',
    ]

    for f in os.listdir('tmp'):
        if f.lower().startswith('stem-') and f.lower().endswith('.mp3'):
            if f in ignored_stems:
                continue

            stem = AudioSegment.from_file(f'tmp/{f}', format = 'mp3')
            mix = mix.overlay(stem, position = 0)

    mix.export('output/backing-track.mp3', format = 'mp3')

def main():
    options = [
        'URL or search term',
        'already isolated stems',
    ]

    print('Create a backing track from:')

    for i, option in enumerate(options):
        print(f'  {i + 1}) {option}')

    print()

    while not (0 < (choice := int(input('Choose an option: '))) <= len(options)):
        print('Invalid option!')

    try:
        os.makedirs('tmp', exist_ok = True)
        os.makedirs('output', exist_ok = True)

        if options[choice - 1] == 'URL or search term':
            source = input('Enter URL or search term: ')

            if not source.startswith('http'):
                source = f'ytsearch:{source}'

                info = json.loads(get_info_from_yt(source))

                print(f"Found video with title '{info['entries'][0]['title']}'")
                #input('Is this correct? [y/n] ')

            download_from_yt(source)

            split_into_stems()
            bounce_stems()
        elif options[choice - 1] == 'already isolated stems':
            stems_dir = input('Enter path to stems directory: ')

            bounce_stems(stems_dir = stems_dir)
        else:
            raise Exception('Unknown error')
    except Exception as e:
        raise e
    finally:
        for f in os.listdir('tmp'):
            os.remove(f'tmp/{f}')

if __name__ == '__main__':
    main()
