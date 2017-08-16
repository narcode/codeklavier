import time
import rtmidi

midiout = rtmidi.MidiOut()
ports = midiout.get_ports()

for i in range(1, 5):
    num = 20+(1)
    print('##'*num)
    time.sleep(0.2)

print('\n', "Welcome to the Codeklavier... this are your detected MIDI devices:", '\n')

for port in ports:
    print(ports.index(port), " -> ", port)

print('\n')
choice = input("Please choose the MIDI device (number) you want to use and hit Enter:")

while int(choice) >= len(ports) or int(choice) < 0:
    print("Invalid number, please try again:")
    choice = input("Please choose the MIDI device (number) you want to use and hit Enter:")

choice = int(choice)
print("You have chosen: ", ports[choice])

if ports:
    midiout.open_port(choice)

noteOn = [0x90, 60, 112]
noteOff = [0x80, 60, 0]
midiout.send_message(noteOn)
time.sleep(1)
midiout.send_message(noteOff)

del midiout
