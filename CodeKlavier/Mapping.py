"""Mapping.py

Contains the classes ``Mapping_HelloWorld``, ``Mapping_HelloWorld_NKK`` and
``Mapping_Motippets``. These class deal with the mapping of the (midi) keys to
chars, strings and commands.

TODO: make a single base class and subclass the different versions from that
class.
"""
import time
from pynput.keyboard import Key, Controller
import socket
from pythonosc import udp_client
import configparser

display1 = 1111
display2 = 2222
display3 = 3333
display4 = 4444
display5 = 5555

class Mapping_HelloWorld:
    """Mapping for the Hello World prototype.

    :param use_display boolean: set if code should be printed in UDP display
    """

    def __init__(self, use_display=False):
        """Init the class

        Print that the user is using this mapping and set the controller.
        """
        if debug:
            print("## Using the Hello World mapping ##")

        #Read config and settings
        self._config = configparser.ConfigParser(delimiters=(':'), comment_prefixes=('#'))
        self._config.read('default_setup.ini')
        self.__keyboard = Controller()
        self.use_display = use_display

        if use_display:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def evaluateSC(self):
        """Evaluate the SuperCollider command (presses shift-enter).
        """

        with self.__keyboard.pressed(Key.shift):
            self.__keyboard.press(Key.enter)
            self.__keyboard.release(Key.shift)

    def stopSC(self, midinumber):
        """If ``midinumber`` is 66, then stop SuperCollider

        By issueing a cmd-. command.

        :param int midinumber: the midinumber pressed on the keyboard
        """
        if midinumber == 66:
            self.__keyboard.press(Key.cmd)
            self.__keyboard.type('.')
            self.__keyboard.release(Key.cmd)

    def formatAndSend(self, msg='', encoding='utf-8', host='localhost', display=1, syntax_color=''):
        """format and prepare a string for sending it over UDP socket

        :param str msg: the string to be sent
        :param str encoding: the character encoding
        :param str host: the UDP server hostname
        :param int display: the UDP destination port
        """

        if display == 1:
            port = 1111
        elif display == 2:
            port = 2222
        elif display == 3:
            port = 3333
        elif display == 4:
            port = 4444

        if self.use_display:
            return self.__socket.sendto(bytes(syntax_color+'\n'+msg, encoding), (host, port))
        else:
            return

    def mapping(self, midinumber, prototype='Hello World', debug=False):
        """Type a letter that is coupled to this midi note.

        :param int midinumber: the midinumber that is played
        """
        try:
            midis = str(midinumber)
            if midis in self._config[prototype]:
                if debug:
                    print(midinumber, self._config[prototype].get(midis))
                mapped_string = self._config[prototype].get(midis)

                if len(mapped_string) < 2:
                    # chars and nums
                    self.__keyboard.type(mapped_string)
                    self.formatAndSend(mapped_string, display=5, syntax_color='hello:', spacing=False)
                else:
                    # special keys
                    if mapped_string == 'space':
                        self.__keyboard.press(Key.space)
                        self.__keyboard.release(Key.space)
                        self.formatAndSend(' ', display=5, syntax_color='hello:', spacing=False)
                    elif mapped_string == 'enter':
                        self.__keyboard.press(Key.enter)
                        self.__keyboard.release(Key.enter)
                        self.formatAndSend('\n', display=5, syntax_color='hello:', spacing=False)
                    elif mapped_string == 'backspace':
                        self.__keyboard.press(Key.backspace)
                        self.__keyboard.release(Key.backspace)
                        self.formatAndSend('', display=5, syntax_color='delete:', spacing=False)
                    elif mapped_string == 'down':
                        self.goDown()
                        self.formatAndSend('\n', display=5, syntax_color='hello:', spacing=False)
                    elif mapped_string == 'sc-evaluate':
                        self.evaluateSC('noEnter_eval')
                        self.formatAndSend('', display=5, syntax_color='hello:', spacing=False)
                    elif mapped_string == '.tempo':
                        self.__keyboard.type(mapped_string)
                        self.formatAndSend(mapped_string, display=5, syntax_color='hello:', spacing=False)
                    elif mapped_string == '.play':
                        self.__keyboard.type(mapped_string)
                        self.formatAndSend(mapped_string, display=5, syntax_color='hello:', spacing=False)
                    elif mapped_string == 'motippetssc-evaluate':
                        self.evaluateSC('eval')
        except KeyError:
            raise LookupError('Missing hello world information in the config file.')

