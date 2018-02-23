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
from CodeKlavier.hello_classes import HelloWorld
from CodeKlavier.Mapping import Mapping_HelloWorld

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
codeK.open_port(myPort)

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
