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
import configparser

display1 = 1111
display2 = 2222
display3 = 3333
display4 = 4444
display5 = 5555

class Mapping_HelloWorld():
    """Mapping for the Hello World prototype.

    :param use_display boolean: set if code should be printed in UDP display
    """

    def __init__(self, use_display=False):
        """Init the class

        Print that the user is using this mapping and set the controller.
        """
        print("## Using the Hello World mapping ##")

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

    def mapping(self, midinumber):
        """Type a letter that is coupled to this midi note.

        :param int midinumber: the midinumber that is played
        """
        # chars and nums
        if midinumber == 69:
            self.__keyboard.type('h')
            self.formatAndSend('h', display=2)
        elif midinumber == 74:
            self.__keyboard.type('l')
            self.formatAndSend('l', display=2)
        elif midinumber == 63:
            self.__keyboard.type('e')
            self.formatAndSend('e', display=2)
        elif midinumber == 80:
            self.__keyboard.type('o')
            self.formatAndSend('o', display=2)
        elif midinumber == 68:
            self.__keyboard.type('o')
            self.formatAndSend('o', display=2)
        elif midinumber == 81:
            self.__keyboard.type('r')
            self.formatAndSend('r', display=2)
        elif midinumber == 88:
            self.__keyboard.type('w')
            self.formatAndSend('w', display=2)
        elif midinumber == 64:
            self.__keyboard.type('d')
            self.formatAndSend('d', display=2)
        elif midinumber ==48:
            self.__keyboard.type('t')
            self.formatAndSend('t', display=2)
        elif midinumber == 47:
            self.__keyboard.type('s')
            self.formatAndSend('s', display=2)
        elif midinumber == 38:
            self.__keyboard.type('a')
            self.formatAndSend('a', display=2)
        elif midinumber == 40:
            self.__keyboard.type('n')
            self.formatAndSend('n', display=2)
        elif midinumber == 42:
            self.__keyboard.type('i')
            self.formatAndSend('i', display=2)
        elif midinumber == 44:
            self.__keyboard.type('o')
            self.formatAndSend('o', display=2)
        elif midinumber == 45:
            self.__keyboard.type('p')
            self.formatAndSend('p', display=2)
        elif midinumber == 59:
            self.__keyboard.type('0')
            self.formatAndSend('0', display=2)
        elif midinumber == 60:
            self.__keyboard.type('1')
            self.formatAndSend('1', display=2)
        elif midinumber == 61:
            self.__keyboard.type('2')
            self.formatAndSend('2', display=2)
        elif midinumber == 62:
            self.__keyboard.type('3')
            self.formatAndSend('3', display=2)
        elif midinumber == 89:
            self.__keyboard.type('4')
            self.formatAndSend('4', display=2)
        elif midinumber == 90:
            self.__keyboard.type('5')
            self.formatAndSend('5', display=2)
        elif midinumber == 91:
            self.__keyboard.type('6')
            self.formatAndSend('6', display=2)
        elif midinumber == 92:
            self.__keyboard.type('7')
            self.formatAndSend('7', display=2)
        elif midinumber == 93:
            self.__keyboard.type('8')
            self.formatAndSend('8', display=2)
        elif midinumber == 94:
            self.__keyboard.type('9')
            self.formatAndSend('9', display=2)
        elif midinumber == 46:
            self.__keyboard.type('m')
            self.formatAndSend('m', display=2)
        elif midinumber == 99:
            self.__keyboard.type('j')
            self.formatAndSend('j', display=2)
        elif midinumber == 104:
            self.__keyboard.type('y')
            self.formatAndSend('y', display=2)
       # special keys
        elif midinumber == 56:
            self.__keyboard.press(Key.space)
            self.__keyboard.release(Key.space)
            self.formatAndSend('\n', display=2)
        elif midinumber == 32:
            self.__keyboard.press(Key.enter)
            self.__keyboard.release(Key.enter)
            self.evaluateSC()
            self.formatAndSend('\nevaluate\n', display=2)
        elif midinumber == 50:
            self.__keyboard.type('~')
            self.formatAndSend('~', display=2)
        elif midinumber == 51:
            self.__keyboard.type('+')
            self.formatAndSend('+', display=2)
        elif midinumber == 54:
            self.__keyboard.type('-')
            self.formatAndSend('-', display=2)
        elif midinumber == 49:
            self.__keyboard.type('=')
            self.formatAndSend('=', display=2)
        elif midinumber == 103:
            self.__keyboard.type('?')
            self.formatAndSend('?', display=2)
        elif midinumber == 105:
            self.__keyboard.type('.!')
            self.formatAndSend('.!', display=2)
        elif midinumber == 95:
            self.__keyboard.press(Key.backspace)
            self.__keyboard.release(Key.backspace)
      # supercollider commands:
        elif midinumber == 33:
            self.evaluateSC()
            self.formatAndSend('\nevaluate\n', display=2)
        elif midinumber == 22:
            self.__keyboard.type('.tempo')
            self.formatAndSend('.tempo', display=2)
        elif midinumber == 21:
            self.__keyboard.type('.play')
            self.formatAndSend('.play', display=2)
        elif midinumber == 102:
            self.__keyboard.type('TempoClock.default')
            self.formatAndSend('TempoClock.default', display=2)
    
      

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
    
       Includes HelloWorld mappings for the Hybrid prototype  
    """
    def __init__(self, debug=True):
        if debug:
            print("## Using the Motippets mapping ##")

        #Read config and settings
        config = configparser.ConfigParser(delimiters=(':'), comment_prefixes=('#'))
        config.read('default_setup.ini')

        try:
            self.__snippet1 = config['snippets'].get('snippet1')
            self.__snippet2 = config['snippets'].get('snippet2')

            self.__mini_snippet_hi_1 = config['snippets'].get('mini_snippet_hi_1')
            self.__mini_unmap_hi_2 = config['snippets'].get('mini_unmap_hi_2')

            self.__mini_snippet_hi_2 = config['snippets'].get('mini_snippet_hi_2')
            self.__mini_unmap_hi_1 = config['snippets'].get('mini_unmap_hi_1')

            self.__mini_snippet_mid_1 = config['snippets'].get('mini_snippet_mid_1')
            self.__mini_unmap_mid_2 = config['snippets'].get('mini_unmap_mid_2')

            self.__mini_snippet_mid_2 = config['snippets'].get('mini_snippet_mid_2')
            self.__mini_snippet_mid_2b = config['snippets'].get('mini_snippet_mid_2') # check?
            self.__mini_unmap_mid_1 = config['snippets'].get('mini_unmap_mid_1')

            self.__mini_snippet_low_1 = config['snippets'].get('mini_snippet_low_1')
            self.__mini_snippet_low_1_amp = config['snippets'].get('mini_snippet_low_1_amp')
            self.__mini_unmap_low_1 = config['snippets'].get('mini_unmap_low_1')
            self.__mini_unmap_low_2 = config['snippets'].get('mini_unmap_low_2')
            self.__mini_unmap_low_3 = config['snippets'].get('mini_unmap_low_3')

            self.__mini_snippet_low_2 = config['snippets'].get('mini_snippet_low_2')
            self.__mini_snippet_low_1_amp = config['snippets'].get('mini_snippet_low_1_amp')
            self.__mini_unmap_low_1 = config['snippets'].get('mini_unmap_low_1')
            self.__mini_unmap_low_2 = config['snippets'].get('mini_unmap_low_2')
            self.__mini_unmap_low_3 = config['snippets'].get('mini_unmap_low_3')

        except KeyError:
            raise LookupError('Missing snippets in the config file.')

        self.__keyboard = Controller()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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


    def mapping(self, midinumber, prototype='Hello World'):
        """Type a letter that is coupled to this midi note.

        :param int midinumber: the midinumber that is played
        """
        # chars and nums
        if midinumber == 69:
            self.__keyboard.type('h')
            self.formatAndSend('h', display=5)
        elif midinumber == 74:
            self.__keyboard.type('l')
            self.formatAndSend('l', display=5)
        elif midinumber == 63:
            self.__keyboard.type('e')
            self.formatAndSend('e', display=5)
        elif midinumber == 80:
            self.__keyboard.type('o')
            self.formatAndSend('o', display=5)
        elif midinumber == 68:
            self.__keyboard.type('o')
            self.formatAndSend('o', display=5)
        elif midinumber == 81:
            self.__keyboard.type('r')
            self.formatAndSend('r', display=5)
        elif midinumber == 88:
            self.__keyboard.type('w')
            self.formatAndSend('w', display=5)
        elif midinumber == 64:
            self.__keyboard.type('d')
            self.formatAndSend('d', display=5)
        elif midinumber ==48:
            self.__keyboard.type('t')
            self.formatAndSend('t', display=5)
        elif midinumber == 47:
            self.__keyboard.type('s')
            self.formatAndSend('s', display=5)
        elif midinumber == 38:
            self.__keyboard.type('a')
            self.formatAndSend('a', display=5)
        elif midinumber == 40:
            self.__keyboard.type('n')
            self.formatAndSend('n', display=5)
        elif midinumber == 42:
            self.__keyboard.type('i')
            self.formatAndSend('i', display=5)
        elif midinumber == 44:
            self.__keyboard.type('o')
            self.formatAndSend('o', display=5)
        elif midinumber == 45:
            self.__keyboard.type('p')
            self.formatAndSend('p', display=5)
        elif midinumber == 59:
            self.__keyboard.type('0')
            self.formatAndSend('0', display=5)
        elif midinumber == 60:
            self.__keyboard.type('1')
            self.formatAndSend('1', display=5)
        elif midinumber == 61:
            self.__keyboard.type('2')
            self.formatAndSend('2', display=5)
        elif midinumber == 62:
            self.__keyboard.type('3')
            self.formatAndSend('3', display=5)
        elif midinumber == 89:
            self.__keyboard.type('4')
            self.formatAndSend('4', display=5)
        elif midinumber == 90:
            self.__keyboard.type('5')
            self.formatAndSend('5', display=5)
        elif midinumber == 91:
            self.__keyboard.type('6')
            self.formatAndSend('6', display=5)
        elif midinumber == 92:
            self.__keyboard.type('7')
            self.formatAndSend('7', display=5)
        elif midinumber == 93:
            self.__keyboard.type('8')
            self.formatAndSend('8', display=5)
        elif midinumber == 94:
            self.__keyboard.type('9')
            self.formatAndSend('9', display=5)
        elif midinumber == 46:
            self.__keyboard.type('m')
            self.formatAndSend('m', display=5)
        elif midinumber == 99:
            self.__keyboard.type('j')
            self.formatAndSend('j', display=5)
        elif midinumber == 104:
            self.__keyboard.type('y')
            self.formatAndSend('y', display=5)
       # special keys
        elif midinumber == 56:
            self.__keyboard.press(Key.space)
            self.__keyboard.release(Key.space)
            self.formatAndSend('\n', display=5)
        elif midinumber == 32:
            self.__keyboard.press(Key.enter)
            self.__keyboard.release(Key.enter)
            self.evaluateSC('eval')
            self.formatAndSend('\nevaluate\n', display=5)
        elif midinumber == 50:
            self.__keyboard.type('~')
            self.formatAndSend('~', display=5)
        elif midinumber == 51:
            self.__keyboard.type('+')
            self.formatAndSend('+', display=5)
        elif midinumber == 54:
            self.__keyboard.type('-')
            self.formatAndSend('-', display=5)
        elif midinumber == 49:
            self.__keyboard.type('=')
            self.formatAndSend('=', display=5)
        elif midinumber == 103:
            self.__keyboard.type('?')
            self.formatAndSend('?', display=5)
        elif midinumber == 105:
            self.__keyboard.type('.!')
            self.formatAndSend('.!', display=5)
        elif midinumber == 95:
            self.__keyboard.press(Key.backspace)
            self.__keyboard.release(Key.backspace)
      # supercollider commands:
        elif midinumber == 33:
            self.evaluateSC('eval')
            self.formatAndSend('\nevaluate\n', display=5)
        elif midinumber == 22:
            self.__keyboard.type('.tempo')
            self.formatAndSend('.tempo', display=5)
        elif midinumber == 21:
            self.__keyboard.type('.play')
            self.formatAndSend('.play', display=5)
        elif midinumber == 102:
            self.__keyboard.type('TempoClock.default')
            self.formatAndSend('TempoClock.default', display=5)
        elif midinumber == 108:
            self.goDown()         
    # motippets only commands:
        elif prototype == 'Motippets':
            if midinumber == 66:
                self.evaluateSC('eval')       
    
    def formatAndSend(self, msg='', encoding='utf-8', host='localhost', display=1, syntax_color=''):
        """format and prepare a string for sending it over UDP socket

        :param str msg: the string to be sent
        :param str encoding: the character encoding
        :param str host: the UDP server hostname
        :param int display: the UDP destination port
        :param str syntax_color: the tag to use for syntax coloring (loop, primitive, mid, low, hi, snippet)
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

        return self.__socket.sendto(bytes(syntax_color+'\n'+msg, encoding), (host, port))

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

        TODO: consider - should we put this in a snippet config file?

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
            self.formatAndSend(self.__mini_snippet_mid_1, display=snippet_num, syntax_color='snippet:')
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
            self.formatAndSend('~tremoloM1 = ' + str(value), display=1, syntax_color='mid:')
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
                self.__keyboard.type('~snippet2.stop;')
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
                self.__keyboard.type('~snippet1.stop;')
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
                self.__keyboard.type('~gong.play(' + str(mod) + ');')
                self.evaluateSC('eval')
                self.formatAndSend('~gong.play(' + str(mod) + ');', display=3, syntax_color='snippet:')
            elif text == 'less than':
                self.__keyboard.type('~gong.play(' + str(mod) + ');');
                self.evaluateSC('eval')
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
                self.formatAndSend("  ____   ____   ____  __  __ _ ", display=1, syntax_color='primitive:')
                self.formatAndSend("  ____   ____   ____  __  __ _ ", display=2, syntax_color='primitive:')
                self.formatAndSend("  ____   ____   ____  __  __ _ ", display=3, syntax_color='primitive:')
                self.__keyboard.type(" |  _ \ / __ \ / __ \|  \/  | |")
                self.enter()
                self.formatAndSend(" |  _ \ / __ \ / __ \|  \/  | |", display=1, syntax_color='primitive:')
                self.formatAndSend(" |  _ \ / __ \ / __ \|  \/  | |", display=2, syntax_color='primitive:')
                self.formatAndSend(" |  _ \ / __ \ / __ \|  \/  | |", display=3, syntax_color='primitive:')
                self.__keyboard.type(" | |_) | |  | | |  | | \  / | |")
                self.enter()
                self.formatAndSend(" | |_) | |  | | |  | | \  / | |", display=1, syntax_color='primitive:')
                self.formatAndSend(" | |_) | |  | | |  | | \  / | |", display=2, syntax_color='primitive:')
                self.formatAndSend(" | |_) | |  | | |  | | \  / | |", display=3, syntax_color='primitive:')
                self.__keyboard.type(" |  _ <| |  | | |  | | |\/| | |")
                self.enter()
                self.formatAndSend(" |  _ <| |  | | |  | | |\/| | |", display=1, syntax_color='primitive:')
                self.formatAndSend(" |  _ <| |  | | |  | | |\/| | |", display=2, syntax_color='primitive:')
                self.formatAndSend(" |  _ <| |  | | |  | | |\/| | |", display=3, syntax_color='primitive:')
                self.__keyboard.type(" | |_) | |__| | |__| | |  | |_|")
                self.enter()
                self.formatAndSend(" | |_) | |__| | |__| | |  | |_|", display=1, syntax_color='primitive:')
                self.formatAndSend(" | |_) | |__| | |__| | |  | |_|", display=2, syntax_color='primitive:')
                self.formatAndSend(" | |_) | |__| | |__| | |  | |_|", display=3, syntax_color='primitive:')
                self.__keyboard.type(" |____/ \____/ \____/|_|  |_(_)   (^0^)//¯  AIR DE COUR  THE END ¯\('…')/¯ ")
                self.enter()
                self.formatAndSend(" |____/ \____/ \____/|_|  |_(_)   (^0^)//¯  AIR DE COUR  THE END ¯\('…')/¯ ", display=1, syntax_color='primitive:')
                self.formatAndSend(" |____/ \____/ \____/|_|  |_(_)   (^0^)//¯  AIR DE COUR  THE END ¯\('…')/¯ ", display=2, syntax_color='primitive:')
                self.formatAndSend(" |____/ \____/ \____/|_|  |_(_)   (^0^)//¯  AIR DE COUR  THE END ¯\('…')/¯ ", display=3, syntax_color='primitive:')
                self.__keyboard.type("")
                self.enter()
            elif text == 'huygens':
                self.__keyboard.type('~huygens.end;')
                self.evaluateSC('eval')

        elif result_num == 5:
            if text == 'comment':
                self.__keyboard.type('// if true -> play Huyg')
                self.enter()
                self.formatAndSend('if true -> play Huyg', display=3, syntax_color='primitive:')
            elif text == 'code':
                self.__keyboard.type('~huygens.stuk('+ str(mod) +');')
                self.evaluateSC('eval')
                self.formatAndSend('~huygens.stuk(' + str(mod) + ');', display=3, syntax_color='snippet:')
            elif text == 'less than':
                self.__keyboard.type('~huygens.stuk('+ str(mod) +');')
                self.evaluateSC('eval')
                self.formatAndSend('~huygens.stuk(' + str(mod) + ');', display=3, syntax_color='snippet:')

    def customPass(self, name, content):
        """
        post custom string message on codespace and display
        
        :param string name: a label to print in front of the string
        :param string content: the message or content
        """
        self.__keyboard.type(name + " " + content)
        self.enter()
        self.formatAndSend(name + " " + content, display=3, syntax_color='comment:')

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
