#!/usr/bin/env python3
"""midi_delegate.py

This file opens a delegate between nodejs and python's CodeKlavier.
Used for the installation at NKK 2017
"""

#TODO: use CodeKlavier module

import time
from pynput.keyboard import Key, Controller
from CK_Setup import Setup

def run(codeK):
    """Run the CodeKlavier

    :param CodeKlavier.Setup.setup codeK: the setup file
    """
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
    """Main function as example.
    """

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
