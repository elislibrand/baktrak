# Baktrak
Generate custom backing tracks from YouTube videos, using stem separation and audio bouncing.

## Installation
Install on Linux:
```
$ curl -LO https://github.com/elislibrand/baktrak/releases/latest/download/baktrak-linux-amd64.zip
$ unzip baktrak-linux-amd64.zip -d ~/.local/bin/
```

## Usage (examples)
### Exclude instruments (-)
Create a backing track of *Paint It, Black* by *The Rolling Stones* for bass and guitar (exclude bass and guitars):
```
$ baktrak -bg the rolling stones paint it black
```

Create a backing track of *Beast Of Burden* by *The Rolling Stones* for vocals (exclude vocals):
```
$ baktrak -v the rolling stones beast of burden
```

### Isolate instruments (+)
Isolate guitar and vocals in *Hurricane* by *Bob Dylan* (exclude all other instruments):
```
$ baktrak +gv bob dylan hurricane
```

> #### NOTE:
> It is also possible to provide a URL or path to a local audio file, instead of a search query.

## Dependencies
Python >= 3.13. Other versions may or may not work correctly.

[FFmpeg](https://ffmpeg.org/) is also needed for processing non-WAV files, like MP3.

## License
This project is licensed under the MIT [License](LICENSE).

## Credits
- [nomadkaraoke](https://github.com/nomadkaraoke) - Author of [Python Audio Separator](https://github.com/nomadkaraoke/python-audio-separator), which serves as the foundation for this entire project.
  - [Anjok07](https://github.com/Anjok07) - Author of [Ultimate Vocal Remover GUI](https://github.com/Anjok07/ultimatevocalremovergui), which almost all of the code in the *Python Audio Separator* repository was copied from. Definitely deserving of credit for anything good from this project.
  - [DilanBoskan](https://github.com/DilanBoskan) - Your contributions at the start of the *Ultimate Vocal Remover GUI* project were essential to the success of UVR.
  - [Kuielab & Woosung Choi](https://github.com/kuielab) - Developed the original MDX-Net AI code.
  - [KimberleyJSN](https://github.com/KimberleyJensen) - Advised and aided the implementation of the training scripts for MDX-Net and Demucs.
  - [Hv](https://github.com/NaJeongMo/Colab-for-MDX_B) - Helped implement chunks into the MDX-Net AI code.
  - [zhzhongshi](https://github.com/zhzhongshi) - Helped add support for the MDXC models in `audio-separator`.
- [jiaaro](https://github.com/jiaaro) - Author of [Pydub](https://github.com/jiaaro/pydub), which provides processing and manipulation of the extracted stems.