class Mapping_HelloWorld_NKK:
    """Mapping of the HelloWorld piece
    as played on the Leiden Nacht van Kunst en Kultuur.
    """

    def __init__(self):
        """Mapping for the Hello World NKK (installation flavour).
        """
        print("Using the Hello World mapping (NKK)")
        self.__keyboard = Controller()

    def evaluateSC(self, what):
        """Evaluate the SuperCollider command 'what'

        :param what string: the command that should be evaluated
        """
        if what == 'play':
            with self.__keyboard.pressed(Key.cmd):
                self.__keyboard.press(Key.right)
                self.__keyboard.release(Key.right)
            time.sleep(0.01)
            self.__keyboard.type('.play')
            with self.__keyboard.pressed(Key.shift):
                self.__keyboard.press(Key.enter)
                self.__keyboard.release(Key.enter)
            time.sleep(0.01)
            self.__keyboard.press(Key.enter)
            self.__keyboard.release(Key.enter)
        elif what == 'stop':
            with self.__keyboard.pressed(Key.cmd):
                self.__keyboard.press(Key.right)
                self.__keyboard.release(Key.right)
            time.sleep(0.01)
            self.__keyboard.type('.stop')
            with self.__keyboard.pressed(Key.shift):
                self.__keyboard.press(Key.enter)
                self.__keyboard.release(Key.enter)
            time.sleep(0.01)
            self.__keyboard.press(Key.enter)
            self.__keyboard.release(Key.enter)
        elif what == 'alt_eval':
            with self.__keyboard.pressed(Key.cmd):
                self.__keyboard.type('e')
                self.__keyboard.release(Key.cmd)
        elif what == 'eval':
            with self.__keyboard.pressed(Key.shift):
                self.__keyboard.press(Key.enter)
                self.__keyboard.release(Key.enter)
            time.sleep(0.01)
            self.__keyboard.press(Key.enter)
            self.__keyboard.release(Key.enter)

    def stopSC(self, midinumber):
        """If ``midinumber`` is 66, then stop SuperCollider

        By issueing a cmd-. command.

        :param int midinumber: the midinumber that is played
        """
        if midinumber == 66:
            self.__keyboard.press(Key.cmd)
            self.__keyboard.type('.')
            self.__keyboard.release(Key.cmd)

    def enter(self):
        """Press the enter key.
        """
        self.__keyboard.press(Key.enter)
        self.__keyboard.release(Key.enter)

    def delete(self):
        """Press the backspace key.
        """
        self.__keyboard.press(Key.backspace)
        self.__keyboard.release(Key.backspace)

    def mapping(self, midinumber):
        """Type a letter that is coupled to this midi note.

        :param int midinumber: the midinumber that is played
        """
        # chars and nums
        if midinumber == 87:
            self.__keyboard.type('h')
        elif midinumber == 92:
            self.__keyboard.type('l')
        elif midinumber == 90:
            self.__keyboard.type('e')
        elif midinumber == 94:
            self.__keyboard.type('o')
        elif midinumber == 95:
            self.__keyboard.type('p')
        elif midinumber == 91:
            self.__keyboard.type('n')
        elif midinumber == 89:
            self.__keyboard.type('r')
        elif midinumber == 84:
            self.__keyboard.type('t')
        elif midinumber == 83:
            self.__keyboard.type('s')
        elif midinumber == 80:
            self.__keyboard.type('o')
        elif midinumber == 102:
            self.__keyboard.type('a')
        elif midinumber == 104:
            self.__keyboard.type('f')
        elif midinumber == 106:
            self.__keyboard.type('x')
        elif midinumber == 88:
            self.__keyboard.type('d')
        elif midinumber == 89:
            self.__keyboard.type('r')
        elif midinumber == 103:
            self.__keyboard.type('-')
        elif midinumber == 105:
            self.__keyboard.type('+')
        elif midinumber == 107:
            self.delete()
       # special keys
        elif midinumber == 85:
            self.__keyboard.type('~')
        elif midinumber == 101:
            self.__keyboard.type('=')
        elif midinumber == 98:
            self.evaluateSC('stop')
        elif midinumber == 99:
            self.__keyboard.type('.tempo')
        elif midinumber == 97:
            self.evaluateSC('play')
        elif midinumber == 108:
            self.evaluateSC('eval')
       # numbers keys
        elif midinumber == 77:
            self.__keyboard.type('1')
        elif midinumber == 79:
            self.__keyboard.type('2')
        elif midinumber == 81:
            self.__keyboard.type('3')

