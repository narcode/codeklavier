"""
classes for Motippets.
Second prototype of the CodeKlavier
"""
import rtmidi
from functools import reduce
from .motifs_interface import Motifs

# class to handle the midi input
class Motippets(object):
    def __init__(self, port, mapping, noteonid):
        self.port = port
        self.mapscheme = mapping
        self.noteonid = noteonid
        self._memory = []
        self._mainMotifs = []        
        self._miniMotifs = []
        self._miniMotifs2 = []        
        self._pianosectons = [47, 78, 108]
        self._motif1_counter = 0
        self._motif2_counter = 0
        self._motif1_played = False #maybe not needed
        self._intervalsArray = []
        self._unmapCounter1 = 0
        self._unmapCounter2 = 0

    def parse_midi(self, event, section):
        message, deltatime = event
        if message[2] > 0: #only noteOn
            
            if (message[0] == 176): #pedal stop (TODO: handle in Mapping class!)
                note = message[1]                
                self.mapscheme.mapping(note)
                
            if (message[0] == self.noteonid):
                note = message[1]
                
                if section == 'low':
                    if note <= self._pianosectons[0]:
                        self.memorize(note, 20, True, 'Low: ')

                        # see if motif_1 is played:
                        self._motif1_played = self.compareMotif(self._memory, 'big', Motifs().motif_1(), note, False)
                        if self._motif1_played:
                            if self._motif1_counter == 0:
                                self.mapscheme.snippets(1)
                                self._motif1_counter = 1
                                
                        mini_motif_1_Low_played = self.compareMotif(self._memory, 'mini', Motifs().mini_motif_1_low(), note, True)
                        mini_motif_2_Low_played = self.compareMotif(self._memory, 'mini2', Motifs().mini_motif_2_low(), note, True)
                        
                        if mini_motif_1_Low_played and self._unmapCounter2 == 0:
                            self.mapscheme.miniSnippets(1, 'low')
                        elif mini_motif_1_Low_played and self._unmapCounter2 > 0:
                            self.mapscheme.miniSnippets(1, 'low with unmap')                            
                        elif mini_motif_2_Low_played and self._unmapCounter1 == 0:
                            self.mapscheme.miniSnippets(2, 'low')
                        elif mini_motif_2_Low_played and self._unmapCounter1 > 0:
                            self.mapscheme.miniSnippets(2, 'low with unmap')                            
                            
                                                        
                elif section == 'mid':
                    if note > self._pianosectons[0] and note <= self._pianosectons[1]:
                        self.memorize(note, 20, False, 'Mid: ')
                       
                        mini_motif_1_Mid_played = self.compareMotif(self._memory, 'mini', Motifs().mini_motif_1_mid(), note, False)
                        mini_motif_2_Mid_played = self.compareMotif(self._memory, 'mini2', Motifs().mini_motif_2_mid(), note, False)
                        #if self._motif1_played: ??? make a delegate?
                        if mini_motif_1_Mid_played and self._unmapCounter2 == 0:
                            self.mapscheme.miniSnippets(1, 'mid')
                        elif mini_motif_1_Mid_played and self._unmapCounter2 > 0:
                            self.mapscheme.miniSnippets(1, 'mid with unmap')    
                        elif mini_motif_2_Mid_played and self._unmapCounter1 == 0:
                            self.mapscheme.miniSnippets(2, 'mid')
                        elif mini_motif_2_Mid_played and self._unmapCounter1 > 0:
                            self.mapscheme.miniSnippets(2, 'mid with unmap')                            
                            
                                
                elif section == 'hi':
                    if note > self._pianosectons[1]:
                        self.memorize(note, 20, True, 'Hi: ')
                        
                        mini_motif_1_Hi_played = self.compareMotif(self._memory, 'mini', Motifs().mini_motif_1_hi(), note, True)
                        mini_motif_2_Hi_played = self.compareMotif(self._memory, 'mini2', Motifs().mini_motif_2_hi(), note, True)
                        
                        if mini_motif_1_Hi_played and self._unmapCounter2 == 0:
                            self.mapscheme.miniSnippets(1, 'hi')
                        elif mini_motif_1_Hi_played and self._unmapCounter2 > 0:
                            self.mapscheme.miniSnippets(1, 'hi with unmap')                            
                        elif mini_motif_2_Hi_played and self._unmapCounter1 == 0:
                            self.mapscheme.miniSnippets(2, 'hi')                            
                        elif mini_motif_2_Hi_played and self._unmapCounter1 > 0:
                            self.mapscheme.miniSnippets(2, 'hi with unmap')                 
                            
                elif section == 'tremoloHi':
                    if note > self._pianosectons[1]:
                        self.memorize(note, 4, False, 'Tremolo Hi: ')
                        
                        if self.countNotes(self._memory, False) == 4:
                            self.tremoloValue([self._memory[2], self._memory[3]], 'hi', deltatime, 0.1, False)

                elif section == 'tremoloMid':
                    if note > self._pianosectons[0] and note <= self._pianosectons[1]:
                        self.memorize(note, 4, False, 'Tremolo Mid: ')
                        
                        if self.countNotes(self._memory, False) == 4:
                            self.tremoloValue([self._memory[2], self._memory[3]], 'mid', deltatime, 0.1, False)
                            
                elif section == 'tremoloLow':
                    if note <= self._pianosectons[0]:
                        self.memorize(note, 4, False, 'Tremolo Low: ')
                        
                        if self.countNotes(self._memory, False) == 4:
                            self.tremoloValue([self._memory[2], self._memory[3]], 'low', deltatime, 0.1, False)                            
                else:
                    #memorize the last 20 notes of the complete register:
                    self.memorize(note, 20, False, 'Main Memory: ')

                    # see if motif_2 is played:
                    motif2_played = self.compareChordalMotif(self._memory, Motifs().motif_2(), note, False)
                    if motif2_played:
                        if self._motif2_counter == 0:                        
                            self.mapscheme.snippets(2)
                            self._motif2_counter = 1
                    

