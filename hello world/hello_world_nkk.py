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
print('your device id is: ', device_id, '\n\n')
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
                # forwarding only note on messages to tutorial terminal for NKK:
                codeK.send_message([message[0], message[1], message[2]])
            if (message[0] == 176): #hardcoded pedal id (not pretty)
                mapping.stopSC(message[1])

codeK.set_callback(HelloWorld(myPort))

# Loop to program to keep listening for midi input
try:
    # timer = time.time()
    while True:
        if tutorial.mode():
            break
        time.sleep(0.01)
except KeyboardInterrupt:
    print('')
finally:
    # print("Bye-Bye :(")
    codeK.end()
