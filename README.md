# Baktrak
Generate custom backing tracks from YouTube videos, using stem separation and audio bouncing.

## Installation
Clone the git repo and `cd` into it:
```
$ git clone https://github.com/elislibrand/baktrak.git
$ cd baktrak/
```

Create a virtual environment:
```
$ python3 -m venv venv
```

Activate the virtual environment:
```
$ source venv/bin/activate
```

Install the required packages:
```
(venv) $ pip3 install -r requirements.txt
```

## Dependencies
Python >= 3.13. Other versions may or may not work correctly.

[FFmpeg](https://ffmpeg.org/) is also needed for processing non-WAV files, like MP3.

## Usage
Run the program:
```
(venv) $ python3 main.py
```
