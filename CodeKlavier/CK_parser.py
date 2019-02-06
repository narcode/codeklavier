"""
Music parsing functions for the Codeklavier
"""

import numpy as np


class CK_Parser(object):
    """
    Main parser class with handy functions to parse Music
    """
    
    def __init__(self):
        self._chordmemory = []
        self._deltamemory = []      

    def compareChordRecursive(self, basechord, note, deltatime=0, deltatolerance=0.03,debug=False):
        """
        Compare played chord with a stored chord. Returns True if the chord matches.
    
        i.e. MIDI note order doesn't matter
    
        param array basechord: the array of notes conforming the base chord for comparison
        param int note: incoming MIDI note
        param float deltatime: the deltatime of the incoming MIDI message
        param float deltatolerance: the minimum deltatime tolerance to consider the 
        incoming notes a chord (i.e. simultanously played)
        """
        compare = False
        
        if debug:
            print('chordmem', self._chordmemory, '\ndeltamem', self._deltamemory, '\nnote', note)
        
        
        if note in basechord:
            if note not in self._chordmemory:
                self._chordmemory.append(note)
                self._deltamemory.append(deltatime)
                
                if len(self._chordmemory) == 2:
                    average = np.average(np.diff(self._deltamemory))
                    if average > (deltatolerance + 0.04):
                        print('length 2 avg:', average)
                        self._chordmemory.pop(0)
                        self._deltamemory.pop(0)
    
        else:
            self._chordmemory = []
            self._deltamemory = []
                
        if len(self._chordmemory) == len(basechord):
            print('yes lebngth:', self._chordmemory)
            playedchord = np.sort(self._chordmemory)
            basechord = np.sort(basechord) 
            
            average = np.average(np.diff(self._deltamemory))
            if debug:
                print('avergage:', average)
        
            if average < deltatolerance:
                
                compare = np.array_equal(np.sort(playedchord), np.sort(basechord))
                    
                if debug:
                    print('chordmem:' + str(self._chordmemory),
                         '\nplayed:' + str(playedchord),
                         '\nbasechord:' + str(basechord),
                         '\ncomparison: ' + str(compare),
                         '\ndeltamem:' + str(self._deltamemory),
                         '\ndelta average: ', average)   
                
    
            self._deltamemory = []
            self._chordmemory = []      
            print('end recursion')
            return compare
        
        else:
            return note, 'chord not complete'
        
        compareChordRecursive(basechord, note, deltatime, deltatolerance, debug)
    
    
    def parseChord(self, note, size=4, deltatime=0, deltatolerance=0.03, debug=False):
        """
        Parse notes than are played simultanously and store them in a list
        param int note: The incoming MIDI note
        param int size: The amount of notes that would conform the chord
        param float deltatime: the deltatime of the incoming MIDI message
        param float deltatolerance: the minimum deltatime tolerance to consider the 
        incoming notes a chord (i.e. simultanously played)
        """
          
        self._chordmemory.append(note)
        self._deltamemory.append(deltatime)
        
        if debug:
            print('b chordmem: ', self._chordmemory, 'b deltamem', self._deltamemory)
            
        if len(self._chordmemory) > 1:
            average = np.average(np.diff(self._deltamemory))
            print('diff:', average)
            if average > deltatolerance or average == 0:
                self._chordmemory = []
                self._deltamemory = []

        if len(self._chordmemory) > size:
            self._chordmemory = self._chordmemory[-1:]
            self._deltamemory = self._deltamemory[-1:]
        
        if len(self._chordmemory) == size:
            average = np.average(np.diff(self._deltamemory))
            
            if average < deltatolerance:
                chord = self._chordmemory
                self._chordmemory = []
                self._deltamemory = []
                return True, chord, average
            
        if debug:
            print('chordmem: ', self._chordmemory, 'deltamem', self._deltamemory)

        return False, None, None     
    