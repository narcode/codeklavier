import time
from pynput.keyboard import Key, Controller
import rtmidi

# Use trick to import from parrentdir
import sys
import os
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from CodeKlavier.Setup import Setup

# Start the CodeKlavier
codeK = Setup()
myPort = codeK.perform_setup()
device_id = codeK.get_device_id()
print('your device id is: ', device_id, '\n')

#TODO: move this keyboard stuff to a seperate class (including evaluateSC and mapping)
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

print("\nCodeKlavier is ready and ON.")
print("You are performing: HELLO WORLD")
print("\nPress Control-C to exit.")

codeK.set_callback(HelloWorld(myPort))

try:
    timer = time.time()
    while True:
        time.sleep(0.01)
except KeyboardInterrupt:
    print('')
finally:
    print("Bye-Bye :(")
    codeK.end()
