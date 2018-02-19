"""
classes for Hello World.
First prototype of the CodeKlavier

"""
import rtmidi

class HelloWorld(object):
    """ class to handle the midi input and map it to characters
    """

    def __init__(self, port, mapping, noteonid):
        """Setup the class

        :param int port: the portnumber
        :param dict mapping: the mapping to use
        :param noteonid: the note-on id
        """
        self.port = port
        self.mapscheme = mapping
        self.noteonid = noteonid

    def __call__(self, event, data=None):
        """Deal with the cal function

        :param event: ?
        :param data: ?
        """
        message, deltatime = event
        if message[0] != 254:
            if message[2] > 0: #only noteOn
                if (message[0] == self.noteonid):
                    self.mapscheme.mapping(message[1])
                if (message[0] == 176): #hardcoded pedal id (not pretty) TODO: make it dynamic
                    self.mapscheme.stopSC(message[1])
