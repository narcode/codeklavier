import time
import rtmidi

midiout = rtmidi.MidiOut()
ports = midiout.get_ports()

print(ports)

if ports:
    midiout.open_port(0)
else:
    midioout.open_virtual_port("narcode_port")

noteOn = [0x90, 60, 112]
noteOff = [0x80, 60, 0]
midiout.send_message(noteOn)
time.sleep(1)
midiout.send_message(noteOff)

del midiout
