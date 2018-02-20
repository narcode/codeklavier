import time
import rtmidi

import sys
import os
import inspect

# CodeKlavier Modules
from CK_Setup import Setup
from Mapping import Mapping_HelloWorld
from hello_classes import HelloWorld

# Start the CodeKlavier
codeK = Setup()
myPort = codeK.perform_setup()
codeK.open_port(myPort)
device_id = codeK.get_device_id()
print('your device id is: ', device_id, '\n')

# Use your favourite mapping of the keys
mapping = Mapping_HelloWorld()

print("\nCodeKlavier is ready and ON.")
print("You are performing: HELLO WORLD")
print("\nPress Control-C to exit.")

codeK.set_callback(HelloWorld(myPort, mapping, device_id))

# Loop to program to keep listening for midi input
try:
    while True:
        time.sleep(0.01)
except KeyboardInterrupt:
    print('')
finally:
    print("Bye-Bye :(")
    codeK.end()
