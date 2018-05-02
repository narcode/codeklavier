#!/usr/bin/env python3

class CK_display(object):
    """
    Class to handle display functionality
    """
    
    def __init__(self, num_displays):
        """
        initialize the number of display's and the corresponding UDP ports
        """        
        self._display1 = 1111
        self._display2 = 2222
        self._display3 = 3333
        self._display4 = 4444
        self._display5 = 5555
        
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