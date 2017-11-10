import rtmidi
from functools import reduce
from .Motifs import Motifs_Anne as Motifs

class Motippets(object):
    """Class to handle the midi input.

    classes for Motippets.
    Second prototype of the CodeKlavier
    """

    def __init__(self, mapping, noteonid):
        """The method to initialise the class and prepare the class variables.
        """
        self.mapscheme = mapping
        self.noteonid = noteonid
        self._memory = []
        self._mainMotifs = []
        self._miniMotifs = []
        self._miniMotifs2 = []
        self._pianosections = [47, 78, 108]
        self._motif1_counter = 0
        self._motif2_counter = 0
        self._intervalsArray = []
        self._unmapCounter1 = 0
        self._unmapCounter2 = 0
        self._conditionalCounter = 0
        self._conditionalsBuffer = []
        self._resultCounter = 0
        self._conditionalStatus = ""
        self._deltatime = 0

    def parse_midi(self, event, section):
        """Parse the midi signal and process it depending on the register.
        
        event: describes the midi event that was triggered\n
        section: the MIDI piano range (i.e. low register, mid or high)
        """
        message, deltatime = event
        self._deltatime += deltatime
        if message[2] > 0 or message[0] != 254: #only noteOn and ignore activesense
            if (message[0] == 176): #pedal stop (TODO: handle in Mapping class!)
                note = message[1]
                self.mapscheme.mapping(note)
                return
                
            if (message[0] == self.noteonid):
                note = message[1]
                
                ### LOW SECTION
                if section == 'low':
                    if note <= self._pianosections[0]:
                        self.memorize(note, 20, False, 'Low: ')
                                                    
                        mini_motif_1_Low_played = self.compare_motif(
                                                    self._memory, 'mini',
                                                    Motifs().mini_motif_1_low(),
                                                    note, False)
                        mini_motif_2_Low_played = self.compare_motif(
                                                    self._memory, 'mini2',
                                                    Motifs().mini_motif_2_low(),
                                                    note, False)
                        
                        if (mini_motif_1_Low_played and
                            self._unmapCounter2 == 0):
                            self.mapscheme.miniSnippets(1, 'low')
                        elif (mini_motif_1_Low_played and
                              self._unmapCounter2 > 0):
                            self.mapscheme.miniSnippets(1, 'low with unmap')
                        elif (mini_motif_2_Low_played and
                              self._unmapCounter1 == 0):
                            self.mapscheme.miniSnippets(2, 'low')
                        elif (mini_motif_2_Low_played and
                              self._unmapCounter1 > 0):
                            self.mapscheme.miniSnippets(2, 'low with unmap')
                            
                ### MID SECTION
                elif section == 'mid':
                    if (note > self._pianosections[0] and
                        note <= self._pianosections[1]):
                        self.memorize(note, 20, False, 'Mid: ')
                        
                        # see if motif_1 is played:
                        motif1_played = self.compare_chordal_motif(
                                                self._memory, Motifs().motif_1(), 
                                                note, True)
                        if motif1_played and self._motif1_counter == 0:
                            self.mapscheme.snippets(1)
                            self._motif1_counter = 1                        
                        
                        mini_motif_1_Mid_played = self.compare_motif(
                                                    self._memory, 'mini',
                                                    Motifs().mini_motif_1_mid(),
                                                    note, False)
                        mini_motif_2_Mid_played = self.compare_motif(
                                                    self._memory, 'mini2',
                                                    Motifs().mini_motif_2_mid(),
                                                    note, False)
                        #if self._motif1_played: ??? make a delegate?
                        if (mini_motif_1_Mid_played and
                            self._unmapCounter2 == 0):
                            self.mapscheme.miniSnippets(1, 'mid')
                        elif (mini_motif_1_Mid_played and
                              self._unmapCounter2 > 0):
                            self.mapscheme.miniSnippets(1, 'mid with unmap')
                        elif (mini_motif_2_Mid_played and
                              self._unmapCounter1 == 0):
                            self.mapscheme.miniSnippets(2, 'mid')
                        elif (mini_motif_2_Mid_played and
                              self._unmapCounter1 > 0):
                            self.mapscheme.miniSnippets(2, 'mid with unmap')
                            
                ### HI SECTION
                elif section == 'hi':
                    if note > self._pianosections[1]:
                        self.memorize(note, 20, False, 'Hi: ')
                        
                        mini_motif_1_Hi_played = self.compare_motif(
                                                    self._memory, 'mini',
                                                    Motifs().mini_motif_1_hi(),
                                                    note, True)
                        mini_motif_2_Hi_played = self.compare_motif(
                                                    self._memory, 'mini2',
                                                    Motifs().mini_motif_2_hi(),
                                                    note, True)
                        
                        if (mini_motif_1_Hi_played and
                            self._unmapCounter2 == 0):
                            self.mapscheme.miniSnippets(1, 'hi')
                        elif (mini_motif_1_Hi_played and
                              self._unmapCounter2 > 0):
                            self.mapscheme.miniSnippets(1, 'hi with unmap')
                        elif (mini_motif_2_Hi_played and
                              self._unmapCounter1 == 0):
                            self.mapscheme.miniSnippets(2, 'hi')
                        elif (mini_motif_2_Hi_played and
                              self._unmapCounter1 > 0):
                            self.mapscheme.miniSnippets(2, 'hi with unmap')
                            
                ### TEMOLO
                elif section == 'tremoloHi':
                    if note > self._pianosections[1]:
                        self.memorize(note, 4, False, 'Tremolo Hi: ')
                        
                        if self.count_notes(self._memory, False) == 4:
                            self.tremolo_value(
                                [self._memory[2], self._memory[3]], 'hi',
                                self._deltatime, 0.1, False)
                
                elif section == 'tremoloMid':
                    if (note > self._pianosections[0] and
                        note <= self._pianosections[1]):
                        self.memorize(note, 4, True, 'Tremolo Mid: ')
                        
                        if self.count_notes(self._memory, False) == 4:
                            self.tremolo_value(
                                [self._memory[2], self._memory[3]], 'mid',
                                self._deltatime, 0.1, True)
                    
                elif section == 'tremoloLow':
                    if note <= self._pianosections[0]:
                        self.memorize(note, 4, False, 'Tremolo Low: ')
                        
                        if self.count_notes(self._memory, False) == 4:
                            self.tremolo_value(
                                [self._memory[2], self._memory[3]], 'low',
                                self._deltatime, 0.1, False)

                ### FULL REGISTER            
                elif section == 'full':
                    self.memorize(note, 20, False, 'Main Memory: ')
                    
                    # check if motif_2 is played:
                    motif2_played = self.compare_chordal_motif(
                                        self._memory, Motifs().motif_2(), note,
                                        False)
                    if motif2_played:
                        if self._motif2_counter == 0:
                            self.mapscheme.snippets(2)
                            self._motif2_counter = 1
                            
                ### CONDITONALS
                elif section == 'conditionals': 
                            
                    if note <= self._pianosections[0]:
                        self.memorize(note, 20, False, 'Conditional Memory: ')
                    
                        conditional2_played = self.compare_chordal_motif(
                                            self._memory,
                                            Motifs().conditional_2(),
                                            note, True)
                    
                        if conditional2_played:
                            if self._conditionalCounter == 0:
                                self.mapscheme.conditional(2)
                                self._memory = []
                                self._conditionalCounter += 1


                    if note > self._pianosections[1]:
                        self.memorize(note, 20, False, 'Conditional Memory: ')
                    
                        result2_played = self.compare_motif(
                                        self._memory, 'conditional result 2',
                                        Motifs().conditional_result_2(),
                                        note, True)
                        
                        if result2_played and self._resultCounter == 0: 
                            if self._conditionalCounter > 0:
                                self.mapscheme.result(2, 'comment')
                                self._conditionalsBuffer = []
                                self._resultCounter += 1
                                self._conditionalStatus = "2 on"
                        
                            return self._conditionalStatus            
                    
    def memorize(self, midinote, length, debug=False, debugname="Motippets", conditional="off"):
        """Store the incoming midi notes by appending to the memory array.

        midinote: the incoming MIDI note message\n
        length: the size of the array to store the midinotes\n
        debug: flag to print console debug messages\n
        debugname: prefix for the debug messages
        conditional: if a parallel buffer is filled in for the conditional functions
        """
        self._memory.append(midinote)

        if len(self._memory) > length:
            self._memory = self._memory[-length:]
        
        if debug == True:
            print(debugname + ','.join(map(str, self._memory)))
            if conditional == "on":
                print(debugname + ','.join(map(str, self._conditionalsBuffer)))            
            
        if conditional == "on":
            self._conditionalsBuffer.append(midinote)
            if len(self._conditionalsBuffer) > length:
                self._conditionalsBuffer = self._conditionalsBuffer[-length:]
                
  
    def count_notes(self, array, debug=False):
        """See if notes are repeated in the passed array so as to be considered
        a tremolo. Can detect tremolos and also triple tremolos, or unisons.
        
        TODO: descrine input and output
        """
        if len(array) > 2:
            count1 = array.count(array[0])
            count2 = array.count(array[1])
            
            if debug:
                print('array is ' + str(array),'repeated notes1: ' + \
                      str(count1), 'repeated notes2: ' + str(count2))
            
            return count1 + count2
        return 0

    def compare_motif(self, array, motiftype, motif, note, debug=False):
        """Compare the passed array to a given array

        i.e. detect if a motif is played

        TODO: describe input params
        """
        if motiftype == 'mini':
            if note in motif:
                self._miniMotifs.append(note)
            else:
                self._miniMotifs = []
                return False #@narcode: is this correct?
            
            if len(self._miniMotifs) >= len(motif):
                self._miniMotifs = self._miniMotifs[-len(motif):]
                if self._miniMotifs == motif:
                    compare = True
                    self._unmapCounter1 += 1
                else:
                    compare = False
                
                if debug:
                    print('played ->' + str(self._miniMotifs), '\nmotif ->' + \
                        str(motif), '\ncomparison: ' + str(compare))
                
                return compare
            
        elif motiftype == 'mini2':
            if note in motif:
                self._miniMotifs2.append(note)
            else:
                self._miniMotifs2 = []
                return False #@narcode: is this correct?
                
            if len(self._miniMotifs2) >= len(motif):
                self._miniMotifs2 = self._miniMotifs2[-len(motif):]
                if self._miniMotifs2 == motif:
                    compare = True
                    self._unmapCounter2 += 1
                else:
                    compare = False
                    
                if debug:
                    print('played ->' + str(self._miniMotifs2),
                          '\nmotif 2 ->' + str(motif),
                          '\ncomparison: ' + str(compare))
                
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
                
                if debug:
                    print('played ->' + str(self._mainMotifs), 
                          '\nbig motif ->' + str(motif),
                          '\ncomparison: ' + str(compare))
                
                return compare

    def compare_chordal_motif(self, array, motif, note, debug=False):
        """Compare chordal motifs
        
        i.e. MIDI note order doesn't matter
        
        TODO: describe input/output params
        """
        if note in motif:
            self._mainMotifs.append(note)
        else:
            self._mainMotifs = []
            
        if len(self._mainMotifs) >= len(motif):
            self._mainMotifs = self._mainMotifs[-len(motif):]
            sum_motif = reduce(
                            (lambda total, sumnotes: total + sumnotes),
                            motif)
            sum_played = reduce(
                            (lambda total, sumnotes: total + sumnotes),
                            self._mainMotifs)
            if sum_motif == sum_played:
                compare = True
            else:
                compare = False
            
            if debug:
                print('played ->' + str(self._mainMotifs),
                      '\nmotif ->' + str(motif),
                      '\ncomparison: ' + str(compare),
                      '\nsum played: ' + str(sum_played),
                      '\nsum motif: ' + str(sum_motif))
            
            return compare

    def tremolo_value(self, notes, pianosection, deltatime,
                     deltatolerance, debug=False):
        """Get the interval of a given tremolo.
        
        TODO: describe input params
        """
        if deltatime < deltatolerance:
            interval = abs(notes[1] - notes[0])
            self._intervalsArray.append(interval)
            self._intervalsArray = self._intervalsArray[-2:]
            
            interval_reduce = reduce(
                                (lambda total, sumnotes: total - sumnotes),
                                self._intervalsArray)
            
            if (interval_reduce != 0 and interval > 0):
                    if debug:
                        print('interval ' + pianosection + ': ' + str(interval))
                    if pianosection == 'hi':
                        self.mapscheme.tremolo('hi', interval)
                    elif pianosection == 'mid':
                        self.mapscheme.tremolo('mid', interval)
                    elif pianosection == 'low':
                        self.mapscheme.tremolo('low', interval)
