#!/usr/bin/env python3

import os
import json
import shutil
import logging
import validators
from yt_dlp import YoutubeDL
from pydub import AudioSegment
#from pydub.effects import normalize
from argparse import ArgumentParser
from audio_separator.separator import Separator

ydl_opts = {
    #'extractor_args': {'youtube': {'player-client': ['default', '-tv', 'web_safari', 'web_embedded']}},
    'no_warnings': True,
    'noplaylist': True,
    'outtmpl': f'/tmp/baktrak/source.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }],
    'quiet': True,
}

def get_info_from_yt(source):
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(source, download = False)

        return json.dumps(ydl.sanitize_info(info))

def download_from_yt(source):
    with YoutubeDL(ydl_opts) as ydl:
        err = ydl.download(source)

def split_into_stems():
    separator = Separator(
        log_formatter = logging.Formatter('[%(module)s] %(message)s'),
        output_format = 'MP3',
        output_dir = '/tmp/baktrak',
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
    output_files = separator.separate('/tmp/baktrak/source.mp3', output_names)

def bounce_stems(exclude_instruments = []):
    ms = len(AudioSegment.from_file('/tmp/baktrak/source.mp3', format = 'mp3'))
    mix = AudioSegment.silent(duration = ms)

    for f in os.listdir('/tmp/baktrak'):
        if f.startswith('stem-') and f.endswith('.mp3'):
            if f.removeprefix('stem-').removesuffix('.mp3') in exclude_instruments:
                continue

            stem = AudioSegment.from_file(f'/tmp/baktrak/{f}', format = 'mp3')
            mix = mix.overlay(stem, position = 0)

    mix.export('baktrak.mp3', format = 'mp3')

def main():
    parser = ArgumentParser(prog = 'baktrak')

    #parser.add_argument('source', nargs = '+', help = 'source to create the backing track from (can be either a YouTube URL, search term or path to a local audio file or already isolated stems)')
    parser.add_argument('source', nargs = '+', help = 'source to create the backing track from (can be either a YouTube URL, search term, or path to a local audio file)')
    parser.add_argument('-b', '--no-bass', action = 'append_const', dest = 'excluded', const = 'bass', help = 'exclude bass from the track')
    parser.add_argument('-d', '--no-drums', action = 'append_const', dest = 'excluded', const = 'drums', help = 'exclude drums from the track')
    parser.add_argument('-g', '--no-guitar', action = 'append_const', dest = 'excluded', const = 'guitar', help = 'exclude guitar from the track')
    parser.add_argument('-o', '--no-other', action = 'append_const', dest = 'excluded', const = 'other', help = 'exclude other from the track')
    parser.add_argument('-p', '--no-piano', action = 'append_const', dest = 'excluded', const = 'piano', help = 'exclude piano from the track')
    parser.add_argument('-v', '--no-vocals', action = 'append_const', dest = 'excluded', const = 'vocals', help = 'exclude vocals from the track')

    args = parser.parse_args()

    try:
        os.makedirs('/tmp/baktrak', exist_ok = True)

        if len(args.source) == 1:
            source = args.source[0]

            if validators.url(source):
                download_from_yt(source)
            elif os.path.exists(source):
                shutil.copy(source, '/tmp/baktrak/source.mp3')
            else:
                raise Exception('Unknown error')
        elif len(args.source) > 1:
            source = ' '.join(args.source)

            info = json.loads(get_info_from_yt(f'ytsearch:{source}'))
            print(f"Found video with title '{info['entries'][0]['title']}'")

            download_from_yt(f'ytsearch:{source}')
        else:
            raise Exception('Unknown error')

        split_into_stems()
        bounce_stems(exclude_instruments = args.excluded)
    except Exception as e:
        raise e
    finally:
        shutil.rmtree('/tmp/baktrak/')

if __name__ == '__main__':
    main()
