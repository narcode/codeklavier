"""CK_lambda functions

Contains basic Lambda calculus expressions
"""    

import functools
from fn import recur

def zero(body=''):
    """
    lambda identity function. Also represents 0 (zero)\n
    returns the function/argument it was applied to\n
    (in lambda notation: ƛx.x)\n
    \n
    :param function body: body variable to replace with the application argument\n
    """
    return body

def true(function1):
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
       

def false(function1):
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

def iszero(number_expression):
    """
    lambda function to return true (select_first) if the number expression is zero (i.e. identity func)\n
    otherwise returns false (selet_second)\n
    [in lambda notation: ƛn.(n true) ]\n
    \n
    :param function number_expression: a funtional representation of an integer (with succesor function)
    """
    
    return number_expression(true)

def negation(boolean_expression):
    """
    returns the negation of the expression.\n
    The expression is a boolean functions, either true or false.\n
    \n
    [in lambda notation: ƛx.((x, false), true) ]
    """
    
    return boolean_expression(false)(true)

def simpleReduce(*functions, debug=False):
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
    
    if debug:        
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
        

def successor(number):
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
        return successor(false)(number)
    
    return succ1


def predecessor(number):
    """
    lambda predecessor function. Returns a function which returns zero if number argument is zero otherwise\n 
    reduces the number expression argument by one level\n
    [in lambda notation: ƛn.(((iszero n) zero)(n false)) ]\n
    
    :param function number: zero or successors of zero as integer representations
    \n
    \nNOTE: The function stops at zero. It doesn't return -1 when applied to zero!
    """
    
    if type(number) is not tuple:
        if iszero(number).__name__ is 'true':
            return zero
        else:
            return number(false)
    else:
        if number[0].__name__ is 'mult_trampoline':
            return number[1][1](false)
            
def recursiveCounter(succesor_expression, counter=0, debug=False):
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
        return reducedfunc(false)              
    
    if succesor_expression.__name__ is 'succ1':
        #recursion point 1
        return recursiveCounter(countreduce(succesor_expression),
                                     sum_one(counter))
    
    elif succesor_expression.__name__ is 'zero':
        if debug:
            print(counter)
        return counter
                   
    else:
        if succesor_expression.__name__ is 'successor':
            print('missing a zero to close the successor chain!')
        else:
            print('this function can only process number expression functions as argument!')
 
@recur.tco            
def trampolineRecursiveCounter(succesor_expression, counter=0, debug=False):
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
        return True, (expression(false), counter + 1)
    
    elif expression.__name__ is 'zero':
        if debug:
            print(counter)
        return False, counter
                   
    else:
        if expression.__name__ is 'successor':
            print('missing a zero to close the successor chain!')
        else:
            print('this function can only process number expression functions as argument!', expression)    
            
def add(x, y):
    """
    function to get the result of the addition of two number expressions.\n
    Returns the resulting representation of an integer\n
    \n
    :param function x: functional representation of an integer [i.e. succesor(succesor(zero)) ]
    :param function y: functional representation of an integer
    """
    
    if iszero(y).__name__ is 'true':
        return x
    else:
        return add(successor(x), predecessor(y))

@recur.tco
def add_trampoline(x, y):
    """
    function to get the result of the addition of two number expressions.\n
    Returns the resulting representation of an integer\n
    \n
    :param function x: functional representation of an integer [i.e. succesor(succesor(zero)) ]
    :param function y: functional representation of an integer
    """   
    
    if iszero(y).__name__ is 'true':
        return False, x
    else:
        return True, (successor(x), predecessor(y))
        
def mult(x, y):
    """
    function to get the result of the multiplication of two number expressions.\n
    Returns the resulting representation of an integer\n
    \n
    :param function x: functional representation of an integer [i.e. succesor(succesor(zero)) ]
    :param function y: functional representation of an integer
    """
    
    if iszero(y).__name__ is 'true':
        return zero
    else:
        return add(x, mult(x, predecessor(y)))

@recur.tco
def mult_trampoline(x, y, acc=zero):
    """
    function to get the result of the multiplication of two number expressions.\n
    Returns the resulting representation of an integer\n
    \n
    :param function x: functional representation of an integer [i.e. succesor(succesor(zero)) ]
    :param function y: functional representation of an integer
    """
    
    if type(y) is not tuple and iszero(y).__name__ is 'true':
        return False, acc
    else:
        #return add(x, mult(x, predecessor(y)))            
        acc = add_trampoline(x, acc)
        return True, (x, predecessor(y), acc)

@recur.tco
def divide(x, y, acc=zero):
    """
    function to get the result of the division between two number expressions.\n
    Returns the resulting representation of an integer\n
    DOESN'T HANDLE FLOATS AND DIVIDING BY ZERO RETURNS ZERO\n
    \n
    :param function x: functional representation of an integer [i.e. succesor(succesor(zero)) ]
    :param function y: functional representation of an integer
    """    
    
    if less(x, y).__name__ is 'true':
        return False, acc
    else:
        acc = successor(acc)        
        return True, (substract(x, y), y, acc)


@recur.tco
def substract(x, y):
    """
    function to get the result of the substraction of two number expressions.\n
    IT DOES NOT HANDLE NEGATIVE NUMBERS, SO NEGATIVE NUMBERS RETURN ZERO
    Returns the resulting representation of an integer\n
    \n
    :param function x: functional representation of an integer [i.e. succesor(succesor(zero)) ]
    :param function y: functional representation of an integer
    """    
    
    if iszero(y).__name__ is 'true':
        return False, x
    else:
        return True, (predecessor(x), predecessor(y))
    
@recur.tco
def equal(x, y):
    """
    function to get the boolean result of the comparison between two number expressions.\n
    Comparison is EQUAL THAN\n
    Returns true or false function definitions\n
    \n
    :param function x: functional representation of an integer [i.e. succesor(succesor(zero)) ]
    :param function y: functional representation of an integer
    """    
    
    if iszero(x).__name__ is 'true' and iszero(y).__name__ is 'true':
        return False, true
    
    elif iszero(x).__name__ is 'true' or iszero(y).__name__ is 'true':
        return False, false

    else:
        return True, (predecessor(x), predecessor(y))
            

def greater(x, y):
    """
    function to get the boolean result of the comparison between two number expressions.\n
    Comparison is GREATER THAN\n
    Returns true or false function definitions\n
    \n
    :param function x: functional representation of an integer [i.e. succesor(succesor(zero)) ]
    :param function y: functional representation of an integer
    """    
    
    return negation(iszero(substract(x, y)))

def less(x, y):
    """
    function to get the boolean result of the comparison between two number expressions.\n
    Comparison is GREATER THAN\n
    Returns true or false function definitions\n
    \n
    :param function x: functional representation of an integer [i.e. succesor(succesor(zero)) ]
    :param function y: functional representation of an integer
    """    
    
    return negation(iszero(substract(y, x)))
    
def test_func(*args):
    return "narcode"

# solutions for stack overflow due to recursive limit
def callTrampoline(f):
    """
    encode instructions for trampoline function 
    """
    def g(*args, **kwds):
        return f, args, kwds
    
    return g

def stopTrampoline(value):
    """return a triple to stop the trampoline iteration
    """
    return None, value, None

def with_trampoline(f):
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