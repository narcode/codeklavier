#!/usr/bin/env python3

import rtmidi
from Motifs import lamdba_mapping as LambdaMapping

class Ckalculator(object):
    """Ckalculator Class
    
    The main class behind the Ckalculator prototype. Lambda calculus with the piano (simple arithmetic operations)
    """
    
    def __init__(self, mapping, noteonid):
        """The method to initialise the class and prepare the class variables.
        """
        self.mapscheme = mapping
        self.noteonid = noteonid
        
    
