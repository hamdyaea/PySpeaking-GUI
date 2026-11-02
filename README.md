# PySpeaking

A lightweight text-to-speech desktop application for Linux, written in Python 3 with Tkinter.

**Developer:** Hamdy Abou El Anein
**Contact:** info@daylightlinux.ch
**License:** GNU GPL v3 (see LICENSE).

## Features

- Tkinter interface with nine selectable languages, replacing EasyGUI.
- Local espeak-ng support, with optional google_speech fallback.
- User text passed directly as a subprocess argument, never through a shell.
- Non-blocking GUI playback and a simple command-line mode.

## Requirements

Python 3.10+, Tkinter, and espeak-ng (recommended) or google_speech.

## Run

    python3 speak.py

    python3 speak.py --text "Hello world" --language en

## Test

    python3 -m unittest discover -s tests -v

Original source: [old branch](https://github.com/hamdyaea/PySpeaking-GUI/tree/old).
