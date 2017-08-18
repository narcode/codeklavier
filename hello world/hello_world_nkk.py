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

def evaluateSC(what):
    if what == 'play':
        keyboard.type('.play')
        with keyboard.pressed(Key.shift):
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
    elif what == 'stop':
        keyboard.type('.stop')
        with keyboard.pressed(Key.shift):
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
    elif what == 'enter':
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)

def enter():
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

def delete():
    keyboard.press(Key.backspace)
    keyboard.release(Key.backspace)


def mapping(midinumber):
    # chars and nums
    if midinumber == 87:
        keyboard.type('h')
    elif midinumber == 92:
        keyboard.type('l')
    elif midinumber == 90:
        keyboard.type('e')
    elif midinumber ==94:
        keyboard.type('o')
    elif midinumber == 95:
        keyboard.type('p')
    elif midinumber == 91:
        keyboard.type('n')
    elif midinumber == 89:
        keyboard.type('r')
    elif midinumber == 84:
        keyboard.type('t')
    elif midinumber == 83:
        keyboard.type('s')
    elif midinumber == 80:
        keyboard.type('o')
    elif midinumber == 102:
        keyboard.type('a')
    elif midinumber == 104:
        keyboard.type('f')
    elif midinumber == 106:
        keyboard.type('x')
    elif midinumber == 88:
        keyboard.type('d')
    elif midinumber == 89:
        keyboard.type('r')
    elif midinumber == 103:
        keyboard.type('-'),
    elif midinumber == 105:
        keyboard.type('+'),
    elif midinumber == 108:
        evaluateSC('enter'),
    elif midinumber == 107:
        delete(),
   # special keys
    elif midinumber == 85:
        keyboard.type('~'),
    elif midinumber == 96:
        keyboard.type('='),
    elif midinumber == 98:
        evaluateSC('stop')
    elif midinumber == 99:
        keyboard.type('.tempo'),
    elif midinumber == 97:
        evaluateSC('play')

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
