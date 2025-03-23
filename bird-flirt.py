#!/usr/bin/env python3

import logging
import argparse
import asyncio
import random
from os import listdir
from os.path import isfile, join
from playsound import playsound
import RPi.GPIO as GPIO
import subprocess

logging.basicConfig(
    format='%(levelname)-8s %(message)s',
    level=logging.DEBUG)

parser = argparse.ArgumentParser(
    prog='Bird Flirt',
    description='Plays bird sounds to call birds. Only wave files are supported.',
    epilog='Thanks for using Bird Flirt')

parser.add_argument('-s', '--sounds', help='set path to sound files. default current directory', default=".")
args = parser.parse_args()
sounds_directory = args.sounds

logging.info("Started Bird Flirt")
logging.info("Using sounds in directory [" + sounds_directory + "]")

files = [file for file in listdir(sounds_directory) if isfile(join(sounds_directory, file))]
files_filtered = [file for file in files if file.endswith("wav") or file.endswith("wave")]
files_full_path = [join(sounds_directory, file) for file in files_filtered]

if not files_full_path:
    exit("No usable files found in given directory")

delay_base_s = 300
delay_range_s = 60


logging.debug("Using files: " + str(files_full_path))

async def play_bird_sound(filename):
    logging.debug("Playing file: " + filename)
    subprocess.run(["aplay", filename])

async def wait_between_sounds():
    delay_random = random.randint(-delay_range_s, delay_range_s)
    delay = delay_base_s + delay_random
    logging.debug("Waiting for random seconds of " + str(delay))
    await asyncio.sleep(delay)

async def play_sound_and_wait(file):
    await asyncio.create_task(play_bird_sound(file))
    await asyncio.create_task(wait_between_sounds())

async def main_loop():
    while True:
        for file in files_full_path:
            task = asyncio.create_task(play_sound_and_wait(file))
            await task

GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

LED_PIN = 15
BTN_PIN = 13

GPIO.setup(BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED_PIN, GPIO.OUT)

GPIO.output(LED_PIN, GPIO.HIGH)
#while True: # Run forever
#    if GPIO.input(10) == GPIO.HIGH:
#        print("Button was pushed!")

asyncio.run(main_loop())
