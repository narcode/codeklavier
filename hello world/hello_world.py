import time
from pynput.keyboard import Key, Controller
import rtmidi

midiin = rtmidi.MidiIn()
ports = midiin.get_ports()

for i in range(1, 5):
    num = 20+(1)
    print('##'*num)
    time.sleep(0.2)

print('\n', "Welcome to the Codeklavier Setup... this are your detected MIDI devices:", '\n')

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

# get device id
print('\nplease play 1 key on your MIDI keyboard')

counter = 0
try:
    while counter < 1:
        msg = midiin.get_message()
        if msg:
            message, deltatime = msg
            device_id = message[0]
            counter += 1
finally:
    print('your device id is: ', device_id, '\n')

# midinumber to alphanumerical characters
keyboard = Controller()

def evaluateSC():
    with keyboard.pressed(Key.shift):
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

def mapping(midinumber):
    # chars and nums
    if midinumber == 69:
        keyboard.type('h')
    elif midinumber == 74:
        keyboard.type('l')
    elif midinumber == 63:
        keyboard.type('e')
    elif midinumber == 80:
        keyboard.type('o')
    elif midinumber == 68:
        keyboard.type('o')
    elif midinumber == 81:
        keyboard.type('r')
    elif midinumber == 88:
        keyboard.type('w')
    elif midinumber == 64:
        keyboard.type('d')
    elif midinumber ==48:
        keyboard.type('t')
    elif midinumber == 47:
        keyboard.type('s')
    elif midinumber == 37:
        keyboard.type('a')
    elif midinumber == 41:
        keyboard.type('n')
    elif midinumber == 42:
        keyboard.type('i')
    elif midinumber == 44:
        keyboard.type('o')
    elif midinumber == 45:
        keyboard.type('p')
    elif midinumber == 59:
        keyboard.type('0')
    elif midinumber == 60:
        keyboard.type('1')
    elif midinumber == 61:
        keyboard.type('2')
    elif midinumber == 62:
        keyboard.type('3')
    elif midinumber == 89:
        keyboard.type('4')
    elif midinumber == 90:
        keyboard.type('5')
    elif midinumber == 91:
        keyboard.type('6')
    elif midinumber == 92:
        keyboard.type('7')
    elif midinumber == 93:
        keyboard.type('8')
    elif midinumber == 94:
        keyboard.type('9')
   # special keys
    elif midinumber == 56:
        keyboard.press(Key.space),
    elif midinumber == 32:
        keyboard.press(Key.enter),
    elif midinumber == 50:
        keyboard.type('~'),
    elif midinumber == 51:
        keyboard.type('+'),
    elif midinumber == 54:
        keyboard.type('-'),
    elif midinumber == 49:
        keyboard.type('='),
    elif midinumber == 103:
        keyboard.type('?'),
    elif midinumber == 105:
        keyboard.type('.!'),
    elif midinumber == 95:
        keyboard.press(Key.backspace),
  # supercollider commands:
    elif midinumber == 33:
        evaluateSC(),
    elif midinumber == 22:
        keyboard.type('.tempo'),
    elif midinumber == 21:
        keyboard.type('.play'),
    elif midinumber == 102:
        keyboard.type('TempoClock.default')

# class to handle the midi input and map it to characters
class HelloWorld(object):
    def __init__(self, port):
        self.port = port

    def __call__(self, event, data=None):
        message, deltatime = event
        # print('deltatime: ', deltatime, 'msg: ', message)
        if message[2] > 0: #only noteOn
            if (message[0] == device_id):
                mapping(message[1])

print("\nCodeKlavier is ready and ON. Press Control-C to exit.")
midiin.set_callback(HelloWorld(0))

try:
    timer = time.time()
    while True:
        # msg = midiin.get_message()
        #
        # if msg:
        #     message, deltatime = msg
        #     print('deltatime: ', deltatime, 'msg: ', message)

        time.sleep(0.01)
except KeyboardInterrupt:
    print('')
finally:
    print("Bye-Bye :(")
    midiin.close_port()

del midiin
