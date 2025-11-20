# Baktrak
Generate custom backing tracks from YouTube videos, using stem separation and audio bouncing.

## Installation
Install on Linux:
```
$ curl -LO https://github.com/elislibrand/baktrak/releases/latest/download/baktrak-linux-amd64.zip
$ unzip baktrak-linux-amd64.zip -d ~/.local/bin/
```

## Usage (examples)
Create a backing track of *Paint It, Black* by *The Rolling Stones* for bass and guitar (exclude bass and guitars):
```
$ baktrak -bg the rolling stones paint it black
```

Create a backing track of *Beast Of Burden* by *The Rolling Stones* for vocals (exclude vocals):
```
$ baktrak -v the rolling stones beast of burden
```

**Note:** it is also possible to provide a URL or path to a local audio file, instead of a search query.

## Dependencies
Python >= 3.13. Other versions may or may not work correctly.

[FFmpeg](https://ffmpeg.org/) is also needed for processing non-WAV files, like MP3.
