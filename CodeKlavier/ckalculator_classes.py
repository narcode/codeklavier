#!/usr/bin/env python3

from inspect import signature
from Motifs import motifs as LambdaMapping

class Ckalculator(object):
    """Ckalculator Class
    
    The main class behind the Ckalculator prototype. Lambda calculus with the piano (simple arithmetic operations)
    """
    
    def __init__(self, noteonid, noteoffid):
        """The method to initialise the class and prepare the class variables.
        """
        #self.mapscheme = mapping
        self.note_on = noteonid
        self.note_off = noteoffid
        self._memory = []
        self._functionStack = []
        self._successorHead = []
        self._conditionalsBuffer = []
        self._pianosections = []
        self._lambda = CK_lambda(True)
        
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
            if note in LambdaMapping.get('successor'):
                self.build_succesor(self._lambda.successor)

            elif note is LambdaMapping.get('eval'):
                if len(self._successorHead) > 0:
                    self._functionStack = []
                    self._lambda.recursiveCounter(self._successorHead[0])
                    self._functionStack.append(self._successorHead[0])
                    self._successorHead = []
                
            elif note in LambdaMapping.get('predecessor'):
                if len(self._functionStack) == 0:
                    self.build_predecessor(self._lambda.zero)
                else:
                    self.build_predecessor(self._lambda.predecessor)
                
    def build_succesor(self, function):
        """
        builds a successor functions chain.\n
        \n
        :param function function: the function to apply the successor function to
        """
        
        print(function.__name__)       
                
        def nestFunc(function1):
            if len(self._successorHead) == 0:
                return function(self._lambda.zero)
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
        
        print(function.__name__)       
                
        def nestFunc(function1):
            if len(self._functionStack) == 0:
                return function(self._lambda.zero)
            else:
                return function(self._functionStack[0])

        self._functionStack.append(nestFunc(function))
                                    
        if len(self._functionStack) > 1:
            if self._functionStack[0].__name__ is 'zero':
                self._functionStack = []
                return 0
            else:
                self._functionStack = self._functionStack[-1:]
                self._lambda.recursiveCounter(self._functionStack[0])
                                            
    
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
        
        if self.iszero(number).__name__ is 'true':
            return self.zero
        else:
            return number(self.false)
                
    def recursiveCounter(self, succesor_expression, counter=0):
        """
        function to count how many times succesor functions are nested until the zero is reached. Returns the count as int.
        
        :param function succesor_expression: the nested succesor functions to be reduced until zero\n
        :param int counter: the integer to increment on each recursion\n
        :param boolean debug: wheather to print debg messages or not
        """
           
        #print(succesor_expression, 'counter: ', counter)           
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
                
    
    def add(self, x, y):
        """
        function to get the result of the addition of two number expressions.\n
        Returns the resulting representation of an integer\n
        \n
        :param function x: functional representation of an integer [i.e. succesor(succesor(zero)) ]
        :param function y: functional representation of an integer
        """
        
        if self.iszero(y).__name__ is 'true':
            pass
        else:
            return self.add(self.successor(x), self.predecessor(y))
        
        return x
    
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
                       
    def test_func(*args):
        return "narcode"

    