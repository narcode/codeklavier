#!/usr/bin/env python3

import functools
import array
from inspect import signature
import random
#from pyparsing import Literal,CaselessLiteral,Word,Combine,Group,Optional,\
    #ZeroOrMore,Forward,nums,alphas
#import operator
from Motifs import motifs_lambda as LambdaMapping
from Mapping import Mapping_Ckalculator
from CK_lambda import *

class Ckalculator(object):
    """Ckalculator Class
    
    The main class behind the Ckalculator prototype. Lambda calculus with the piano (simple arithmetic operations)
    TODO: _fullStack is not used yet but added for the future. Evaluate the decision and either implement or deprecate
    """
    
    def __init__(self, noteonid, noteoffid, pedal_id):
        """The method to initialise the class and prepare the class variables.
        """
        
        self.mapscheme = Mapping_Ckalculator(True, False)
        self.note_on = noteonid
        self.note_off = noteoffid
        self.pedal = pedal_id
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
        
        # fill/define the piano range:
        self._pianoRange = array.array('i', (i for i in range (21, 109)))

        # get all "meaningful" mapping notes:
        for item in list(LambdaMapping.values()):
            for sub_item in item:
                if sub_item > 0:
                    self._notesList.append(sub_item)
        print('valid notes:', self._notesList)
        

        
    def parse_midi(self, event, section, ck_deltatime_per_note=0, ck_deltatime=0, articulaton={'staccato': 0.1, 'sostenuto': 0.8, 'chord': 0.02}):
        """Parse the midi signal and process it depending on the register.

        :param tuple event: describes the midi event that was received
        :param string section: the MIDI piano range (i.e. low register, mid or high)
        :param float ck_deltatime_per_note: the deltatime between incoming note-on MIDI messages
        :param int target: target the parsing for a specific snippet. 0 is no target
        :param list articulation: array containg the threshold in deltatime values for articulation (i.e. staccato, sostenuto, etc.)
        """   
        
        message, deltatime = event

        if (message[0] == self.pedal):
            if message[2] == 127:
                print('(')
                self.mapscheme.formatAndSend('(', display=2, syntax_color='int:', spacing=False)
                self._fullStack.append('(')
                self._tempStack = []
                self._tempStack.append('(')                
                self._temp = True
            elif message[2] == 0 and '(' in self._fullStack: #could also be: and self._temp = True
                print(')')
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
            
        #if message[0] == self.note_on:
            #print('ON delta:', ck_deltatime)

        if message[0] == self.note_off or (message[0] == self.note_on and message[2] == 0):
            note = message[1]
            self._deltatime = ck_deltatime_per_note 
            #print('Articulation delta: ', ck_deltatime_per_note)
            
            if note not in self._notesList:
                print('...', '\nwrong note', '...', 'shifting', '\n...')
                #self._nonMappedNoteCounter += 1
                #print(self._nonMappedNoteCounter)
                self.shift_mapping(1, 'random')
            else:
            ### lambda calculus ###
                if note in LambdaMapping.get('successor'):
                    
                    if self._deltatime <= articulaton['staccato']:
                        self.build_succesor(successor)
                    
                    elif self._deltatime > articulaton['staccato']: #this is either the func 'zero' or 'predecessor'
                        
                        if note in [LambdaMapping.get('successor')[0]]:
                            if len(self._numberStack) == 0:
                                self.build_predecessor(zero) # what kind of result is better?
                            else:
                                self.build_predecessor(predecessor)
                                
                        else: #zero + recursive counter:
                            self.zeroPlusRec()                                  
                                
                        self._successorHead = []
                        
                elif note in LambdaMapping.get('zero'):
                    print('identity')
                    self.zeroPlusRec()
                    self._successorHead = []
                                                                            
                elif note in LambdaMapping.get('eval'): # if chord (> 0.02) and which notes? 
                    print('evaluate!')
                    self.mapscheme.newLine(display=1)
                    if len(self._functionStack) > 0 and len(self._numberStack) > 0:
                        self.evaluateFunctionStack(self._functionStack)
                        if (self._numberStack[0].__name__ is 'succ1'):
                            self._evalStack = []
                            self._evalStack.append(trampolineRecursiveCounter(self._numberStack[0]))
                            if (type(self._evalStack[0]) == int):
                                self.mapscheme.formatAndSend(str(self._evalStack[0]), display=3, \
                                                             syntax_color='result:')
                                print(self._evalStack[0])
                                self.mapscheme._osc.send_message("/ck", str(self._evalStack[0]))
                            else: 
                                self.mapscheme.formatAndSend('error', display=3, syntax_color='error:')
                                self.mapscheme.formatAndSend('result is not a number', display=3, syntax_color='e_debug:')
                                self.mapscheme._osc.send_message("/ck_error", str(self._evalStack[0]))
                                
                                
                        
                        else:
                            #print(self.oscName)
                            self.mapscheme.formatAndSend(self._numberStack[0].__name__, display=3, \
                                                         syntax_color='result:')
                            self.mapscheme._osc.send_message("/"+self.oscName, self._numberStack[0].__name__)
                            
                        self._functionStack = []
                    
                elif note in LambdaMapping.get('predecessor'):
                    print('used via articulation under 1 succesor')
                        
                elif note in LambdaMapping.get('addition'):
                    if self._deltatime <= articulaton['staccato']:
                        if not self._temp:
                            self.add()
                        else:
                            self.add(temp=True)
                    elif self._deltatime > articulaton['staccato']:
                        if not self._temp:
                            self.multiply() 
                        else:
                            self.multiply(True)                    
                    
                elif note in LambdaMapping.get('substraction'):
                    if self._deltatime <= articulaton['staccato']:                
                        if not self._temp:
                            self.substract()  
                        else:
                            self.substract(True)
                    elif self._deltatime > articulaton['staccato']:
                        if not self._temp:
                            self.divide() 
                        else:
                            self.divide(True)                    
                    
                elif note in LambdaMapping.get('multiplication'):
                    print('used via articulation under addition')
                    
                elif note in LambdaMapping.get('division'):
                    print('used via articulation under substraction')
                                    
                # number comparisons    
                elif note in LambdaMapping.get('equal'):
                    self.equal() 
                    
                elif note in LambdaMapping.get('greater'):
                    if self._deltatime <= articulaton['staccato']:                                
                        self.greater_than() 
                    elif self._deltatime > articulaton['staccato']:
                        self.less_than()  
                        
                elif note in LambdaMapping.get('less'):
                    print('used via articulation under greater than')                                              

                
    def build_succesor(self, function):
        """
        builds a successor functions chain.\n
        \n
        :param function function: the function to apply the successor function to
        """
        
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
            
    def build_predecessor(self, function):
        """
        builds a predecessor functions chain.\n
        \n
        :param function function: the function to apply the predecessor function to
        """

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
                    self.mapscheme.formatAndSend(str(trampolineRecursiveCounter(self._numberStack[0])), display=2, syntax_color='int:')                
                    print(trampolineRecursiveCounter(self._numberStack[0]))
                else:
                    print('predecessor receives only number expressions!')
                
                                            
    def add(self, temp=False):
        """
        Append an addition function to the functions stack and any existing number expression\n
        \n
        """
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
        
    def substract(self, temp=False):
        """
        Append a substraction function to the functions stack and any existing number expression\n
        \n
        """
        self.mapscheme.formatAndSend('-', display=2, syntax_color='min:',spacing=False)               
        self.mapscheme.formatAndSend('minus', display=1, syntax_color='min:')       
        print('substraction')
        
        if not temp:
            if len(self._numberStack) == 0:
                self._functionStack.append(zero)
            else:
                self._functionStack.append(self._numberStack[0])
            #append the operator        
            #self._functionStack.append(self._lambda.add)
            self._functionStack.append(substract) 
        else:
            if len(self._tempNumberStack) == 0:
                self._tempFunctionStack.append(zero)
            else:
                self._tempFunctionStack.append(self._tempNumberStack[0])
            #append the operator        
            #self._functionStack.append(self._lambda.add)
            self._tempFunctionStack.append(substract)           
            
        
        self._fullStack.append(substract)
        if len(self._tempStack) > 0:
            if self._tempStack[0] == '(':
                self._tempStack.append(substract)         


    def equal(self):
        """
        Compare two number expressions for equality\n
        \n
        """
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
        
        
        
    def greater_than(self):
        """
        Compare two number expressions for equality\n
        \n
        """
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
        
        
    def less_than(self):
        """
        Compare two number expressions for equality\n
        \n
        """
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
    def evaluateFunctionStack(self, stack, temp=False):
        """Evaluate a function with 2 arguments.\n
        \n
        :param function function: the function to evaluate with the given args
        :param function args: the function arguments to pass
        """
        
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
        
    
    def multiply(self, temp=False):
        """Append an addition function to the functions stack and any existing number expression\n
        \n
        """
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
            
        
    def divide(self, temp=False):
        """
        Append an addition function to the functions stack and any existing number expression\n
        \n
        """
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
        
    def shift_mapping(self, offset, shift_type='semitone'):
        """
        shift the mapping structure every time a note not belonging to the original mapping is played
        :param int offset: the offset in semitones
        :param str shift_type: the type of shifting to perform. options are now 'semitone' or 'octave shift'
        """
        mappings = list(LambdaMapping.items())
        self._notesList = []
        
        if shift_type == 'random':
            shift_type = random.choice(['octave shift', 'semitone shift'])
            print(shift_type)
            self.mapscheme.formatAndSend(shift_type, display=3, syntax_color='error:')
        
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
        self.mapscheme.formatAndSend('eval mapped to ' +
                                     note_names.get((LambdaMapping.get('eval')[0]%len(note_names))+24) + ' (' +
                                     str(LambdaMapping.get('eval')[0]) + ')', display=3,
                                     syntax_color='e_debug:');
        #print('new valid notes', self._notesList)
        
    def zeroPlusRec(self):
        if len(self._successorHead) > 0:
            print('succ head: ', trampolineRecursiveCounter(self._successorHead[0]))
            
            if self._temp is False:
                self._numberStack = []                                
                #print result:
                self.mapscheme.formatAndSend('zero', display=1, syntax_color='zero:')  
                #self.mapscheme.newLine(display=1)
                self.mapscheme.formatAndSend(str(trampolineRecursiveCounter(self._successorHead[0])), \
                                             display=2, syntax_color='int:', spacing=False)

                self._numberStack.append(self._successorHead[0])
                self._fullStack.append(self._successorHead[0])
                                                
            
            else:
                self.mapscheme.formatAndSend('zero', display=1, syntax_color='zero:')  
                #self.mapscheme.newLine(display=1)
                
                if len(self._tempStack) > 0:
                    self._tempNumberStack = []                                                                            
                    if self._tempStack[0] == '(':
                        self._tempNumberStack.append(self._successorHead[0])
                        self.mapscheme.formatAndSend(str(trampolineRecursiveCounter(self._tempNumberStack[0])), \
                                                     display=2, syntax_color='int:', spacing=False)                                        
                        
                        if len(self._tempFunctionStack) > 0:
                            self.evaluateFunctionStack(self._tempFunctionStack, True)                        
                            if (self._tempNumberStack[0].__name__ is 'succ1'):
                                self._evalStack = []
                                self._evalStack.append(trampolineRecursiveCounter(self._tempNumberStack[0]))
                                self.mapscheme.formatAndSend(str(self._evalStack[0]), display=3, \
                                                             syntax_color='result:')                                
                                print(self._evalStack[0])                        
                                self._tempFunctionStack = []        
                  
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
    
    def iszero(self, number_expression):
        """
        lambda function to return true (select_first) if the number expression is zero (i.e. identity func)\n
        otherwise returns false (selet_second)\n
        [in lambda notation: ƛn.(n true) ]\n
        \n
        :param function number_expression: a funtional representation of an integer (with succesor function)
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
        [in lambda notation: ƛn.ƛs.((s false) n) ]\n
        
        :param function number: zero or successors of zero as integer representations  
        """
        
        def succ1(successor):
            """
            :param function succesor: a bound variable to be replaced by the argument after final application (i.e. select_first)
                    
            """
            return successor(self.false)(number)
        
        return succ1
    
    
    def predecessor(self, number):
        """
        lambda predecessor function. Returns a function which returns zero if number argument is zero otherwise\n 
        reduces the number expression argument by one level\n
        [in lambda notation: ƛn.(((iszero n) zero)(n false)) ]\n
        
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
                
    def recursiveCounter(self, succesor_expression, counter=0):
        """
        function to count how many times succesor functions are nested until the zero is reached. Returns the count as int.
        
        :param function succesor_expression: the nested succesor functions to be reduced until zero\n
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
            applies the succesor function to select_second recursively\n
            \n
            :param function reducedfunc: the function to reduce
            """
            #nonlocal reduced # this is really functional now            
            return reducedfunc(self.false)              
        
        if succesor_expression.__name__ is 'succ1':
            #recursion point 1
            return self.recursiveCounter(countreduce(succesor_expression),
                                         sum_one(counter))
        
        elif succesor_expression.__name__ is 'zero':
            if self._debug:
                print(counter)
            return counter
                       
        else:
            if succesor_expression.__name__ is 'successor':
                print('missing a zero to close the successor chain!')
            else:
                print('this function can only process number expression functions as argument!')
                
    def trampolineRecursiveCounter(self, succesor_expression, counter=0):
        """
        function to count how many times succesor functions are nested until the zero is reached. Returns the count as int.
        
        :param function succesor_expression: the nested succesor functions to be reduced until zero\n
        :param int counter: the integer to increment on each recursion\n
        :param boolean debug: wheather to print debg messages or not
        """         
        
        if type(succesor_expression) is tuple:
            expression = succesor_expression[1]            
        else:
            expression = succesor_expression
        
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
        :param function x: functional representation of an integer [i.e. succesor(succesor(zero)) ]
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
        :param function x: functional representation of an integer [i.e. succesor(succesor(zero)) ]
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
        :param function x: functional representation of an integer [i.e. succesor(succesor(zero)) ]
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
        :param function x: functional representation of an integer [i.e. succesor(succesor(zero)) ]
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

