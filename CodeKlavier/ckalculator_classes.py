#!/usr/bin/env python3

import functools
import array
from inspect import signature
import random
import configparser
import numpy as np
#from multiprocessing import Pool
from multiprocessing.pool import ThreadPool, Pool
#from pyparsing import Literal,CaselessLiteral,Word,Combine,Group,Optional,\
    #ZeroOrMore,Forward,nums,alphas
#import operator
from Motifs import motifs_lambda as LambdaMapping
from Mapping import Mapping_Ckalculator
from CK_lambda import *
from CK_parser import *

class Ckalculator(object):
    """Ckalculator Class
    
    The main class behind the Ckalculator prototype. Lambda calculus with the piano (simple arithmetic operations)
    TODO: _fullStack is not used yet but added for the future. Evaluate the decision and either implement or deprecate
    """
    
    def __init__(self, noteonid, noteoffid, pedal_id, debug=False, print_functions=False):
        """The method to initialise the class and prepare the class variables.
        """
        
        self.mapscheme = Mapping_Ckalculator(True, False)
        self.note_on = noteonid
        self.note_off = noteoffid
        self.pedal = pedal_id
        self._note_on_cue = []
        self._memory = []
        self._functionStack = []
        self._numberStack = []
        self._tempNumberStack = []
        self._successorHead = []
        self._conditionalsBuffer = []
        self._pianosections = []
        self._fullStack = []
        self._evalStack = []
        self._tempStack = []
        self._temp = False
        self._tempFunctionStack = []
        self.oscName = "ck"
        self._nonMappedNoteCounter = 0
        self._notesList = []
        self._pianoRange = []
        self._fullMemory = []
        self._filtered_cue = []
        self._postOstinatoMemory = []
        self.ostinato = {'first': [], 'compare': []}
        self._foundOstinato = False
        self._developedOstinato = False
        self._functionBody = {}
        self._numForFunctionBody = None
        self._pool = ThreadPool(processes=1)
        self._memories = {}
        self.parser = CK_Parser()
        self._noteon_delta = {}
        self._lastnotes = []
        self._lastdeltas = []
        self._defineCounter = 0
        self._arg1Counter = 0
        self._arg2Counter = 0
        
        # fill/define the piano range:
        self._pianoRange = array.array('i', (i for i in range (21, 109)))

        # get all "meaningful" mapping notes:
        for item in list(LambdaMapping.values()):
            for sub_item in item:
                if sub_item > 0:
                    self._notesList.append(sub_item)
                    
        if debug:
            print('valid notes:', self._notesList)
        
        if print_functions:
            for f in self.ckFunc():
                function_print = (',').join(midiToNotes(f['name'])) + ' -> (' + f['body']['func'] + ' ' + \
                f['body']['arg1str'] + ' ' + f['body']['var'] + ')'
                self.mapscheme.formatAndSend(function_print, display=4, syntax_color='function:')
                

    def parse_midi(self, event, section, ck_deltatime_per_note=0, ck_deltatime=0,
                   articulation={'staccato': 0.1, 'sostenuto': 0.8, 'chord': 0.02}, sendToDisplay=True):
        """Parse the midi signal and process it depending on the register.

        :param tuple event: describes the midi event that was received
        :param string section: the MIDI piano range (i.e. low register, mid or high)
        :param float ck_deltatime_per_note: the note durations
        :param int target: target the parsing for a specific snippet. 0 is no target
        :param list articulation: array containg the threshold in deltatime values for articulation (i.e. staccato, sostenuto, etc.)
        """   
        
        message, deltatime = event

        if (message[0] == self.pedal):
            if message[2] == 127 and (')' in self._fullStack or self._temp == False):
                print('(')
                if sendToDisplay:
                    self.mapscheme.formatAndSend('(', display=2, syntax_color='int:', spacing=False)
                self._fullStack.append('(')
                self._tempStack = []
                self._tempStack.append('(')                
                self._temp = True
            elif message[2] == 0 and '(' in self._fullStack: #could also be: and self._temp = True
                print(')')
                if sendToDisplay:
                    self.mapscheme.formatAndSend(')', display=2, syntax_color='int:', spacing=False)                
                self._fullStack.append(')')
                # to main stack
                print('temp num stack:', self._tempNumberStack);
                if len(self._tempNumberStack) > 0:
                    self._numberStack.append(self._tempNumberStack.pop())
                #self.evaluateTempStack(self._tempStack)
                self._tempFunctionStack = []
                self._tempNumberStack = []
                self._temp = False
                self._fullStack = []
            
        if message[0] == self.note_on and message[2] > 0:

            if section == 'ostinatos':
                if not self._developedOstinato:
                    self._note_on_cue.append(message[1])
                    #self.find_ostinato(self._fullMemory, debug=True)
                    #print('note on mem:', self._note_on_cue)
                else:
                    if self._functionBody == '':
                        print('ostinato developed, awaiting arithmetic function')
                        self.mapscheme.formatAndSend('ostinato developed, awaiting arithmetic function', display=2, 
                                                     syntax_color='result:')
                        
        #print(self._noteon_delta)

        if message[0] == self.note_off or (message[0] == self.note_on and message[2] == 0):
            note = message[1]
            self._deltatime = ck_deltatime_per_note 
            #print('note: ', note, 'Articulation delta: ', ck_deltatime_per_note)

            
            if self.wrong_note(note, False):
                #self._nonMappedNoteCounter += 1
                #print(self._nonMappedNoteCounter)
                self.shift_mapping(1, 'random')

            #else: #no worng note for now... 
            
            if section == 'ostinatos':
                if not self._developedOstinato:
                    self._fullMemory.append(note)
                    self.find_ostinato(self._fullMemory, debug=False)                        
                else:
                    if len(self._functionBody) < 2:
                        print('define func body...')
                        if self._defineCounter == 0:
                            self.mapscheme.formatAndSend('define func body...', display=4, syntax_color='function:')
                            self._defineCounter += 1
                        self.define_function_body(note, articulation)
                    
                             
            if section == 'full':        
                
        ########### CK function definition ############
                #print('incoming:', note)
                self._lastnotes.append(note) # coming from note on messages in main()
                self._lastdeltas.append(self._noteon_delta[note])
                if len(self._lastnotes) > 2:
                    self._lastnotes = self._lastnotes[-2:]
                if len(self._lastdeltas) > 2:
                    self._lastdeltas = self._lastdeltas[-2:]
                    
                last_events = sorted(self._noteon_delta.values())[-2:]
                last_events_new = np.diff(sorted(self._lastdeltas))
                #for n in self._noteon_delta.items():
                    #for l in last_events:
                        #if l in n:
                            #self._lastnotes.append(n)
                #print(self._noteon_delta[note])
                #print('last events:', last_events)
                #print('last notes:', self._lastnotes)
                #print('last deltas:', self._lastdeltas)
                #print('diff: ', last_events[-1] - last_events[0])
                #print('diff new: ', last_events_new)

                
                if last_events_new < 0.03: #deltatime tolerance between the notes of a chord
                    chordparse = self._pool.apply_async(self.parser.parseChordTuple, args=(self._lastnotes, 4, 
                                                                                self._lastdeltas, 
                                                                                0.03, True)) 
                
                #if last_events[-1] - last_events[0] < 0.03:                    
                    ##spawn thread for detecting chords:
                    #chordparse = self._pool.apply_async(self.parser.parseChord, args=(note, 4, 
                                                                                #self._noteon_delta[note], 
                                                                                #0.03, True))
                    chordfound, chord = chordparse.get()

                    if chordfound:
                        for f in self.ckFunc():
                            with Pool(len(self.ckFunc())) as pool:
                                result = pool.apply_async(self.parser.compareChordRecursive, (f['name'], chord))                              
                                #print('process result for ' + f['ref'], result.get())
                                if result.get():
                                    
                                    try:
                                        function_to_call = getattr(self, f['body']['func'])
                                        func_exists = True
                                    except AttributeError:
                                        #raise NotImplementedError("Class `{}` does not implement `{}`".
                                                                  #format(self.__class__.__name__, 
                                                                         #function_to_call))
                                        func_exists = False
                                        print('function not implemented for now... ')
                                    
                                    if func_exists:
                                        if function_to_call.__name__ not in ['successor', 'predecessor']:
                                            function_to_call(False, sendToDisplay)
                                    
                                            if f['body']['arg1'].__name__ == 'succ1':
                                                self.append_successor(f['body']['arg1'])
                                                self.zeroPlusRec(False, True) ## check 2nd argument    
                                                self._successorHead = []
                                    
                        ########################
                ########### lambda calculus  ###########
                        ########################
                                    
                if note in LambdaMapping.get('successor'):

                    if self._deltatime <= articulation['staccato']:
                        self.successor(successor, sendToDisplay)
                    
                    elif self._deltatime > articulation['staccato']: #this is either the func 'zero' or 'predecessor'
                        
                        if note in [LambdaMapping.get('successor')[0]]:
                            if len(self._numberStack) == 0:
                                self.predecessor(zero, sendToDisplay) # what kind of result is better?
                            else:
                                self.predecessor(predecessor, sendToDisplay)
                                
                        else: #zero + recursive counter:
                            self.zeroPlusRec(sendToDisplay)                         
                                
                        self._successorHead = []
                        
                elif note in LambdaMapping.get('zero'):
                    print('identity')
                    self.zeroPlusRec(sendToDisplay)
                    self._successorHead = []
                                                                            
                elif note in LambdaMapping.get('eval'): # if chord (> 0.02) and which notes? 
                    print('evaluate!')
                    self.mapscheme.newLine(display=1)
                    if len(self._functionStack) > 0 and len(self._numberStack) > 0:
                        self.evaluateFunctionStack(self._functionStack, sendToDisplay=sendToDisplay)
                        if (self._numberStack[0].__name__ is 'succ1'):
                            self._evalStack = []
                            self._evalStack.append(trampolineRecursiveCounter(self._numberStack[0]))
                            if (type(self._evalStack[0]) == int):
                                                               
                                if sendToDisplay:
                                    self.mapscheme.formatAndSend(str(self._evalStack[0]), display=3, \
                                                                 syntax_color='result:')
                                print(self._evalStack[0])
                                self.mapscheme._osc.send_message("/ck", str(self._evalStack[0]))
                                
                                # Huygens easter eggs
                                self.easterEggs(number=str(self._evalStack[0]), debug=True, sendToDisplay=sendToDisplay)
                                
                            else: 
                                if sendToDisplay:
                                    self.mapscheme.formatAndSend('error', display=3, syntax_color='error:')
                                    self.mapscheme.formatAndSend('result is not a number', display=3, syntax_color='e_debug:')
                                   
                                    self.mapscheme._osc.send_message("/ck_error", str(self._evalStack[0]))
                                
                                
                        
                        else:
                            #print(self.oscName)
                            if sendToDisplay:
                                self.mapscheme.formatAndSend(self._numberStack[0].__name__, display=3, \
                                                             syntax_color='result:')
                            self.mapscheme._osc.send_message("/"+self.oscName, self._numberStack[0].__name__)
                            
                        self._functionStack = []
                    
                elif note in LambdaMapping.get('predecessor'):
                    print('used via articulation under 1 successor')
                        
                elif note in LambdaMapping.get('addition'):
                    if self._deltatime <= articulation['staccato']:
                        if not self._temp:
                            self.add(False, sendToDisplay)
                        else:
                            self.add(temp=True)
                    elif self._deltatime > articulation['staccato']:
                        if not self._temp:
                            self.multiply(False, sendToDisplay) 
                        else:
                            self.multiply(True, sendToDisplay)                    
                    
                elif note in LambdaMapping.get('subtraction'):
                    if self._deltatime <= articulation['staccato']:                
                        if not self._temp:
                            self.subtract(False, sendToDisplay)  
                        else:
                            self.subtract(True, sendToDisplay)
                    elif self._deltatime > articulation['staccato']:
                        if not self._temp:
                            self.divide(False, sendToDisplay) 
                        else:
                            self.divide(True, sendToDisplay)                    
                    
                elif note in LambdaMapping.get('multiplication'):
                    print('used via articulation under addition')
                    
                elif note in LambdaMapping.get('division'):
                    print('used via articulation under subtraction')
                                    
                # number comparisons    
                elif note in LambdaMapping.get('equal'):
                    self.equal(sendToDisplay) 
                    
                elif note in LambdaMapping.get('greater'):
                    if self._deltatime <= articulation['staccato']:                                
                        self.greater_than(sendToDisplay) 
                    elif self._deltatime > articulation['staccato']:
                        self.less_than(sendToDisplay)  
                        
                elif note in LambdaMapping.get('less'):
                    print('used via articulation under greater than')                                              

                
    def successor(self, function, sendToDisplay=True):
        """
        builds a successor functions chain.\n
        \n
        :param function function: the function to apply the successor function to
        """
        if sendToDisplay:
            self.mapscheme.formatAndSend(function.__name__, display=1, syntax_color='succ:', spacing=False)
        print(function.__name__)       
                
        def nestFunc(function1):
            if len(self._successorHead) == 0:
                return function(zero)
            else:
                return function(self._successorHead[0])

        self._successorHead.append(nestFunc(function))
                                    
        if len(self._successorHead) > 1:
            self._successorHead = self._successorHead[-1:]
    
    def append_successor(self, function, sendToDisplay=True):
        """
        Append a successor function to the successorHead stack\n
        \n
        :param function function: the function to apply the successor function to
        """
        if sendToDisplay:
            succesors = trampolineRecursiveCounter(function)
            for s in range(succesors):
                self.mapscheme.formatAndSend('successor', display=1, syntax_color='succ:', spacing=False)
        print(function.__name__)       
                
        self._successorHead.append(function)
                                    
        if len(self._successorHead) > 1:
            self._successorHead = self._successorHead[-1:]      
            
    def predecessor(self, function, sendToDisplay=True):
        """
        builds a predecessor functions chain.\n
        \n
        :param function function: the function to apply the predecessor function to
        """
        if sendToDisplay: 
            self.mapscheme.formatAndSend(function.__name__, display=1, syntax_color='pred:', spacing=False)
        print(function.__name__)       
                
        def nestFunc(function1):
            if len(self._numberStack) == 0:
                return function(zero)
            else:
                return function(self._numberStack[0])

        self._numberStack.append(nestFunc(function))
        self._fullStack.append(nestFunc(function))
        if len(self._tempStack) > 0:
            if self._tempStack[0] == '(':
                self._tempStack.append(nestFunc(function))        
                                    
        if len(self._numberStack) > 1:
            if self._numberStack[0].__name__ is 'zero':
                self._numberStack = []
                return zero
            else:
                self._numberStack = self._numberStack[-1:]
                if self._numberStack[0].__name__ is 'succ1':
                    
                    self._evalStack = []
                    self._evalStack.append(trampolineRecursiveCounter(self._numberStack[0]))
                    
                    if (type(self._evalStack[0]) == int):
                        if sendToDisplay:
                            self.mapscheme.formatAndSend(str(self._evalStack[0]), display=3, \
                                                         syntax_color='result:')
                        print(self._evalStack[0])
                        self.mapscheme._osc.send_message("/ck", str(self._evalStack[0]))
                        
                        # Huygens easter eggs
                        self.easterEggs(number=str(self._evalStack[0]), debug=True, sendToDisplay=sendToDisplay)
                        
                    #self.mapscheme.formatAndSend(str(trampolineRecursiveCounter(self._numberStack[0])), display=2, syntax_color='int:')                
                    #print(trampolineRecursiveCounter(self._numberStack[0]))
                else:
                    print('predecessor receives only number expressions!')
                
                                            
    def add(self, temp=False, sendToDisplay=True):
        """
        Append an addition function to the functions stack and any existing number expression\n
        \n
        """
        if sendToDisplay:
            self.mapscheme.formatAndSend('+', display=2, syntax_color='add:', spacing=False)                       
            self.mapscheme.formatAndSend('add', display=1, syntax_color='add:')               
        print('addition')
        
        if not temp:
            if len(self._numberStack) == 0:
                self._functionStack.append(zero)
            else:
                self._functionStack.append(self._numberStack[0])
            #append the operator        
        #self._functionStack.append(self._lambda.add)
            self._functionStack.append(add_trampoline)
        else:
            if len(self._tempNumberStack) == 0:
                self._tempFunctionStack.append(zero)
            else:
                self._tempFunctionStack.append(self._tempNumberStack[0])
            #append the operator        
        #self._functionStack.append(self._lambda.add)
            self._tempFunctionStack.append(add_trampoline)
            
        self._fullStack.append(add_trampoline)
        
        if len(self._tempStack) > 0:
            if self._tempStack[0] == '(':
                self._tempStack.append(add_trampoline)        
        
    def subtract(self, temp=False, sendToDisplay=True):
        """
        Append a subtraction function to the functions stack and any existing number expression\n
        \n
        """
        if sendToDisplay:
            self.mapscheme.formatAndSend('-', display=2, syntax_color='min:',spacing=False)               
            self.mapscheme.formatAndSend('minus', display=1, syntax_color='min:')       
        print('subtraction')
        
        if not temp:
            if len(self._numberStack) == 0:
                self._functionStack.append(zero)
            else:
                self._functionStack.append(self._numberStack[0])
            #append the operator        
            #self._functionStack.append(self._lambda.add)
            self._functionStack.append(subtract) 
        else:
            if len(self._tempNumberStack) == 0:
                self._tempFunctionStack.append(zero)
            else:
                self._tempFunctionStack.append(self._tempNumberStack[0])
            #append the operator        
            #self._functionStack.append(self._lambda.add)
            self._tempFunctionStack.append(subtract)           
            
        
        self._fullStack.append(subtract)
        if len(self._tempStack) > 0:
            if self._tempStack[0] == '(':
                self._tempStack.append(subtract)         


    def equal(self, sendToDisplay=True):
        """
        Compare two number expressions for equality\n
        \n
        """
        if sendToDisplay:
            self.mapscheme.formatAndSend('equal to', display=1, syntax_color='equal:') 
            self.mapscheme.formatAndSend('==', display=2, syntax_color='int:', spacing=False)                       
        
        print('equal to')
        
        if len(self._numberStack) == 0:
            self._functionStack.append(zero)
        else:
            self._functionStack.append(self._numberStack[0])
            #append the operator        
        #self._functionStack.append(self._lambda.add)
        self._functionStack.append(equal)
        self._fullStack.append(equal)
        self.oscName = "ck_equal"
        
        
        
    def greater_than(self, sendToDisplay=True):
        """
        Compare two number expressions for equality\n
        \n
        """
        if sendToDisplay:
            self.mapscheme.formatAndSend('greater than', display=1, syntax_color='gt:') 
            self.mapscheme.formatAndSend('>', display=2, syntax_color='int:', spacing=False)                       
        
        print('greater than')
        if len(self._numberStack) == 0:
            self._functionStack.append(zero)
        else:
            self._functionStack.append(self._numberStack[0])
            #append the operator        
        #self._functionStack.append(self._lambda.add)
        self._functionStack.append(greater) 
        self._fullStack.append(greater)
        self.oscName = "ck_gt"
        
        
    def less_than(self, sendToDisplay=True):
        """
        Compare two number expressions for equality\n
        \n
        """
        if sendToDisplay:
            self.mapscheme.formatAndSend('less than', display=1, syntax_color='lt:')  
            self.mapscheme.formatAndSend('<', display=2, syntax_color='int:', spacing=False)                       
        print('less than')
        if len(self._numberStack) == 0:
            self._functionStack.append(zero)
        else:
            self._functionStack.append(self._numberStack[0])
            #append the operator        
        #self._functionStack.append(self._lambda.add)
        self._functionStack.append(less)  
        self._fullStack.append(less)
        self.oscName = "ck_lt"
        
    ##stack and evaluation
    def evaluateFunctionStack(self, stack, temp=False, sendToDisplay=True):
        """Evaluate a function with 2 arguments.\n
        \n
        :param function function: the function to evaluate with the given args
        :param function args: the function arguments to pass
        """
        if sendToDisplay:
            self.mapscheme.formatAndSend('apply functions', display=1, syntax_color='eval:')       
            self.mapscheme.newLine(display=1)       
        
        def evaluate2args(function, *args):
            """Evaluate a function with 2 arguments.\n
            \n
            :param function function: the function to evaluate with the given args
            :param function args: the function arguments to pass
            """
            return function(args[0], args[1])
        
        if type(stack) is not list:
            print('This function expects a List/Stack')
        else:
            # append the 2nd number
            if len(stack) == 0:
                print('not enough elements in stack to apply the function')
            elif len(stack) == 2:
                if not temp:
                    if len(self._numberStack) > 0:
                        self._functionStack.append(self._numberStack[0])             
                else:
                    self._tempFunctionStack.append(self._tempNumberStack[0])
            
            if len(stack) == 3:
                self._numberStack = [] 
                self._tempNumberStack = []
                if not temp:
                    self.mapscheme.newLine(display=2)
                    self.mapscheme.newLine(display=2)                    
                    self._numberStack.append(evaluate2args(self._functionStack[1], \
                                                           self._functionStack[0], \
                                                           self._functionStack[2]))             
                else:
                    #self._numberStack.append(evaluate2args(self._tempFunctionStack[1], \
                                                           #self._tempFunctionStack[0], \
                                                           #self._tempFunctionStack[2])) 
                    self._tempNumberStack.append(evaluate2args(self._tempFunctionStack[1], \
                                                           self._tempFunctionStack[0], \
                                                           self._tempFunctionStack[2])) 
                    
                #print('TEMP NUM STACK: ', self._tempNumberStack)
                #print('NORM STACK: ', self._numberStack)
                     
    
    def evaluateTempStack(self, stack):
        """Evaluate the functions within parenthesis.
        \n
        :param list stack: a list containing the functions to be evaluated
        """        
        if stack[0] == '(':
            return False
    
    def evalPostfix(self, stack):
        """
        evaluate the stack postfix style
        """
        
    
    def multiply(self, temp=False, sendToDisplay=True):
        """Append an addition function to the functions stack and any existing number expression\n
        \n
        """
        if sendToDisplay:
            self.mapscheme.formatAndSend('*', display=2, syntax_color='mul:', spacing=False)                        
            self.mapscheme.formatAndSend('multiply', display=1, syntax_color='mul:')       
        print('multiplication')
        
        if not temp:
            if len(self._numberStack) == 0:
                self._functionStack.append(zero)
            else:
                self._functionStack.append(self._numberStack[0])
                #append the operator        
                self._functionStack.append(mult_trampoline)
                        
        else:
            if len(self._tempNumberStack) == 0:
                self._tempFunctionStack.append(zero)
            else:
                self._tempFunctionStack.append(self._tempNumberStack[0])
                #append the operator        
                self._tempFunctionStack.append(mult_trampoline)            
            
        self._fullStack.append(mult_trampoline)
        
        if len(self._tempStack) > 0:        
            if self._tempStack[0] == '(':
                self._tempStack.append(mult_trampoline)         
            
        
    def divide(self, temp=False, sendToDisplay=True):
        """
        Append an addition function to the functions stack and any existing number expression\n
        \n
        """
        if sendToDisplay:
            self.mapscheme.formatAndSend('/', display=2, syntax_color='div:', spacing=False)                
            self.mapscheme.formatAndSend('divide', display=1, syntax_color='div:')        
        print('division')
        
        if not temp:
            if len(self._numberStack) == 0:
                self._functionStack.append(zero)
            else:
                self._functionStack.append(self._numberStack[0])
            #append the operator        
            self._functionStack.append(divide)

        else:
            if len(self._tempNumberStack) == 0:
                self._tempFunctionStack.append(zero)
            else:
                self._tempFunctionStack.append(self._tempNumberStack[0])
            #append the operator        
            self._tempFunctionStack.append(divide)            

        self._fullStack.append(divide)
        if len(self._tempStack) > 0:        
            if self._tempStack[0] == '(':
                self._tempStack.append(divide)         
        
                     
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


    def wrong_note(self, note, debug=False, configfile='default_setup.ini'):
        """
        calculate the wrong notes based on the semi-tone tolerance 
        :param int note: the midinote coming in
        """
        config = configparser.ConfigParser(delimiters=(':'), comment_prefixes=('#'))
        config.read(configfile, encoding='utf8')
        
        tolerance = config['ckalculator'].getint('wrong_note_tolerance')      
        
        wrong_notes = list(map(lambda x: [x-tolerance, x+tolerance], self._notesList))
        wrong_notes = list(np.array(wrong_notes).flat)
        
        if note in wrong_notes:
            if debug:
                print('wrong note! -> played', note)
            return True
        else:
            return False
        
    def find_ostinato(self, array, size=4, repetitions=5, debug=False):
        """
        find ostinatos in the MIDI in stream
        param array array: The array of MIDI notes to analyze for ostinato presence
        param int size: the amount of notes that conforms the ostinato
        param int repetitions: the amount of repetitions of notes to conform an ostinato
        param boolean debug: print debugging messages
        """
        length = size*repetitions+size
        if not self._developedOstinato and len(self._fullMemory) > length: #full_mem needed or better to only use _note_on_cue?
            self._fullMemory = self._fullMemory[-length:]
            self._note_on_cue = self._note_on_cue[-length:]
            self._filtered_cue = self._filtered_cue[-length:]
            
            notes, index, reverse, counts = np.unique(self._fullMemory, True, True, True)
            #cue_notes, cue_reverse = np.unique(self._note_on_cue, False, True, False)
            
            if debug:                        
                print('memory:', self._fullMemory, '\nnote_on cue:', self._note_on_cue)
                print('notes:', notes, '\ncounts:', counts, '\nreverse:', reverse)
                
            #self.get_ostinato_pattern(cue_reverse, size, True)
                
            i = np.where(counts > 3)

            #print('i:', i)
            
            if i[0].shape[0] > 3:
                # np_notes = notes[i] ### this is shorthand for what happend later ?
                for x in self._note_on_cue:
                    if x in notes[i]:
                        self._filtered_cue.append(x)
                
                cue_notes, cue_reverse = np.unique(self._filtered_cue, False, True, False)
                pattern_match = self.get_ostinato_pattern(cue_reverse, size, False)                        
                
                if debug:
                    print('cue notes:', cue_notes, '\ncue_reverse:', cue_reverse)

                if pattern_match:
                    for item in i[0]:
                        if not self._foundOstinato:
                            self.ostinato['first'].append(notes[item])
                            
                            if len(self.ostinato['first']) > 1:
                                np_notes = np.array(self.ostinato['first'])
                                
                            if len(self.ostinato['first']) > 3:
                                # get uniquness! (i.e. [49, 95, 49, 95]) and 8ve range
                                self.ostinato['first'] = self.ostinato['first'][-4:]
                                
                                if np_notes.max() - np_notes.min() <= 12: #within an 8ve range
                                    self._foundOstinato = True #pause listening to analyze the frame
                                    self._fullMemory = []
                                    self._note_on_cue = []
                                    if debug:
                                        print('i -> ', i)
                                    print('found ostinato!', midiToNotes(self.ostinato['first']))
                                    msg_notes = (',').join(midiToNotes(self.ostinato['first']))
                                    self.mapscheme.formatAndSend('found ostinato ' + msg_notes, 
                                                                 display=4, syntax_color='function:')
                                else:
                                    self._foundOstinato = False
                        else:
                            self.ostinato['compare'].append(notes[item])
                            
                            #if len(self.ostinato['compare']) > 1:
                                #np_notes = np.array(self.ostinato['compare'])
                                
                            if len(self.ostinato['compare']) > 3:
                                # get uniquness! (i.e. [49, 95, 49, 95]) and 8ve range
                                self.ostinato['compare'] = self.ostinato['compare'][-4:]
                                np_notes = np.array(self.ostinato['compare'])
                                
                                print('compare: ', midiToNotes(self.ostinato['compare']))
                                
                                if np_notes.max() - np_notes.min() <= 12: #within an 8ve range
                                    self.compare_ostinato(self.ostinato['first'], self.ostinato['compare'],
                                                          debug=True)
                                                                                   
                        
    def get_ostinato_pattern(self, noteson_array, ostinato_size, debug=False):
        """
        Compare the pattern of notes in the note_on cue. In order to see if it is
        a repeated pattern and thus an ostinato.
        param array noteson_array: the notes cue
        param int ostinato_size: number of notes conforming the ostinato
        Returns True or False 
        """
        noteson_array = noteson_array[-12:] #correct it
        if len(noteson_array) == 12:
            pattern1 = noteson_array[0:ostinato_size]
            pattern2 = noteson_array[4:ostinato_size*2]
            pattern3 = noteson_array[8:ostinato_size*3]
            #pattern4 = noteson_array[12:ostinato_size*4]
        
            pattern_stack = np.vstack([pattern1, pattern2, pattern3])
              
            pattern_check = (np.diff(pattern_stack.reshape(len(pattern_stack),-1), axis=0)==0).all()
        
            if debug:
                if pattern_check:
                    print(pattern1,'\n',pattern2,'\n',pattern3,'\n')
                    print(pattern_check)       
        
            return pattern_check
                       
    def compare_ostinato(self, ostinato1, ostinato2, debug=False):
        """
        Detect deviations of an ostinato.
        param array ostinato: the base ostinato
        param int note: the ostinato to compare
        """
        if np.array_equal(ostinato1, ostinato2):
            self.ostinato = {'first': [], 'compare': []}
            if debug:
                print('ostinato did not change')
                self.mapscheme.formatAndSend('ostinato did not change', display=4, syntax_color='function:')
        else:
            diff = np.subtract(ostinato1, ostinato2)
            
            if np.array_equal(sorted(np.abs(diff)), [0,0,0,1]):
                self._developedOstinato = True
                
                if debug:
                    print('ostinato has 1 note difference! Well done 👸🏼-> ', diff)
                self.mapscheme.formatAndSend('ostinato has 1 note difference! Well done', display=4,
                                                 syntax_color='function:')
            else:
                print('😤 ostinato was not developed correctly. Please try again')
                self._developedOstinato = False
                self.ostinato = {'first': [], 'compare': []}
                
                self.mapscheme.formatAndSend('ostinato was not developed correctly. Please try again', display=4,
                                             syntax_color='function:')
        # clean ostinato memory
        self._foundOstinato = False
        self._fullMemory = []
        self._note_on_cue = []
        self._filtered_cue = []
        #self.ostinato = {'first': [], 'compare': []}

        print('first:', midiToNotes(ostinato1),
              'compare:', midiToNotes(ostinato2))      
       
    def define_function_body(self, note, articulation, debug=True):
        """
        High level function to choose a lambda function to be used as part of the function body 
        of a function definition.
      
        :param int note: incoming MIDI note
        :param list articulation: array containg the threshold in deltatime values for articulation (i.e. staccato, sostenuto, etc.)
        """ 
        if len(self._functionBody) == 0:
            if note in LambdaMapping.get('successor'):
    
                if self._deltatime <= articulation['staccato']:
                    self._functionBody['arg1'] = 'successor'
                
                elif self._deltatime > articulation['staccato']: #this is either the func 'zero' or 'predecessor'
                    
                    if note in [LambdaMapping.get('successor')[0]]:
                        self._functionBody['arg1'] = 'predecessor'
                            
            elif note in LambdaMapping.get('zero'):
                self._functionBody['arg1'] = 'zero'
               
            elif note in LambdaMapping.get('eval'): # if chord (> 0.02) and which notes? 
                self._functionBody['arg1'] = 'eval'
                
            elif note in LambdaMapping.get('predecessor'):
                self._functionBody['arg1'] = 'predecessor'
                
            elif note in LambdaMapping.get('addition'):
                if self._deltatime <= articulation['staccato']:
                    self._functionBody['arg1'] = 'add'
                    
                elif self._deltatime > articulation['staccato']:
                    self._functionBody['arg1'] = 'multiply'
                    
            elif note in LambdaMapping.get('subtraction'):
                if self._deltatime <= articulation['staccato']:                
                    self._functionBody['arg1'] = 'subtract'
                    
                elif self._deltatime > articulation['staccato']:
                    self._functionBody['arg1'] = 'divide'
                    
            # number comparisons    
            elif note in LambdaMapping.get('equal'):
                self._functionBody['arg1'] = 'equal'
                
            elif note in LambdaMapping.get('greater'):
                if self._deltatime <= articulation['staccato']:
                    self._functionBody['arg1'] = 'greater'
                elif self._deltatime > articulation['staccato']:
                    self._functionBody['arg1'] = 'less'                
                    
        elif len(self._functionBody) == 1:
            if debug:
                print('function body arg 1 is: ', self._functionBody['arg1'])
            if self._arg1Counter == 0:
                self.mapscheme.formatAndSend('function body arg 1 is:' + self._functionBody['arg1'], display=4,
                                             syntax_color='function:')
            self._arg1Counter += 1
                
        elif len(self._functionBody) == 2:
            if debug:
                print('function body arg 2 is: ', self._functionBody['arg2'])
            if self.arg2Counter == 0:
                self.mapscheme.formatAndSend('function body arg 2 is:' + self._functionBody['arg2'], display=4,
                                             syntax_color='function:')
            self._arg2Counter += 1

            
    def storeFunction(self, funcfile='ck_functions.ini', debug=True, sendToDisplay=True):
        """
        Store the defined function in a .ini file for future use.
        """
        ck_functions = configparser.ConfigParser(delimiters=(':'), comment_prefixes=('#'))
        ck_functions.read(funcfile, encoding='utf8')
        existingfuncs = []
        
        for f in self.ckFunc():
            existingfuncs.append(f['name'])
            
        print(existingfuncs)   
        
        func_num = len(ck_functions['functions'])

        name = 'function' + repr(func_num+1) + ': '
        name2 = 'function' + repr(func_num+2) + ': '
        chord = ','.join(map(str, self.ostinato['first']))
        chord2 = ','.join(map(str, self.ostinato['compare']))
        body = chord + ' -> (' + self._functionBody['arg1'] + ' ' + repr(self._functionBody['arg2']) + ' x)\n'
        body2 = chord2 + ' -> (' + self._functionBody['arg1'] + ' ' + repr(self._functionBody['arg2']) + ' x)\n'
        
        with open(funcfile, 'a') as file:
            if self.ostinato['first'] not in existingfuncs:
                file.write(name + body)
                print('function saved 1', midiToNotes(self.ostinato['first']))
            else:
                print('chord is assigned already. cannot overwrite')
                
            if self.ostinato['compare'] not in existingfuncs:
                file.write(name2 + body2)
                print('function saved 2', midiToNotes(self.ostinato['compare']))
            else:
                print('chord is assigned already. cannot overwrite')
                
            file.close()
            
        if sendToDisplay:
            total = len(self.ckFunc())
            count = 0
            for f in self.ckFunc():
                count += 1
                function_print = (',').join(midiToNotes(f['name'])) + ' -> (' + f['body']['func'] + ' ' + \
                f['body']['arg1str'] + ' ' + f['body']['var'] + ')'
                if count == total:
                    self.mapscheme.formatAndSend(function_print, display=4, syntax_color='function:')
                else:
                    self.mapscheme.formatAndSend(function_print, display=4, syntax_color='saved:')
            
        #reset the ostinato analysis
        self.ostinato = {'first': [], 'compare': []}
        self._fullMemory = []
        self._note_on_cue = []
        self._filtered_cue = []
        self._functionBody = {}
        self._defineCounter = 0
        self._foundOstinato = False
        self._developedOstinato = False 
                
    def shift_mapping(self, offset, shift_type='semitone', configfile='default_setup.ini', sendToDisplay=True):
        """
        shift the mapping structure every time a note not belonging to the original mapping is played
        :param int offset: the offset in semitones
        :param str shift_type: the type of shifting to perform. options are now 'semitone' or 'octave shift'
        """
        config = configparser.ConfigParser(delimiters=(':'), comment_prefixes=('#'))
        config.read(configfile, encoding='utf8')
        
        shift_on = config['ckalculator'].get('shift')
        
        if shift_on == 'on':
            mappings = list(LambdaMapping.items())
            self._notesList = []
                    
            if shift_type == 'random':           
                shift_type = random.choice(['octave shift', 'semitone shift'])
                print(shift_type)
                if sendToDisplay:
                    self.mapscheme.formatAndSend('Wrong note!\n'+shift_type, display=3, syntax_color='error:')
            
            if shift_type == 'semitone shift':
                for mapping in mappings:
                    LambdaMapping[mapping[0]] = list(map(lambda x: 
                                                         self._pianoRange[(x + offset) % len(
                                                             self._pianoRange) - 21], #compensate for lower note being 21 not 0
                                                         mapping[1]))
            elif shift_type == 'octave shift':
                print('octave shift triggered')
                for mapping in mappings:
                    LambdaMapping[mapping[0]] = list(map(lambda x: 
                                                         self._pianoRange[(x + 12) % len(
                                                             self._pianoRange) - 21],
                                                         mapping[1]))
            
            for item in list(LambdaMapping.values()):
                for sub_item in item:
                    if sub_item > 0:
                        self._notesList.append(sub_item)        
    
            #print('new mapping', LambdaMapping)
            note_names = {24:"C",25:"C#",26:"D",27:"D#",28:"E",29:"F",30:"F#",31:"G",32:"G#",33:"A",34:"A#",35:"B"}
            if sendToDisplay:
                self.mapscheme.formatAndSend('eval mapped to ' +
                                             note_names.get((LambdaMapping.get('eval')[0]%len(note_names))+24) + ' (' +
                                             str(LambdaMapping.get('eval')[0]) + ')', display=3,
                                             syntax_color='e_debug:');
            #print('new valid notes', self._notesList)
        
    def zeroPlusRec(self, sendToDisplay=True, sendToStack=False):
        if len(self._successorHead) > 0:
            num = trampolineRecursiveCounter(self._successorHead[0])
            print('succ head: ', num)
            
            if len(self._functionBody) > 0:
                self._numForFunctionBody = num 
                
            if self._temp is False:
                self._numberStack = []                                
                #print result:
                if sendToDisplay or sendToStack:
                    self.mapscheme.formatAndSend('zero', display=1, syntax_color='zero:')  
                    #self.mapscheme.newLine(display=1)
                    self.mapscheme.formatAndSend(str(trampolineRecursiveCounter(self._successorHead[0])), \
                                                 display=2, syntax_color='int:', spacing=False)

                self._numberStack.append(self._successorHead[0])
                self._fullStack.append(self._successorHead[0])
                                                
            
            else:
                if sendToDisplay:
                    self.mapscheme.formatAndSend('zero', display=1, syntax_color='zero:')  
                    #self.mapscheme.newLine(display=1)
                
                if len(self._tempStack) > 0:
                    self._tempNumberStack = []                                                                            
                    if self._tempStack[0] == '(':
                        self._tempNumberStack.append(self._successorHead[0])
                        if sendToDisplay or sendToStack:
                            self.mapscheme.formatAndSend(str(trampolineRecursiveCounter(self._tempNumberStack[0])), \
                                                         display=2, syntax_color='int:', spacing=False)                                        
                        
                        if len(self._tempFunctionStack) > 0:
                            self.evaluateFunctionStack(self._tempFunctionStack, sendToDisplay=sendToDisplay)                        
                            if (self._tempNumberStack[0].__name__ is 'succ1'):
                                self._evalStack = []
                                self._evalStack.append(trampolineRecursiveCounter(self._tempNumberStack[0]))
                                if sendToDisplay:
                                    self.mapscheme.formatAndSend(str(self._evalStack[0]), display=3, \
                                                                 syntax_color='result:')                                
                                print(self._evalStack[0])                        
                                self._tempFunctionStack = []     
                                
    def easterEggs(self, configfile='default_setup.ini', number=100, debug=False, special_num=7,sendToDisplay=True):
        """
        Attach certain events to specific numbers. Easter egg style.
        
        :param string number: the number-key to grab the value from the config file
        """
        config = configparser.ConfigParser(delimiters=(':'), comment_prefixes=('#'))
        config.read(configfile, encoding='utf8')
        
        if int(number)%special_num is 0: #for huygens its 42
            number = str(special_num)

        if number in config['easter eggs']:
            if debug:
                print('EASTER EGG FOUND: ', config['easter eggs'].get(number))

            if sendToDisplay:
                self.mapscheme._osc.send_message("/ck_easteregg", config['easter eggs'].get(number))    
                self.mapscheme.formatAndSend(config['easter eggs'].get(number), syntax_color='r_debug:', display=3)

    
    def ckFunc(self, funcfile='ck_functions.ini', debug=False):
        """
        Load and parse a CK custom function
        """

        funcs = configparser.ConfigParser(delimiters=(':'), comment_prefixes=('#'))
        funcs.read(funcfile, encoding='utf8')
        functions = []
        
        for function in funcs['functions']:
            functions.append(parseCKfunc(funcs['functions'].get(function), function))
        
        if debug:
            print(functions)
        
        return functions
                   
    #def dumpCkfunctions(self, funcfile='ck_functions.ini', debug=False):
        #"""
        #Dump existing CK custom functions
        #"""

        #funcs = configparser.ConfigParser(delimiters=(':'), comment_prefixes=('#'))
        #funcs.read(funcfile, encoding='utf8') 
        #functions = []
        
        #for function in funcs['functions']:
            #functions.append(funcs['functions'].get(function))
            
        #return functions
        
                  
