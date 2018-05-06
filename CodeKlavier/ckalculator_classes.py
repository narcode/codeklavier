#!/usr/bin/env python3

import rtmidi
from Motifs import motifs as LambdaMapping

class Ckalculator(object):
    """Ckalculator Class
    
    The main class behind the Ckalculator prototype. Lambda calculus with the piano (simple arithmetic operations)
    """
    
    def __init__(self, mapping, noteonid, noteoffid):
        """The method to initialise the class and prepare the class variables.
        """
        self.mapscheme = mapping
        self.note_on = noteonid
        self.note_off = noteoffid
        self._memory = []
        self._conditionalsBuffer = []
        self._pianosections = []
        
    def parse_midi(self, event, section, ck_deltatime=0, target=0):
        """Parse the midi signal and process it depending on the register.

        :param tuple event: describes the midi event that was received
        :param string section: the MIDI piano range (i.e. low register, mid or high)
        :param float ck_deltatime: the deltatime between incoming note-on MIDI messages
        :param int target: target the parsing for a specific snippet. 0 is no target
        """   
        
        message, deltatime = event


        if (message[0] == self.note_on):
            note = message[1]
            self._deltatime = ck_deltatime 
            
            ### lambda calculus ###
            
    
    def memorize(self, midinote, length, debug=False, debugname="Ckalculator", conditional="off"):
        """Store the incoming midi notes by appending to the memory array.

        :param midinote: the incoming MIDI note message\n
        :param int length: the size of the array to store the midinotes\n
        :param boolean debug: flag to print console debug messages\n
        :param string debugname: prefix for the debug messages
        :param string conditional: if a parallel buffer is filled in for the conditional functions
        """
        self._memory.append(midinote)

        if len(self._memory) > length:
            self._memory = self._memory[-length:]

        if debug == True:
            print(debugname, ','.join(map(str, self._memory)))
            if conditional == "on":
                print(debugname + ','.join(map(str, self._conditionalsBuffer)))

        if conditional == "on":
            self._conditionalsBuffer.append(midinote)
            if len(self._conditionalsBuffer) > length:
                self._conditionalsBuffer = self._conditionalsBuffer[-length:]
                
    
class CK_lambda(object):
    """CK_lambda Class
    
    The main class containing basic Lambda calculus expressions
    """    
    
    def __init__(self):
        self._type = 'function'
    
    def zero(self, body=''):
        """
        lambda identity function. Also represents 0 (zero)\n
        returns the function/argument it was applied to\n
        (in lambda notation: ƛx.x)\n
        \n
        :param function body: body variable to replace with the application argument\n
        """
        return body
    
    def true(self, function1):
        """
        lambda select first function. Also represents TRUE\n
        returns the first variable (function1)\n 
        (in lambda notation: ƛx.ƛy.x)\n
        \n
        :param function function1: expression that will be returned\n
        :param function function2: expression that will be discarded/destroyed\n
        """
        def select_first(function2):
            return function1
        
        return select_first
           
    
    def false(self, function1):
        """
        lambda select second function. Also represents FALSE\n
        returns the second variable (function2)\n 
        (in lambda notation: ƛx.ƛy.y)\n
        \n
        :param function function1: expression that will be discarded/destroyed\n
        :param function function2: expression that will be returned\n
        """ 
        def select_second(function2):
            return function2
        
        return select_second
    
    
    def simpleApply(self, function1, *functions):
        """
        lambda application of functions. 
        
        :param function function1: the function to apply to the next functions in *functions
        :param function *functions: the function(s) to treat as argument(s) for the application 
        """
        
        functions_array = []
                
        for f in functions:
            if callable(f):
                functions_array.append(f)
                
        if len(functions_array) < len(functions):
            print('not all arguments are functions!')
            return
                
        print(functions_array)

        if callable(function1):
            # TODO: think if a loop is doable...
            if len(functions_array) == 1:
                return function1(functions_array[0])()
            elif len(functions_array) == 2:
                return function1(functions_array[0])(functions_array[1])()
            elif len(functions_array) == 3:
                return function1(functions_array[0])(functions_array[1])\
                    (functions_array[2])
            elif len(functions_array) == 4:
                return function1(functions_array[0])(functions_array[1])\
                    (functions_array[2])(functions_array[3])
        
        
    def test_func(arg=''):
        return "narcode"
        
        
        
    

    