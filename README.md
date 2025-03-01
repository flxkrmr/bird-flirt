# Bird Flirt

Application to play audio files at a pseudo random interval to attract birds. Only wav files with suffix .wav or .wave are supported.

## Setup
```
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install pipenv
pipenv install
```

## Run
```
pipenv run python bird-flirt.py --sounds <path-to-sound-files>
```
