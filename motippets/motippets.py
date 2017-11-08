import time
from threading import Thread

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

# Use your favourite mapping of the keys0

mapping = Mapping_Motippets()

print("\nCodeKlavier is ready and ON.")
print("You are performing: Motippets")
print("\nPress Control-C to exit.")

# main memory (i.e. listen to the whole register)
mainMem = Motippets(mapping, device_id)

# midi listening per register
pianosectons = [47, 78, 108]
memLow = Motippets(mapping, device_id)
memMid = Motippets(mapping, device_id)
memHi = Motippets(mapping, device_id)

#midi listening for tremolos
tremoloHi = Motippets(mapping, device_id)
tremoloMid = Motippets(mapping, device_id)
tremoloLow = Motippets(mapping, device_id)

#midi listening for conditionals 
conditionals = Motippets(mapping, device_id)
noteBuffer = Motippets(mapping, device_id)

#multiprocessing vars
counter = 0
 
def parallelism(debug=True):
    print('thread started')
    
    for s in range(0, 10):
        if counter > 100:
            mapping.result(2, 'code')
            break
        if debug:        
            print(counter)
        time.sleep(1)
        
# Loop to program to keep listening for midi input
try:
    while True:
        msg = codeK.get_message()

        if msg:
            counter += 1
            
            ##motifs:
            mainMem.parse_midi(msg, 'full')
            memLow.parse_midi(msg, 'low')
            memMid.parse_midi(msg, 'mid')
            memHi.parse_midi(msg, 'hi')
            ##tremolos:
            tremoloHi.parse_midi(msg, 'tremoloHi')
            tremoloMid.parse_midi(msg, 'tremoloMid')
            tremoloLow.parse_midi(msg, 'tremoloLow')
            
            ##conditionals              
            if conditionals.parse_midi(msg, 'conditionals') == "2 on":
                counter = 0 # reset the counter
                if __name__ == '__main__':
                    p = Thread(target=parallelism, name='conditional note counter thread')
                    p.start()      
        
        time.sleep(0.01)
        
except KeyboardInterrupt:
    print('')
finally:
    print("Bye-Bye :(")
    codeK.end()