class Mapping_Motippets:
    """Mapping for the Motippets prototype.

       Includes Hello World mappings for the Hybrid prototype
    """
    def __init__(self, debug=True):
        if debug:
            print("## Using the Motippets mapping ##")

        #Read config and settings
        self._config = configparser.ConfigParser(delimiters=(':'), comment_prefixes=('#'))
        self._config.read('default_setup.ini')

        try:
            self.__snippet1 = self._config['snippets'].get('snippet1')
            self.__snippet2 = self._config['snippets'].get('snippet2')

            self.__mini_snippet_hi_1 = self._config['snippets'].get('mini_snippet_hi_1')
            self.__mini_unmap_hi_2 = self._config['snippets'].get('mini_unmap_hi_2')

            self.__mini_snippet_hi_2 = self._config['snippets'].get('mini_snippet_hi_2')
            self.__mini_unmap_hi_1 = self._config['snippets'].get('mini_unmap_hi_1')

            self.__mini_snippet_mid_1 = self._config['snippets'].get('mini_snippet_mid_1')
            self.__mini_unmap_mid_2 = self._config['snippets'].get('mini_unmap_mid_2')

            self.__mini_snippet_mid_2 = self._config['snippets'].get('mini_snippet_mid_2')
            self.__mini_snippet_mid_2b = self._config['snippets'].get('mini_snippet_mid_2') # check?
            self.__mini_unmap_mid_1 = self._config['snippets'].get('mini_unmap_mid_1')

            self.__mini_snippet_low_1 = self._config['snippets'].get('mini_snippet_low_1')
            self.__mini_snippet_low_1_amp = self._config['snippets'].get('mini_snippet_low_1_amp')
            self.__mini_unmap_low_1 = self._config['snippets'].get('mini_unmap_low_1')
            self.__mini_unmap_low_2 = self._config['snippets'].get('mini_unmap_low_2')
            self.__mini_unmap_low_3 = self._config['snippets'].get('mini_unmap_low_3')

            self.__mini_snippet_low_2 = self._config['snippets'].get('mini_snippet_low_2')
            self.__mini_snippet_low_1_amp = self._config['snippets'].get('mini_snippet_low_1_amp')
            self.__mini_unmap_low_1 = self._config['snippets'].get('mini_unmap_low_1')
            self.__mini_unmap_low_2 = self._config['snippets'].get('mini_unmap_low_2')
            self.__mini_unmap_low_3 = self._config['snippets'].get('mini_unmap_low_3')

        except KeyError:
            raise LookupError('Missing snippets in the config file.')

        self.__keyboard = Controller()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._osc = udp_client.SimpleUDPClient('127.0.0.1', 57120) #standard supercollider OSC listening port

    def evaluateSC(self, what):
        """Evaluate the SuperCollider command 'what'

        :param string what: the command that should be evaluated
        """
        if what == 'play':
            with self.__keyboard.pressed(Key.cmd):
                self.__keyboard.press(Key.right)
                self.__keyboard.release(Key.right)
            time.sleep(0.01)
            self.__keyboard.type('.play')
            with self.__keyboard.pressed(Key.shift):
                self.__keyboard.press(Key.enter)
                self.__keyboard.release(Key.enter)
            time.sleep(0.01)
            self.__keyboard.press(Key.enter)
            self.__keyboard.release(Key.enter)
        elif what == 'stop':
            with self.__keyboard.pressed(Key.cmd):
                self.__keyboard.press(Key.right)
                self.__keyboard.release(Key.right)
            time.sleep(0.01)
            self.__keyboard.type('.stop')
            with self.__keyboard.pressed(Key.shift):
                self.__keyboard.press(Key.enter)
                self.__keyboard.release(Key.enter)
            time.sleep(0.01)
            self.__keyboard.press(Key.enter)
            self.__keyboard.release(Key.enter)
        elif what == 'alt_eval':
            with self.__keyboard.pressed(Key.cmd):
                self.__keyboard.type('e')
                self.__keyboard.release(Key.cmd)
        elif what == 'eval':
            with self.__keyboard.pressed(Key.shift):
                self.__keyboard.press(Key.enter)
                self.__keyboard.release(Key.enter)
            time.sleep(0.2)
            self.__keyboard.press(Key.enter)
            self.__keyboard.release(Key.enter)
        elif what == 'noEnter_eval':
            with self.__keyboard.pressed(Key.shift):
                self.__keyboard.press(Key.enter)
                self.__keyboard.release(Key.enter)

    def goDown(self):
        """Press command-arrow down and enter.
        """
        with self.__keyboard.pressed(Key.cmd):
            self.__keyboard.press(Key.down)
            self.__keyboard.release(Key.down)
        time.sleep(0.2)
        self.__keyboard.press(Key.enter)
        self.__keyboard.release(Key.enter)

    def enter(self):
        """Press the enter key.
        """
        self.__keyboard.press(Key.enter)
        self.__keyboard.release(Key.enter)

    def delete(self):
        """Press the backspace key.
        """
        self.__keyboard.press(Key.backspace)
        self.__keyboard.release(Key.backspace)


    def mapping(self, midinumber, prototype='Hello World', debug=False):
        """Type a letter that is coupled to this midi note.

        :param int midinumber: the midinumber that is played
        """
        try:
            midis = str(midinumber)
            if midis in self._config[prototype]:
                if debug:
                    print(midinumber, self._config[prototype].get(midis))
                mapped_string = self._config[prototype].get(midis)

                if len(mapped_string) < 2:
                    # chars and nums
                    self.__keyboard.type(mapped_string)
                    self.formatAndSend(mapped_string, display=5, syntax_color='hello:', spacing=False)
                else:
                    # special keys
                    if mapped_string == 'space':
                        self.__keyboard.press(Key.space)
                        self.__keyboard.release(Key.space)
                        self.formatAndSend(' ', display=5, syntax_color='hello:', spacing=False)
                    elif mapped_string == 'enter':
                        self.__keyboard.press(Key.enter)
                        self.__keyboard.release(Key.enter)
                        self.formatAndSend('\n', display=5, syntax_color='hello:', spacing=False)
                    elif mapped_string == 'backspace':
                        self.__keyboard.press(Key.backspace)
                        self.__keyboard.release(Key.backspace)
                        self.formatAndSend('', display=5, syntax_color='delete:', spacing=False)
                    elif mapped_string == 'down':
                        self.goDown()
                        self.formatAndSend('\n', display=5, syntax_color='hello:', spacing=False)
                    elif mapped_string == 'sc-evaluate':
                        self.evaluateSC('noEnter_eval')
                        self.formatAndSend('', display=5, syntax_color='hello:', spacing=False)
                    elif mapped_string == '.tempo':
                        self.__keyboard.type(mapped_string)
                        self.formatAndSend(mapped_string, display=5, syntax_color='hello:', spacing=False)
                    elif mapped_string == '.play':
                        self.__keyboard.type(mapped_string)
                        self.formatAndSend(mapped_string, display=5, syntax_color='hello:', spacing=False)
                    elif mapped_string == 'motippetssc-evaluate':
                        self.evaluateSC('eval')
        except KeyError:
            raise LookupError('Missing hello world information in the config file.')


    def formatAndSend(self, msg='', encoding='utf-8', host='localhost', display=1, syntax_color='', spacing=True):
        """format and prepare a string for sending it over UDP socket

        :param str msg: the string to be sent
        :param str encoding: the character encoding
        :param str host: the UDP server hostname
        :param int display: the UDP destination port
        :param str syntax_color: the tag to use for syntax coloring (loop, primitive, mid, low, hi, snippet)
        :param boolean spacing: wheather to put a \n (new line) before the msg
        """

        if display == 1:
            port = 1111
        elif display == 2:
            port = 2222
        elif display == 3:
            port = 3333
        elif display == 4:
            port = 4444
        elif display == 5:
            port = 5555

        if spacing:
            newline = '\n'
        else:
            newline = ''

        return self.__socket.sendto(bytes(syntax_color+newline+msg, encoding), (host, port))

    def snippets(self, num, configfile='default_setup.ini'):
        """Type code snippets

        :param int num: the id of the code snippet to play
        :param str configfile: the name of the config file to parse
        """

        if num == 1:
            self.__keyboard.type(self.__snippet1)
            self.formatAndSend(self.__snippet1, display=1, syntax_color='snippet:')
            self.evaluateSC('eval')
        elif num == 2:
            self.__keyboard.type(self.__snippet2)
            self.formatAndSend(self.__snippet2, display=2, syntax_color='snippet:')
            self.evaluateSC('eval')

    def miniSnippets(self, snippet_num, pianosection):
        """Type a mini snippet for specific pianosections'utf-8'

        :param int snippet_num: the id of the mini snippet to play
        :param string pianosections: the pianosection that is used ('hi', 'mid', 'low')
        """
        if snippet_num == 1 and pianosection == 'hi':
            self.__keyboard.type(self.__mini_snippet_hi_1)
            self.evaluateSC('eval')
            self.formatAndSend(self.__mini_snippet_hi_1, display=snippet_num, syntax_color='snippet:')
        if snippet_num == 1 and pianosection == 'hi with unmap':
            self.__keyboard.type(self.__mini_snippet_hi_1)
            self.evaluateSC('eval')
            self.formatAndSend(self.__mini_snippet_hi_1, display=snippet_num, syntax_color='snippet:')
            #unmap other motif
            self.__keyboard.type(self.__mini_unmap_hi_2)
            self.evaluateSC('eval')
            self.formatAndSend(self.__mini_unmap_hi_2, display=snippet_num, syntax_color='snippet:')
        if snippet_num == 1 and pianosection == 'mid':
            self.__keyboard.type(self.__mini_snippet_mid_1)
            self.evaluateSC('eval')
            self.formatAndSend(self.__mini_snippet_mid_1, display=5, syntax_color='mid:')
        if snippet_num == 1 and pianosection == 'mid with unmap':
            self.__keyboard.type(self.__mini_snippet_mid_1)
            self.evaluateSC('eval')
            #unmap
            self.__keyboard.type(self.__mini_unmap_mid_2)
            self.evaluateSC('eval')
            self.formatAndSend(self.__mini_unmap_mid_2, display=snippet_num, syntax_color='snippet:')

            ## LOW SECTION
        if snippet_num == 1 and pianosection == 'low':
            self.__keyboard.type(self.__mini_snippet_low_1)
            self.evaluateSC('eval')
            self.formatAndSend(self.__mini_snippet_low_1, display=snippet_num, syntax_color='low:')
        if snippet_num == 1 and pianosection == 'low amp':
            self.__keyboard.type(self.__mini_snippet_low_1_amp)
            self.evaluateSC('eval')
            self.formatAndSend(self.__mini_snippet_low_1_amp, display=snippet_num, syntax_color='low:')
        if snippet_num == 1 and pianosection == 'low with unmap 2':
            self.__keyboard.type(self.__mini_snippet_low_1)
            self.evaluateSC('eval')
            self.formatAndSend(self.__mini_snippet_low_1, display=snippet_num, syntax_color='low:')
            #unmap 2:
            self.__keyboard.type(self.__mini_unmap_low_2)
            self.evaluateSC('eval')
            self.formatAndSend(self.__mini_unmap_low_2, display=snippet_num, syntax_color='low:')
        if snippet_num == 1 and pianosection == 'low with unmap 3':
            self.__keyboard.type(self.__mini_snippet_low_1)
            self.evaluateSC('eval')
            self.formatAndSend(self.__mini_snippet_low_1, display=snippet_num, syntax_color='low:')
            #unmap 3:
            self.__keyboard.type(self.__mini_unmap_low_3)
            self.evaluateSC('eval')
            self.formatAndSend(self.__mini_unmap_low_3, display=snippet_num, syntax_color='low:')
        if snippet_num == 1 and pianosection == 'low amp with unmap 1':
            self.__keyboard.type(self.__mini_snippet_low_1_amp)
            self.evaluateSC('eval')
            self.formatAndSend(self.__mini_snippet_low_1_amp, display=snippet_num, syntax_color='low:')
            #unmap 1:
            self.__keyboard.type(self.__mini_unmap_low_1)
            self.evaluateSC('eval')
            self.formatAndSend(self.__mini_unmap_low_1, display=snippet_num, syntax_color='low:')
        if snippet_num == 1 and pianosection == 'low amp with unmap 2':
            self.__keyboard.type(self.__mini_snippet_low_1_amp)
            self.evaluateSC('eval')
            self.formatAndSend(self.__mini_snippet_low_1, display=snippet_num, syntax_color='low:')
            #unmap 2:
            self.__keyboard.type(self.__mini_unmap_low_2)
            self.evaluateSC('eval')
            self.formatAndSend(self.__mini_unmap_low_2, display=snippet_num, syntax_color='low:')

        # for snippet 2:
        if snippet_num == 2 and pianosection == 'hi':
            self.__keyboard.type(self.__mini_snippet_hi_2)
            self.evaluateSC('eval')
            self.formatAndSend(self.__mini_snippet_hi_2, display=snippet_num, syntax_color='hi:')
        if snippet_num == 2 and pianosection == 'hi with unmap':
            self.__keyboard.type(self.__mini_snippet_hi_2)
            self.evaluateSC('eval')
            self.formatAndSend(self.__mini_snippet_hi_2, display=snippet_num, syntax_color='hi:')
            #unmap other motif
            self.__keyboard.type(self.__mini_unmap_hi_1)
            self.evaluateSC('eval')
            self.formatAndSend(self.__mini_unmap_hi_1, display=snippet_num, syntax_color='hi:')
        if snippet_num == 2 and pianosection == 'mid':
            self.__keyboard.type(self.__mini_snippet_mid_2)
            self.evaluateSC('eval')
            self.formatAndSend(self.__mini_snippet_mid_2, display=snippet_num, syntax_color='mid:')
        if snippet_num == 2 and pianosection == 'mid with unmap':
            self.__keyboard.type(self.__mini_snippet_mid_2b)
            self.evaluateSC('eval')
            self.formatAndSend(self.__mini_snippet_mid_2b, display=snippet_num, syntax_color='mid:')
            #unmap
            self.__keyboard.type(self.__mini_unmap_mid_1)
            self.evaluateSC('eval')
            self.formatAndSend(self.__mini_unmap_mid_1, display=snippet_num, syntax_color='mid:')

            ## LOW SECTION
        if snippet_num == 2 and pianosection == 'low':
            self.__keyboard.type(self.__mini_snippet_low_2)
            self.evaluateSC('eval')
            self.formatAndSend(self.__mini_snippet_low_2, display=snippet_num, syntax_color='low:')
        if snippet_num == 2 and pianosection == 'low with unmap 1':
            self.__keyboard.type(self.__mini_snippet_low_2)
            self.evaluateSC('eval')
            self.formatAndSend(self.__mini_snippet_low_2, display=snippet_num, syntax_color='low:')
            #unmap 1:
            self.__keyboard.type(self.__mini_unmap_low_1)
            self.evaluateSC('eval')
            self.formatAndSend(self.__mini_unmap_low_1, display=snippet_num, syntax_color='low:')
        if snippet_num == 2 and pianosection == 'low with unmap 3':
            self.__keyboard.type(self.__mini_snippet_low_2)
            self.evaluateSC('eval')
            self.formatAndSend(self.__mini_snippet_low_2, display=snippet_num, syntax_color='low:')
            #unmap 3:
            self.__keyboard.type(self.__mini_unmap_low_3)
            self.evaluateSC('eval')
            self.formatAndSend(self.__mini_unmap_low_3, display=snippet_num, syntax_color='low:')


    def tremolo(self, pianoregister, value):
        """Type the tremolo command + the tremolo-value

        :param string pianoregister: the pianoregister the tremolo is played in. Values are: 'hi_1', 'hi_2', 'mid_1', 'mid_2', 'low_1', 'low_2', 'low_3'.
        :param int value: the tremolo value as distance between the notes
        """
        if pianoregister == 'hi_1':
            self.__keyboard.type('~tremoloH1 = ' + str(value))
            self.formatAndSend('~tremoloH1 = ' + str(value), display=1, syntax_color='hi:')
        elif pianoregister == 'hi_2':
            self.__keyboard.type('~tremoloH2 = ' + str(value))
            self.formatAndSend('~tremoloH2 = ' + str(value), display=2, syntax_color='hi:')
        elif pianoregister == 'mid_1':
            self.__keyboard.type('~tremoloM1 = ' + str(value))
            self.formatAndSend('~tremoloM1 = ' + str(value), display=5, syntax_color='mid:')
        elif pianoregister == 'mid_2':
            self.__keyboard.type('~tremoloM2 = ' + str(value))
            self.formatAndSend('~tremoloM2 = ' + str(value), display=2, syntax_color='mid:')
        elif pianoregister == 'low_1':
            self.__keyboard.type('~tremoloL1 = ' + str(value))
            self.formatAndSend('~tremoloL1 = ' + str(value), display=1, syntax_color='low:')
        elif pianoregister == 'low_2':
            self.__keyboard.type('~tremoloL2 = ' + str(value))
            self.formatAndSend('~tremoloL2 = ' + str(value), display=2, syntax_color='low:')
        elif pianoregister == 'low_3':
            self.__keyboard.type('~tremoloL1amp = ' + str(value))
            self.formatAndSend('~tremoloL1amp = ' + str(value), display=1, syntax_color='low:')
        self.evaluateSC('eval')

    def conditional(self, conditional_num):
        """Setup a conditional

        There are three options: settimg up a conditional if number of notes
        played is more than 100 in ... (option 1), setting up a conditional if
        range is more than ... (option 2), and setting up a conditional if range
        is less than ... (option 3).

        :param int conditional_num: the selection for the type of conditional
        """
        if conditional_num == 1:
            self.__keyboard.type('// setting up a conditional: IF number of\
            notes played is more than 100 in...')
            self.enter()
            self.formatAndSend('setting up a conditional: \nIF number of notes played is more than 100 in...', display=3, syntax_color='primitive:')
        elif conditional_num == 2:
            self.__keyboard.type('// setting up an ONGOING conditional: IF range is more than...')
            self.enter()
            self.formatAndSend('setting up an ONGOING conditional: \nIF range is more than...', display=3, syntax_color='primitive:')
        elif conditional_num == 3:
            self.__keyboard.type('// setting up an ONGOING conditional: IF range is less than...')
            self.enter()
            self.formatAndSend('setting up an ONGOING conditional: \nIF range is less than...', display=3, syntax_color='primitive:')

    def result(self, result_num, text, mod=0): #how to make optional params?
        """TOOD: document function

        :param int result_num: type of result?
        :param string text: indication of the type of message
        :param mod: some function
        :type mod: int or None
        """
        if result_num == 1:
            if text == 'comment':
                self.__keyboard.type('// if true -> stop ~snippet2')
                self.enter()
                self.formatAndSend('if true -> stop ~snippet2', display=3, syntax_color='snippet:')
            elif text == 'code':
                self.__keyboard.type('~snippet2.stop(10);')
                self.evaluateSC('eval')
                self.formatAndSend('~snippet2.stop;', display=3, syntax_color='snippet:')
            elif text == 'less than':
                self.__keyboard.type('//less than an 8ve. Nothing happens :(')
                self.evaluateSC('eval')
                self.formatAndSend('if false -> Nothing happens BUUUUU!', display=3, syntax_color='primitive:')

        elif result_num == 2:
            if text == 'comment':
                self.__keyboard.type('// if true -> stop ~snippet1')
                self.enter()
                self.formatAndSend('if true -> stop ~snippet1', display=3, syntax_color='primitive:')
            elif text == 'code':
                self.__keyboard.type('~snippet1.stop(20);')
                self.evaluateSC('eval')
                self.formatAndSend('~snippet1.stop;', display=3)
            elif text == 'less than':
                self.__keyboard.type('//less than an 8ve. Nothing happens :(')
                self.evaluateSC('eval')
                self.formatAndSend('if false -> Nothing happens BUUUUU!', display=3, syntax_color='primitive:')

        elif result_num == 3:
            if text == 'comment':
                self.__keyboard.type('// if true -> play gong sound!')
                self.enter()
                self.formatAndSend('if true -> play gong sound!', display=3, syntax_color='primitive:')
            elif text == 'code':
                #self.__keyboard.type('~gong.play(' + str(mod) + ');')
                #self.evaluateSC('eval')
                self._osc.send_message("/gong", str(mod))
                self.formatAndSend('~gong.play(' + str(mod) + ');', display=3, syntax_color='snippet:')
            elif text == 'less than':
                #self.__keyboard.type('~gong.play(' + str(mod) + ');');
                #self.evaluateSC('eval')
                self._osc.send_message("/gong", str(mod))
                self.formatAndSend('~gong.play(' + str(mod) + ');', display=3, syntax_color='snippet:')


        elif result_num == 4:
            if text == 'comment':
                self.__keyboard.type('HUYGENS! //is activating...')
                self.evaluateSC('eval')
                self.formatAndSend('HUYGENS', display=1, syntax_color='warning:')
                self.formatAndSend('IS', display=2, syntax_color='warning:')
                self.formatAndSend('ACTIVATING...', display=3, syntax_color='warning:')
            elif text == 'start':
                self.__keyboard.type('// HUYGENS countdown started!')
                self.evaluateSC('eval')
                self.formatAndSend('HUYGENS', display=1, syntax_color='warning:')
                self.formatAndSend('COUNTDOWN', display=2, syntax_color='warning:')
                self.formatAndSend('STARTED!', display=3, syntax_color='warning:')
            elif text == 'code':
                self.__keyboard.type("")
                self.enter()
                self.__keyboard.type("  ____   ____   ____  __  __ _ ")
                self.enter()
                self.formatAndSend(" ____ ", display=5, syntax_color='primitive:')
                self.formatAndSend("  ____  ", display=1, syntax_color='primitive:') 
                self.formatAndSend("  ____  ", display=2, syntax_color='primitive:')
                self.formatAndSend(" __  __  ", display=3, syntax_color='primitive:')
                self.formatAndSend(" _ ", display=4, syntax_color='primitive:')
                self.__keyboard.type(" |  _ \ / __ \ / __ \|  \/  | |")
                self.enter()
                self.formatAndSend("|  _ \ ", display=5, syntax_color='primitive:')
                self.formatAndSend(" / __ \ ", display=1, syntax_color='primitive:')
                self.formatAndSend(" / __ \ ", display=2, syntax_color='primitive:')
                self.formatAndSend("|  \/  |", display=3, syntax_color='primitive:')
                self.formatAndSend("| | ", display=4, syntax_color='primitive:')                
                self.__keyboard.type(" | |_) | |  | | |  | | \  / | |")
                self.enter()
                self.formatAndSend("| |_) | ", display=5, syntax_color='primitive:')
                self.formatAndSend("| |  | |", display=1, syntax_color='primitive:')
                self.formatAndSend("| |  | |", display=2, syntax_color='primitive:')
                self.formatAndSend("| \  / |", display=3, syntax_color='primitive:')
                self.formatAndSend("| | ", display=4, syntax_color='primitive:')                
                self.__keyboard.type(" |  _ <| |  | | |  | | |\/| | |")
                self.enter()
                self.formatAndSend("|  _ <| ", display=5, syntax_color='primitive:')
                self.formatAndSend("| |  | |", display=1, syntax_color='primitive:')
                self.formatAndSend("| |  | |", display=2, syntax_color='primitive:')
                self.formatAndSend("| |\/| |", display=3, syntax_color='primitive:')
                self.formatAndSend("| | ", display=4, syntax_color='primitive:')                
                self.__keyboard.type(" | |_) | |__| | |__| | |  | |_|")
                self.enter()
                self.formatAndSend("| |_) | ", display=5, syntax_color='primitive:')
                self.formatAndSend("| |__| |", display=1, syntax_color='primitive:')
                self.formatAndSend("| |__| |", display=2, syntax_color='primitive:')
                self.formatAndSend("| |  | |", display=3, syntax_color='primitive:')
                self.formatAndSend("|_| ", display=4, syntax_color='primitive:')                
                self.__keyboard.type(" |____/ \____/ \____/|_|  |_(_)   (^0^)//¯  AIR DE COUR  THE END ¯\('…')/¯ ")
                self.enter()
                self.formatAndSend("|____/", display=5, syntax_color='primitive:')
                self.formatAndSend(" \____/", display=1, syntax_color='primitive:')
                self.formatAndSend(" \____/", display=2, syntax_color='primitive:')
                self.formatAndSend("|_|  |_|", display=3, syntax_color='primitive:')
                self.formatAndSend("(_) \n\n (^0^)//¯  AIR DE COUR \n\n THE END ¯\('…')/¯ ", display=4, syntax_color='primitive:')                
                self.__keyboard.type("")
                self.enter()
            elif text == 'huygens':
                self.__keyboard.type('~stop.all;')
                self.__keyboard.type('~huygens.eind;') # ~huygens.end to not have the ending Huygens extract
                self.evaluateSC('eval')

        elif result_num == 5:
            if text == 'comment':
                self.__keyboard.type('// if true -> play Huyg')
                self.enter()
                self.formatAndSend('if true -> play Huyg', display=3, syntax_color='primitive:')
            elif text == 'code':
                #self.__keyboard.type('~huygens.stuk('+ str(mod) +');')
                #self.evaluateSC('eval')
                self._osc.send_message("/huygens", str(mod))
                self.formatAndSend('~huygens.stuk(' + str(mod) + ');', display=3, syntax_color='snippet:')
            elif text == 'less than':
                #self.__keyboard.type('~huygens.stuk('+ str(mod) +');')
                #self.evaluateSC('eval')
                self._osc.send_message("/huygens", str(mod))
                self.formatAndSend('~huygens.stuk(' + str(mod) + ');', display=3, syntax_color='snippet:')

        elif result_num == 6:
            if text == 'comment':
                self.__keyboard.type('HUYGENS! //is activating...')
                self.evaluateSC('eval')
            elif text == 'start':
                self.__keyboard.type('// HUYGENS countdown started!')
                self.evaluateSC('eval')
            elif text == 'code':
                self.__keyboard.type("")
                self.enter()
                self.__keyboard.type("  ____   ____   ____  __  __ _ ")
                self.enter()
                self.__keyboard.type(" |  _ \ / __ \ / __ \|  \/  | |")
                self.enter()
                self.__keyboard.type(" | |_) | |  | | |  | | \  / | |")
                self.enter()
                self.__keyboard.type(" |  _ <| |  | | |  | | |\/| | |")
                self.enter()
                self.__keyboard.type(" | |_) | |__| | |__| | |  | |_|")
                self.enter()
                self.__keyboard.type(" |____/ \____/ \____/|_|  |_(_)   (^0^)//¯  AIR DE COUR  ¯\\(^0^) ")
                self.enter()
                self.__keyboard.type("")
                self.enter()
            elif text == 'huygens':
                self.__keyboard.type('~huygens.end')
                self.evaluateSC('eval')

    def customPass(self, name, content, osc_only=False):
        """
        post custom string message on codespace and display

        :param string name: a label to print in front of the string
        :param string content: the message or content
        """
        self.formatAndSend(name + " " + content, display=3, syntax_color='comment:')            

        if not osc_only:
            self.__keyboard.type(name + " " + content) 
            self.enter()


    def onlyDisplay(self, content, tag=1, warning=False):
        """
        print a custom string on the UDP display only!

        :param string content: the message or content
        :param int tag: the reference to a color tag
        :param warning: wether to print the message with the warning color tag (i.e. red)

        """
        if warning:
            self.formatAndSend(content, display=4, syntax_color='warning:')
        else:
            if tag == 2:
                self.formatAndSend(content, display=4, syntax_color='loop2:')
            elif tag == 3:
                self.formatAndSend(content, display=4, syntax_color='loop3:')
            else:
                self.formatAndSend(content, display=4, syntax_color='loop:')

