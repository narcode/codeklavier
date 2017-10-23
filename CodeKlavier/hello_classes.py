import rtmidi
"""
classes for Hello World.
First prototype of the CodeKlavier

"""

# class to handle the midi input and map it to characters
class HelloWorld(object):
    def __init__(self, port, mapping):
        self.port = port
        self.mapscheme = mapping

    def __call__(self, event, data=None):
        message, deltatime = event
        if message[2] > 0: #only noteOn
            if (message[0] == device_id):
                self.mapscheme.mapping(message[1])
            if (message[0] == 176): #hardcoded pedal id (not pretty) TODO: make it dynamic
                self.mapscheme.stopSC(message[1])
