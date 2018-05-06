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
    
    def zero(body):
        """
        lambda identity function. Also represent 0 (zero)\n
        returns the function/argument it was applied to        
        
        :param any body: body variable to replace with the application argument
        """
        
        return body
    
    
    def apply(function1, function2):
        """
        lambda application of 2 functions. 
        
        :param function function1: the function to apply 
        :param function function2: the function to treat as argument for the application 
        """
        
        if callable(function1) and callable(function2):
            return function1(function2)()
        else: 
            print('arguments need to be function expressions!')
            
        
    def test_func():
        return "narcode"
        
        
        
    

    