#!/usr/bin/env python3

#TODO: use CodeKlavier module

"""miditest.py

This file is a tester for the midisignals from your input device. It quickly helps you
check if your midi input device is being registered and it's messages received.
This file is not a formal part of the CodeKlavier. However, if you can see the
midi messages being printed after running this script then you can rest assured that
the CodeKlavier will run with your midi setup.
"""

import time
from CodeKlavier.Setup import Setup

def run(codeK):
    """This method creates an infinite loop that you can break by the standard
    keyboard interrupt.

    :param CodeKlavier.Setup.Setup CodeK: a setup file for the CodeKlavier
    """
    print("CodeKlavier is ON. Press Control-C to exit.")
    try:
        while True:
            msg = codeK.get_message()

            if msg:
                message, deltatime = msg
                print('deltatime: ', deltatime, 'msg: ', message)


            time.sleep(0.01)

    except KeyboardInterrupt:
        print('')
    finally:
        print("Bye-Bye :(")
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
