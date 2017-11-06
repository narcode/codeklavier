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
note_count = 0
bomb_is_armed = False
#set the number of notes that can be parsed once the bomb is enabled
bomb_countdown = 10

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

#midi listening for conditionals 
conditionals = Motippets(myPort, mapping, device_id)


# Loop to program to keep listening for midi input
try:
    timer = time.time()
    while True:
        msg = codeK.get_message()

        if msg:
            trigger_count = False
            #motifs:
            trigger_count = mainMem.parse_midi(msg, 'full') or trigger_count
            trigger_count = memLow.parse_midi(msg, 'low') or trigger_count
            trigger_count = memMid.parse_midi(msg, 'mid') or trigger_count
            trigger_count = memHi.parse_midi(msg, 'hi') or trigger_count
            #tremolos:
            trigger_count = tremoloHi.parse_midi(msg, 'tremoloHi') \
                                or trigger_count
            trigger_count = tremoloMid.parse_midi(msg, 'tremoloMid') \
                                or trigger_count
            trigger_count = tremoloLow.parse_midi(msg, 'tremoloLow') \
                                or trigger_count
            #conditionals
            trigger_count = conditionals.parse_midi(msg, 'full_conditionals') \
                                or trigger_count

            note_count = note_count + 1 if trigger_count else note_count
            #Optional:
            #print("Notes played: {0}".format(note_count))

            #bomb is activated when 10 notes are played.
            #TODO: add motif or other pattern to trigger the activation
            if note_count == 10:
                bomb_is_armed = True

            if bomb_is_armed and trigger_count:
                #Decrease countdown after playing and parsing a note
                bomb_countdown -= 1
                #Optional:
                #print("Notes left to play: {0}".format(bomb_countdown))

            if bomb_countdown == 0:
                print("")
                print("  ____   ____   ____  __  __ _ ")
                print(" |  _ \ / __ \ / __ \|  \/  | |")
                print(" | |_) | |  | | |  | | \  / | |")
                print(" |  _ <| |  | | |  | | |\/| | |")
                print(" | |_) | |__| | |__| | |  | |_|")
                print(" |____/ \____/ \____/|_|  |_(_)")
                print("")

                #TODO: add more actions when bomb explodes and CodeKlavier stops
                #TODO: when this becomes elaborate: put it into a function
                break

        time.sleep(0.01)
except KeyboardInterrupt:
    print('')
finally:
    print("Bye-Bye :(")
    codeK.end()