# store the incoming midi notes
    def memorize(self, midinote, length, debug, debugname):
        # append incoming midinotes to the memory array
        self._memory.append(midinote)

        if len(self._memory) > length:
            self._memory = self._memory[-length:]

        if debug == True:
            print(debugname + ','.join(map(str, self._memory)))
  
# see if notes are repeated in the passed array so as to be considered a tremolo
# can detect tremolos and also triple tremolos, or unisons
    def countNotes(self, array, debug):
        if len(array) > 2:
            count1 = array.count(array[0])
            count2 = array.count(array[1])

            if debug == True:
                print('array is ' + str(array),'repeated notes1: ' + str(count1), 'repeated notes2: ' + str(count2))
            
            return count1+count2

# compare the passed array to a given array (i.e. detect if a motif is played)
    def compareMotif(self, array, motiftype, motif, note, debug):
        if motiftype == 'mini':
            if note in motif:
                self._miniMotifs.append(note)
            else:
                self._miniMotifs = []
                    
            if len(self._miniMotifs) >= len(motif):
                self._miniMotifs = self._miniMotifs[-len(motif):]
                if self._miniMotifs == motif:
                    compare = True
                    self._unmapCounter1 += 1
                else:
                    compare = False
                
                if debug == True:
                    print('played ->' + str(self._miniMotifs), '\nmotif ->' + str(motif), '\ncomparison: ' + str(compare))
                
                return compare
            
        elif motiftype == 'mini2':
            if note in motif:
                self._miniMotifs2.append(note)
            else:
                self._miniMotifs2 = []
                
            if len(self._miniMotifs2) >= len(motif):
                self._miniMotifs2 = self._miniMotifs2[-len(motif):]
                if self._miniMotifs2 == motif:
                    compare = True
                    self._unmapCounter2 += 1                    
                else:
                    compare = False
                    
                if debug == True:
                    print('played ->' + str(self._miniMotifs2), '\nmotif 2 ->' + str(motif), '\ncomparison: ' + str(compare))
                
                return compare            
        else:
            if note in motif:
                self._mainMotifs.append(note)
            else:
                self._mainMotifs = []
                    
            if len(self._mainMotifs) >= len(motif):
                self._mainMotifs = self._mainMotifs[-len(motif):]
                if self._mainMotifs == motif:
                    compare = True
                else:
                    compare = False
                
                if debug == True:
                    print('played ->' + str(self._mainMotifs), '\nbig motif ->' + str(motif), '\ncomparison: ' + str(compare))
                
                return compare            

# compate chordal motifs (i.e. MIDI note order doesn't matter)
    def compareChordalMotif(self, array, motif, note, debug):
        if note in motif:
            self._mainMotifs.append(note)
        else:
            self._mainMotifs = []
                
        if len(self._mainMotifs) >= len(motif):
            self._mainMotifs = self._mainMotifs[-len(motif):]
            sum_motif = reduce((lambda total, sumnotes: total + sumnotes), motif)
            sum_played = reduce((lambda total, sumnotes: total + sumnotes), self._mainMotifs)
            if sum_motif == sum_played:
                compare = True
            else:
                compare = False
            
            if debug == True:
                print('played ->' + str(self._mainMotifs), '\nmotif ->' + str(motif), '\ncomparison: ' + str(compare), '\nsum played: ' + str(sum_played), 
                      '\nsum motif: ' + str(sum_motif))
            
            return compare            

# get the interval of a given tremolo        
    def tremoloValue(self, notes, pianosection, deltatime, deltatolerance, debug):
        if deltatime < deltatolerance:
            interval = abs(notes[1]-notes[0])
            self._intervalsArray.append(interval)
            self._intervalsArray = self._intervalsArray[-2:]
            
            #print('intervals array: ' + str(self._intervalsArray))
            interval_reduce = reduce((lambda total, sumnotes: total - sumnotes), self._intervalsArray)
            
            if (interval_reduce != 0):
                if interval > 0:
                    if debug:
                        print('interval ' + pianosection + ': ' + str(interval))
                    if pianosection == 'hi':    
                        self.mapscheme.tremolo('hi', interval)        
                    elif pianosection == 'mid':
                        self.mapscheme.tremolo('mid', interval)
                    elif pianosection == 'low':
                        self.mapscheme.tremolo('low', interval)
                    
        
        
        