class Mapping_Ckalculator:
    """Mapping for the Ckalculator prototype.
    """
    def __init__(self, use_display=False, debug=True):
        if debug:
            print("## Using the Ckalculator mapping ##")

        self.__keyboard = Controller()

        if use_display:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self._osc = udp_client.SimpleUDPClient('127.0.0.1', 57120)


    def formatAndSend(self, msg='', encoding='utf-8', host='localhost', display=1, syntax_color=':', spacing=True, spacechar=' '):
        """format and prepare a string for sending it over UDP socket

        :param str msg: the string to be sent
        :param str encoding: the character encoding
        :param str host: the UDP server hostname
        :param int display: the UDP destination port
        :param str syntax_color: the tag to use for syntax coloring (loop, primitive, mid, low, hi, snippet)
        :param boolean spacing: wheather to put a \n (new line) before the msg
        :param boolean spacechar: the character to place in between the msgs. Can be ''
        """

        if display == 1:
            port = 1111
        elif display == 2:
            port = 2222
        elif display == 3:
            port = 3333

        if spacing:
            newline = '\n'
        else:
            newline = spacechar

        return self.__socket.sendto(bytes(syntax_color+msg+newline, encoding), (host, port))

    def newLine(self, display=1):
        """
        send a new line to the code display
        """
        if display == 1:
            port = 1111
        elif display == 2:
            port = 2222
        elif display == 3:
            port = 3333

        return self.__socket.sendto(bytes('line:\n', 'utf-8'), ('localhost', port))
