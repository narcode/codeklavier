#!/usr/bin/env python3

#TODO: use CodeKlavier module

"""midi_delegate.py

This file opens a delegate between nodejs and python's CodeKlavier.
Used for the installation at NKK 2017
"""

#TODO: add docstrings and comments

import time
from pynput.keyboard import Key, Controller
from Setup import Setup

def run(codeK):
    print("CodeKlavier is ON. Press Control-C to exit.")
    try:
        timer = time.time()
        keyboard = Controller()
        while True:
            msg = codeK.get_message()

            if msg:
                message, deltatime = msg
                # this filters the 'enter' delegate:
                if message[1] == 64 and message[2] == 1:
                    print('deltatime: ', deltatime, 'msg: ', message)
                    print('enter sent!')
                    keyboard.press(Key.enter)
                    keyboard.release(Key.enter)
                    time.sleep(2)

                #this sends the break delegate
                if message[1] == 64 and message[2] == 2:
                    break

            time.sleep(0.01)

    except KeyboardInterrupt:
        print('')
    finally:
        print("MIDI delegate auto-destruct")
        codeK.end()

def main():

    codeK = Setup()

    # Start the CodeKlavier
    codeK = Setup()
    myPort = codeK.perform_setup()
    codeK.open_port(myPort)
    device_id = codeK.get_device_id()
    print('your device id is: ', device_id, '\n')
    run(codeK)

if __name__ == "__main__":
    main()
