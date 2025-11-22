#!/usr/bin/env python3

import os
import json
import shutil
import logging
import validators
from argparse import ArgumentParser

ydl_opts = {
    #'extractor_args': {'youtube': {'player-client': ['default', '-tv', 'web_safari', 'web_embedded']}},
    'max_results': 1,
    'no_warnings': True,
    'noplaylist': True,
    'outtmpl': f'/tmp/baktrak/source.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }],
    'quiet': True,
}

def download_from_yt(source):
    from yt_dlp import YoutubeDL

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(source, download = True)
        sanitized_info = ydl.sanitize_info(info)

        if 'entries' in info:
            sanitized_info = sanitized_info['entries'][0]

        title = sanitized_info['title']
        print(f"Found source with title '{title}'")

def split_into_stems():
    from audio_separator.separator import Separator

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
    from pydub import AudioSegment, effects

    ms = len(AudioSegment.from_file('/tmp/baktrak/source.mp3', format = 'mp3'))
    mix = AudioSegment.silent(duration = ms)

    for f in os.listdir('/tmp/baktrak'):
        if f.startswith('stem-') and f.endswith('.mp3'):
            if f.removeprefix('stem-').removesuffix('.mp3') in exclude_instruments:
                continue

            stem = AudioSegment.from_file(f'/tmp/baktrak/{f}', format = 'mp3')
            mix = mix.overlay(stem, position = 0)

    mix = effects.normalize(mix)
    mix.export('baktrak.mp3', format = 'mp3')

    print(f"Backing track written to: {os.path.abspath('baktrak.mp3')}")

def main():
    parser = ArgumentParser(prog = 'baktrak', prefix_chars = '-+')

    parser.add_argument('source', nargs = '+', help = 'source to create the backing track from (can be either a YouTube URL, search term, or path to a local audio file)')

    excluding = parser.add_argument_group('excluding instruments')
    excluding.add_argument('-b', action = 'append_const', dest = 'excluded', const = 'bass', help = 'exclude bass from the track')
    excluding.add_argument('-d', action = 'append_const', dest = 'excluded', const = 'drums', help = 'exclude drums from the track')
    excluding.add_argument('-g', action = 'append_const', dest = 'excluded', const = 'guitar', help = 'exclude guitar from the track')
    excluding.add_argument('-o', action = 'append_const', dest = 'excluded', const = 'other', help = 'exclude other from the track')
    excluding.add_argument('-p', action = 'append_const', dest = 'excluded', const = 'piano', help = 'exclude piano from the track')
    excluding.add_argument('-v', action = 'append_const', dest = 'excluded', const = 'vocals', help = 'exclude vocals from the track')

    isolating = parser.add_argument_group('isolating instruments')
    isolating.add_argument('+b', action = 'append_const', dest = 'isolated', const = 'bass', help = 'isolate bass in the track')
    isolating.add_argument('+d', action = 'append_const', dest = 'isolated', const = 'drums', help = 'isolate drums in the track')
    isolating.add_argument('+g', action = 'append_const', dest = 'isolated', const = 'guitar', help = 'isolate guitar in the track')
    isolating.add_argument('+o', action = 'append_const', dest = 'isolated', const = 'other', help = 'isolate other in the track')
    isolating.add_argument('+p', action = 'append_const', dest = 'isolated', const = 'piano', help = 'isolate piano in the track')
    isolating.add_argument('+v', action = 'append_const', dest = 'isolated', const = 'vocals', help = 'isolate vocals in the track')

    args = parser.parse_args()

    if not args.excluded and not args.isolated:
        parser.error('at least one instrument must be excluded (-) or isolated (+)')

    if args.excluded and args.isolated:
        parser.error('instruments cannot be both excluded (-) and isolated (+)')

    excluded = args.excluded

    if args.isolated:
        excluded = list(set([a.const for a in parser._actions if a.dest == 'isolated']) - set(args.isolated))

    try:
        os.environ['CUDA_VISIBLE_DEVICES'] = ''
        os.makedirs('/tmp/baktrak', exist_ok = True)

        source = ' '.join(args.source)

        if validators.url(source):
            download_from_yt(source)
        elif os.path.exists(source):
            shutil.copy(source, '/tmp/baktrak/source.mp3')
        else:
            download_from_yt(f'ytsearch:{source}')

        split_into_stems()
        bounce_stems(exclude_instruments = excluded)
    except KeyboardInterrupt as e:
        pass
    except Exception as e:
        raise e
    finally:
        shutil.rmtree('/tmp/baktrak/')

if __name__ == '__main__':
    main()