class CK_lambda(object):
    """CK_lambda Class
    *DEPRECATEDE CLASS* 
    The main class containing basic Lambda calculus expressions
    """    
    
    def __init__(self, debug=False):
        self._debug = debug
    
    def zero(self, body=''):
        """
        lambda identity function. Also represents 0 (zero)\n
        returns the function/argument it was applied to\n
        (in lambda notation: λx.x)\n
        \n
        :param function body: body variable to replace with the application argument\n
        """
        return body
    
    def true(self, function1):
        """
        lambda select first function. Also represents TRUE\n
        returns the first variable (function1)\n 
        (in lambda notation: λx.λy.x)\n
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
        (in lambda notation: λx.λy.y)\n
        \n
        :param function function1: expression that will be discarded/destroyed\n
        :param function function2: expression that will be returned\n
        """ 
        def select_second(function2):
            return function2
        
        return select_second
    
    def iszero(self, number_expression):
        """
        lambda function to return true (select_first) if the number expression is zero (i.e. identity func)\n
        otherwise returns false (selet_second)\n
        [in lambda notation: λn.(n true) ]\n
        \n
        :param function number_expression: a funtional representation of an integer (with successor function)
        """
        
        return number_expression(self.true)
    
    
    def simpleReduce(self, *functions):
        """
        lambda function to apply selector functions.\n
        \n
        :param function function1: the function to apply to the next functions in *functions\n
        :param function *functions: the function(s) to treat as argument(s) for the application\n 
        \n\n
        TODO: Make a simpleApply function 
        """
        
        functions_array = []
                
        for f in functions:
            if callable(f):
                functions_array.append(f)
                
        if len(functions_array) < len(functions):
            print('not all arguments are functions!')
            return
        
        if self._debug:        
            print('array of functions length: ', len(functions_array))

        if len(functions_array) > 1:
            # TODO: think if this can be done recursively
            if len(functions_array) == 2:
                return functions_array[0](functions_array[1])
            elif len(functions_array) == 3:
                return functions_array[0](functions_array[1])(functions_array[2])
            elif len(functions_array) == 4:
                return functions_array[0](functions_array[1])(functions_array[2])\
                    (functions_array[3])
            elif len(functions_array) == 5:
                return functions_array[0](functions_array[1])(functions_array[2])\
                    (functions_array[3])(functions_array[4])
            
    
    def successor(self, number):
        """
        lambda successor function. Returns a pair function with FALSE as first
        argument and the original number (function expression) as second argument.\n
        [in lambda notation: λn.λs.((s false) n) ]\n
        
        :param function number: zero or successors of zero as integer representations  
        """
        
        def succ1(successor):
            """
            :param function successor: a bound variable to be replaced by the argument after final application (i.e. select_first)
                    
            """
            return successor(self.false)(number)
        
        return succ1
    
    
    def predecessor(self, number):
        """
        lambda predecessor function. Returns a function which returns zero if number argument is zero otherwise\n 
        reduces the number expression argument by one level\n
        [in lambda notation: λn.(((iszero n) zero)(n false)) ]\n
        
        :param function number: zero or successors of zero as integer representations
        \n
        \nNOTE: The function stops at zero. It doesn't return -1 when applied to zero!
        """
        
        if type(number) is not tuple:
            if self.iszero(number).__name__ is 'true':
                return self.zero
            else:
                return number(self.false)
        else:
            if number[0].__name__ is 'mult_trampoline':
                return number[1][1](self.false)
                
    def recursiveCounter(self, successor_expression, counter=0):
        """
        function to count how many times successor functions are nested until the zero is reached. Returns the count as int.
        
        :param function successor_expression: the nested successor functions to be reduced until zero\n
        :param int counter: the integer to increment on each recursion\n
        :param boolean debug: wheather to print debg messages or not
        """
                   
        def sum_one(num):
            """
            add 1 to the counter.\n
            \n
            :param integer counter: the number to add 1 to
            """
            if type(num) is int:
                return num + 1
        
        def countreduce(reducedfunc):
            """
            applies the successor function to select_second recursively\n
            \n
            :param function reducedfunc: the function to reduce
            """
            #nonlocal reduced # this is really functional now            
            return reducedfunc(self.false)              
        
        if successor_expression.__name__ is 'succ1':
            #recursion point 1
            return self.recursiveCounter(countreduce(successor_expression),
                                         sum_one(counter))
        
        elif successor_expression.__name__ is 'zero':
            if self._debug:
                print(counter)
            return counter
                       
        else:
            if successor_expression.__name__ is 'successor':
                print('missing a zero to close the successor chain!')
            else:
                print('this function can only process number expression functions as argument!')
                
    def trampolineRecursiveCounter(self, successor_expression, counter=0):
        """
        function to count how many times successor functions are nested until the zero is reached. Returns the count as int.
        
        :param function successor_expression: the nested successor functions to be reduced until zero\n
        :param int counter: the integer to increment on each recursion\n
        :param boolean debug: wheather to print debg messages or not
        """         
        
        if type(successor_expression) is tuple:
            expression = successor_expression[1]            
        else:
            expression = successor_expression
        
        if expression.__name__ is 'succ1' or expression.__name__ is 'mult_add':
            #recursion point 1
            return self.callTrampoline(self.trampolineRecursiveCounter)(expression(self.false),
                                         counter + 1)
        
        elif expression.__name__ is 'zero':
            if self._debug:
                print(counter)
            return self.stopTrampoline(counter)
                       
        else:
            if expression.__name__ is 'successor':
                print('missing a zero to close the successor chain!')
            else:
                print('this function can only process number expression functions as argument!', expression)    
                
    def add(self, x, y):
        """
        function to get the result of the addition of two number expressions.\n
        Returns the resulting representation of an integer\n
        \n
        :param function x: functional representation of an integer [i.e. successor(successor(zero)) ]
        :param function y: functional representation of an integer
        """
        
        if self.iszero(y).__name__ is 'true':
            return x
        else:
            return self.add(self.successor(x), self.predecessor(y))
    
    
    def add_trampoline(self, x, y):
        """
        function to get the result of the addition of two number expressions.\n
        Returns the resulting representation of an integer\n
        \n
        :param function x: functional representation of an integer [i.e. successor(successor(zero)) ]
        :param function y: functional representation of an integer
        """   
        
        if self.iszero(y).__name__ is 'true':
            return self.stopTrampoline(x)
        else:
            return self.callTrampoline(self.add_trampoline)(self.successor(
                x), self.predecessor(y))
            
    def mult(self, x, y):
        """
        function to get the result of the multiplication of two number expressions.\n
        Returns the resulting representation of an integer\n
        \n
        :param function x: functional representation of an integer [i.e. successor(successor(zero)) ]
        :param function y: functional representation of an integer
        """
        
        if self.iszero(y).__name__ is 'true':
            return self.zero
        else:
            return self.add(x, self.mult(x, self.predecessor(y)))
    
    def mult_trampoline(self, x, y):
        """
        function to get the result of the multiplication of two number expressions.\n
        Returns the resulting representation of an integer\n
        \n
        :param function x: functional representation of an integer [i.e. successor(successor(zero)) ]
        :param function y: functional representation of an integer
        """
                   
        if type(y) is not tuple and self.iszero(y).__name__ is 'true':
            return self.stopTrampoline(self.zero)
        else:
            #return self.add(x, self.mult(x, self.predecessor(y)))
            def mult_add(y):
                return self.callTrampoline(self.mult_trampoline)(x,
                                                                 self.predecessor(y))
        
            return self.callTrampoline(self.add_trampoline)(x, mult_add)
                       
    def test_func(*args):
        return "narcode"

    # solutions for stack overflow due to recursive limit
    def callTrampoline(self, f):
        """
        encode instructions for trampoline function 
        """
        def g(*args, **kwds):
            return f, args, kwds
        
        return g
    
    def stopTrampoline(self, value):
        """return a triple to stop the trampoline iteration
        """
        return None, value, None
    
    def with_trampoline(self, f):
        """
        wrap a trampoline around a recursive function
        """
        
        @functools.wraps(f)
        def g(*args, **kwds):
            h = f
            # the trampoline
            while h is not None:
                h, args, kwds = h(*args, **kwds)

            return args

        return g 

