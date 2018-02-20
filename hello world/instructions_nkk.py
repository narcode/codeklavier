import time
import rtmidi

# Use trick to import from parentdir
import sys
import os
import inspect


from CK_Setup import Setup
from Mapping import Mapping_HelloWorld_NKK
from Instructions import Instructions

# Start the CodeKlavier
codeK = Setup()
tutorial = Instructions()
myPort = codeK.perform_setup()
codeK.open_port(myPort)
codeK.open_port_out(myPort)
device_id = codeK.get_device_id()
print('your device id is: ', device_id, '\n')

# Use your favourite mapping of the keys
mapping = Mapping_HelloWorld_NKK()

# class to handle the midi input and map it to characters
#TODO: this is ugly! Move this to the CodeKlavier module
class HelloWorld(object):
    def __init__(self, port):
        self.port = port

    def __call__(self, event, data=None):
        message, deltatime = event
        # print(message)
        if message[2] > 0: #only noteOn
            if (message[0] == device_id):
                mapping.mapping(message[1])

codeK.set_callback(HelloWorld(myPort))

tutorial.do_tutorial()
codeK.send_message([0x90, 108, 127]) #send enter to codespace
tutorial.level_four()

# Loop to program to keep listening for midi input
try:
    timer = time.time()
    while True:
        time.sleep(0.01)
except KeyboardInterrupt:
    print('')
finally:
    # print("Bye-Bye :(")
    codeK.end()
