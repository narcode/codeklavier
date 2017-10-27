import time
import rtmidi

import sys
import os
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from CodeKlavier.Setup import Setup
from CodeKlavier.Mapping import Mapping_Motippets
from CodeKlavier.motippets_classes import Motippets

# Start the CodeKlavier
codeK = Setup()
myPort = codeK.perform_setup()
codeK.open_port(myPort)
device_id = codeK.get_device_id()
print('your device id is: ', device_id, '\n')

# Use your favourite mapping of the keys
mapping = Mapping_Motippets()

print("\nCodeKlavier is ready and ON.")
print("You are performing: Motippets")
print("\nPress Control-C to exit.")

# main memory (i.e. listen to the whole register)
mainMem = Motippets(myPort, mapping, device_id)

# midi listening per register
pianosectons = [47, 78, 108]
memLow = Motippets(myPort, mapping, device_id)
memMid = Motippets(myPort, mapping, device_id)
memHi = Motippets(myPort, mapping, device_id)

#midi listening for tremolos
tremoloHi = Motippets(myPort, mapping, device_id)
tremoloMid = Motippets(myPort, mapping, device_id)
tremoloLow = Motippets(myPort, mapping, device_id)


# Loop to program to keep listening for midi input
try:
    timer = time.time()
    while True:
        msg = codeK.get_message()

        if msg:
            #motifs:
            mainMem.parse_midi(msg, '')
            memLow.parse_midi(msg, 'low')
            memMid.parse_midi(msg, 'mid')
            memHi.parse_midi(msg, 'hi')
            #tremolos:
            tremoloHi.parse_midi(msg, 'tremoloHi')
            tremoloMid.parse_midi(msg, 'tremoloMid')
            tremoloLow.parse_midi(msg, 'tremoloLow')            

        time.sleep(0.01)
except KeyboardInterrupt:
    print('')
finally:
    print("Bye-Bye :(")
    codeK.end()
