import configparser
import inspect
import os
import rtmidi
import sys
import time

# CodeKlavier Modules
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from CodeKlavier.CK_Setup import Setup
from CodeKlavier.Mapping import Mapping_HelloWorld_NKK
from CodeKlavier.Instructions import Instructions

# Start the CodeKlavier
config = configparser.ConfigParser()
config.read('default_setup.ini')

try:
    myPort = config['midi'].getint('port')
    device_id = config['midi'].getint('device_id')
except KeyError:
    print('Missing key information in the config file.')
    exit(0)

codeK = Setup()
tutorial = Instructions()
codeK.open_port(myPort)
codeK.open_port_out(myPort)

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
