"""
Music parsing functions for the Codeklavier
"""

import numpy as np
chordmem = []
deltamem = []

def compareChordRecursive(basechord, note, deltatime=0, deltatolerance=0.03,debug=False):
    """
    Compare played chord with a stored chord. Returns True if the chord matches.

    i.e. MIDI note order doesn't matter

    param array basechord: the array of notes conforming the base chord for comparison
    param int note: incoming MIDI note
    param float deltatime: the deltatime of the incoming MIDI message
    param float deltatolerance: the minimum deltatime tolerance to consider the 
    incoming notes a chord (i.e. simultanously played)
    """
    global chordmem, deltamem
    compare = False
    
    if debug:
        print('chordmem', chordmem, '\ndeltamem', deltamem, '\nnote', note)
    
    
    if note in basechord:
        if note not in chordmem:
            chordmem.append(note)
            deltamem.append(deltatime)
            
            if len(chordmem) == 2:
                average = np.average(np.diff(deltamem))
                if average > (deltatolerance + 0.04):
                    print('length 2 avg:', average)
                    chordmem.pop(0)
                    deltamem.pop(0)

    else:
        chordmem = []
        deltamem = []
            
    if len(chordmem) == len(basechord):
        print('yes lebngth:', chordmem)
        playedchord = np.sort(chordmem)
        basechord = np.sort(basechord) 
        
        average = np.average(np.diff(deltamem))
        if debug:
            print('avergage:', average)
    
        if average < deltatolerance:
            
            compare = np.array_equal(np.sort(playedchord), np.sort(basechord))
                
            if debug:
                print('chordmem:' + str(chordmem),
                     '\nplayed:' + str(playedchord),
                     '\nbasechord:' + str(basechord),
                     '\ncomparison: ' + str(compare),
                     '\ndeltamem:' + str(deltamem),
                     '\ndelta average: ', average)   
            

        deltamem = []
        chordmem = []      
        print('end recursion')
        return compare
    
    else:
        return note, 'chord not complete'
    
    compareChordRecursive(basechord, note, deltatime, deltatolerance, chordmem, deltamem, debug)
    

def compareChordRecursiveNoGlobals(basechord, note, deltatime=0, deltatolerance=0.03, chordmem=[], 
                          deltamem=[],debug=False):
    """
    Compare played chord with a stored chord. Returns True if the chord matches.

    i.e. MIDI note order doesn't matter

    param array basechord: the array of notes conforming the base chord for comparison
    param int note: incoming MIDI note
    param float deltatime: the deltatime of the incoming MIDI message
    param float deltatolerance: the minimum deltatime tolerance to consider the 
    incoming notes a chord (i.e. simultanously played)
    """
    #print('chordmem', chordmem, '\ndeltamem', deltamem, '\nnote', note)
    compare = False
    
    if note in basechord:
        if note not in chordmem:
            chordmem.append(note)
            deltamem.append(deltatime)
            
            compare, chordmem, deltamem = compareChordRecursive(basechord, note, deltatime, 
                                                                deltatolerance, chordmem, deltamem)   
            
        if len(chordmem) > len(basechord):
            print('end recursion')
            return compare, chordmem, deltamem

        else:
            
            playedchord = np.sort(chordmem)
            basechord = np.sort(basechord) 
            
            if len(playedchord) > len(basechord):
                playedchord = playedchord[len(basechord):]
                deltamem = deltamem[len(basechord):]          
                
            if len(deltamem) == len(basechord):
                average = np.average(np.diff(deltamem))
                print('average', average)
            else:
                average = 99
        
            if average < deltatolerance:
                
                compare = np.array_equal(np.sort(playedchord), np.sort(basechord))
                    
                if debug:
                    print('chordmem:' + str(chordmem),
                         '\nplayed:' + str(playedchord),
                         '\nbasechord:' + str(basechord),
                         '\ncomparison: ' + str(compare),
                         '\ndeltamem:' + str(deltamem),
                         '\ndelta average: ', average)            
                    
    else:
        chordmem = []
        deltamem = []
        return compare, chordmem, deltamem
    

    return compare, chordmem, deltamem