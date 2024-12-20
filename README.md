# Bible TTS
This is a Python script that converts the [Catholic Public Domain Version](https://www.sacredbible.org/catholic/) of the bible to an 40Kb per second MP3 audio bible with full ID3 tagging.

Two pregenerated audio bibles are provided as .zip files. Check the [releases page](https://github.com/MrRar/bible-tts/releases) for details.

## bible-tts setup
bible-tts will only run on Linux since it relies on [Piper](https://github.com/rhasspy/piper) for text to speech. Piper is only available for Linux.

python3, eyeD3, and ffmpeg will need to be installed on the computer.

Download and extract the [bible-tts](https://github.com/MrRar/bible-tts) repository somewhere.

Download the piper binaries from the the [piper releases page](https://github.com/rhasspy/piper/releases).

Download the Catholic Public Domain Version as JSON from this [link](https://bitbucket.org/sbruno/cpdv-json-encoder/src/master/CPDV-JSON/EntireBible-CPDV.json). Place EntireBible-CPDV.json in the root of the bible-tts directory.

Download one or more [piper voices](https://rhasspy.github.io/piper-samples/) and place them in the models folder. You will need both a .onnx file and a .json file for each one.

The Bible TTS script will detect all the models that are in the models directory and will generate audio bibles using all of them.

Setup is complete! To start Bible TTS, cd into the bible-tts directory and run `python3 bible-tts.py`

If you close the script you can start it again and it will continue generating audio files where it left off.

It takes about 8 and a half hours to generate one audio bible on my laptop.
