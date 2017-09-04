import time
import rtmidi

# Use trick to import from parrentdir
import sys
import os
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from CodeKlavier.Setup import Setup
from CodeKlavier.Mapping import Mapping_HelloWorld

# Start the CodeKlavier
codeK = Setup()
myPort = codeK.perform_setup()
codeK.open_port(myPort)
device_id = codeK.get_device_id()
print('your device id is: ', device_id, '\n')

# Use your favourite mapping of the keys
mapping = Mapping_HelloWorld()

# class to handle the midi input and map it to characters
#TODO: this is ugly! Move this to the CodeKlavier module
class HelloWorld(object):
    def __init__(self, port):
        self.port = port

    def __call__(self, event, data=None):
        message, deltatime = event
        if message[2] > 0: #only noteOn
            if (message[0] == device_id):
                mapping.mapping(message[1])
            if (message[0] == 176): #hardcoded pedal id (not pretty)
                mapping.stopSC(message[1])

print("\nCodeKlavier is ready and ON.")
print("You are performing: HELLO WORLD")
print("\nPress Control-C to exit.")

codeK.set_callback(HelloWorld(myPort))

# Loop to program to keep listening for midi input
try:
    timer = time.time()
    while True:
        time.sleep(0.01)
except KeyboardInterrupt:
    print('')
finally:
    print("Bye-Bye :(")
    codeK.end()
