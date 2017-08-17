import time
import rtmidi

midiin = rtmidi.MidiIn()
ports = midiin.get_ports()

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
    midiin.open_port(choice)

print("CodeKlavier is ON. Press Control-C to exit.")
try:
    timer = time.time()
    while True:
        msg = midiin.get_message()

        if msg:
            message, deltatime = msg
            print('deltatime: ', deltatime, 'msg: ', message)

        time.sleep(0.01)
except KeyboardInterrupt:
    print('')
finally:
    print("Bye-Bye :(")
    midiin.close_port()
del midiin
