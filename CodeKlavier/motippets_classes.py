import rtmidi
import numpy as np
from functools import reduce
from Motifs import motifs, conditional_motifs, conditional_motifs_mel, mini_motifs, \
     mini_motifs_mel, conditional_results_motifs, conditional_results_motifs_mel

class Motippets(object):
    """Class to handle the midi input.

    classes for Motippets.
    Second prototype of the CodeKlavier
    """

    def __init__(self, mapping, noteonid, noteoffid, mid_low, mid_hi):
        """The method to initialise the class and prepare the class variables.
        """
        self.mapscheme = mapping
        self.noteonid = noteonid
        self.noteoffid = noteoffid
        self._memory = []
        self._memoryCond = {'Low': {}, 'Hi': {}, 'Mid': {}}
        
        self._mainMotifs = [] #DEP
        self._mainMotifs2 = [] #
        self._mainMotifs1 = [] #
        
        self._miniMotifs = []  #
        self._miniMotifs2 = [] #
        self._miniMotifs3 = [] #
        self._miniMotifs3m = [] #

        self._deltaHelper1 = [] #
        self._deltaHelper2 = [] #
        self._results1 = [] #
        self._results2 = [] #
        self._results3 = [] #
        self._results5 = [] #
        
        self._pianosections = [mid_low, mid_hi] # TODO: MOVE TO .ini
        
        #motifs:
        self._allMotifs = {}
        self._deltaHelper = {}
        self._motifsCount = {}
        for motif in motifs:
            self._motifsCount[motif] = {'played': False, 'count': 0}
            self._allMotifs[motif] = []
            self._deltaHelper[motif] = []
        
        self._conditionalCount = {}
        for motif in conditional_motifs:
            self._allMotifs[motif] = []
            self._deltaHelper[motif] = []
            self._conditionalCount[motif] = {'played': False, 'count': 0, 'type': 'chord'}
            
        for motif in conditional_motifs_mel:
            self._allMotifs[motif] = []
            self._deltaHelper[motif] = []
            self._conditionalCount[motif] = {'played': False, 'count': 0, 'type': 'mel'}
        
        for motif in conditional_results_motifs:
            self._allMotifs[motif] = []
            self._deltaHelper[motif] = []
            self._conditionalCount[motif] = {'played': False, 'count': 0, 'type': 'chord'}
            
        for motif in conditional_results_motifs_mel:
            self._allMotifs[motif] = []
            self._deltaHelper[motif] = []
            self._conditionalCount[motif] = {'played': False, 'count': 0, 'type': 'mel'}            
        
        self._allConditional_motifs = conditional_motifs.copy()
        self._allConditional_motifs.update(conditional_motifs_mel)
        self._conditional_results_all = conditional_results_motifs.copy()
        self._conditional_results_all.update(conditional_results_motifs_mel)
        
        for c in self._allConditional_motifs:
            for register in ['Low', 'Hi', 'Mid']:
                self._memoryCond[register][c] = []
        
        self._miniMotifsLow = {}
        self._miniMotifsMid = {}
        self._miniMotifsHi = {}
        for motif in mini_motifs_mel:
            self._allMotifs[motif] = []
            self._deltaHelper[motif] = []
            
            top_note = np.array(mini_motifs_mel[motif]).max()
            bottom_note = np.array(mini_motifs_mel[motif]).min()
            if top_note <= self._pianosections[0]:
                self._miniMotifsLow[motif] = {'played': False, 'count': 0, 'type': 'mel'}
            elif bottom_note > self._pianosections[0] and top_note <= self._pianosections[1]:
                self._miniMotifsMid[motif] = {'played': False, 'count': 0, 'type': 'mel'}
            elif bottom_note > self._pianosections[1]:
                self._miniMotifsHi[motif] = {'played': False, 'count': 0, 'type': 'mel'}
            else:
                print('your motif ' + motif + ' is in between registers. Please adjust')
                                   
        self._intervalsArray = []
        self._interval = 0
        
        self._unmapCounter1 = 0 #
        self._unmapCounter2 = 0 #
        self._unmapCounter3 = 0 #
        self._unmapCounter3_m = 0 #
        
        self._conditionalCounter = 0
        self._conditionalsBuffer = []
        self._resultCounter = 0
        self._conditionalStatus = None
        self._deltatime = 0
        self._timer = 0
        self._range = 0

    def parse_midi(self, event, section, ck_deltatime=0, target=None):
        """Parse the midi signal and process it depending on the register.

        :param tuple event: describes the midi event that was received
        :param string section: the MIDI piano range (i.e. low register, mid or high)
        :param float ck_deltatime: the deltatime between incoming note-on MIDI messages
        :param int target: target the parsing for a specific snippet. None is no target (used for tremolo parsing)
        """
        message, deltatime = event

        if message[2] > 0 and message[0] == 176: #PEDAL STOP
            note = message[1]
            self.mapscheme.mapping(note, 'Motippets')
            return

        if (message[0] == self.noteonid):
            note = message[1]
            self._deltatime = ck_deltatime

            ### LOW SECTION
            if section == 'low':
                if note <= self._pianosections[0]:
                    self.memorize(note, 4, False, 'Low: ')
                    
                    for motif in self._miniMotifsLow:
                        if self._miniMotifsLow[motif]['type'] == 'mel':
                            
                            self._miniMotifsLow[motif]['played'] = self.compare_motif_new(
                                None, motif,
                                mini_motifs_mel.get(motif),
                                note, section, False)
                            
                            other_minis_count = []
                            mapped_mini = None
                            for m in self._miniMotifsLow:
                                if m != motif:
                                    other_minis_count.append(self._miniMotifsLow[m]['count'])
                                    if self._miniMotifsLow[m]['count'] > 0:
                                        mapped_mini = m
                                        
                            np_others = np.array(other_minis_count)
                            
                            if self._miniMotifsLow[motif]['played'] and np_others.sum() == 0:
                                self.mapscheme.miniSnippets(motif, section)
                                
                            elif self._miniMotifsLow[motif]['played'] and np_others.sum() > 0:
                                if mapped_mini != None:
                                    self.mapscheme.miniSnippets(motif, section, m)
                                    
            ### MID SECTION
            elif section == 'mid':
                if (note > self._pianosections[0] and
                    note <= self._pianosections[1]):
                    self.memorize(note, 9, False, 'Mid: ')
                    
                    for motif in self._miniMotifsMid:
                        if self._miniMotifsMid[motif]['type'] == 'mel':
                            
                            self._miniMotifsMid[motif]['played'] = self.compare_motif_new(
                                None, motif,
                                mini_motifs_mel.get(motif),
                                note, section)
                        
                            other_minis_count = []
                            mapped_mini = None
                            for m in self._miniMotifsMid:
                                if m != motif:
                                    other_minis_count.append(self._miniMotifsMid[m]['count'])
                                    if self._miniMotifsMid[m]['count'] > 0:
                                        mapped_mini = m
                                        
                            np_others = np.array(other_minis_count)
                            
                            if self._miniMotifsMid[motif]['played'] and np_others.sum() == 0:
                                self.mapscheme.miniSnippets(motif, section)
                                
                            elif self._miniMotifsMid[motif]['played'] and np_others.sum() > 0:
                                if mapped_mini != None:
                                    self.mapscheme.miniSnippets(motif, section, m)                        

                    #mini_motif_1_Mid_played = self.compare_motif(
                        #self._memory, 'mini',
                        #mini_motifs.get('mini_motif_1_mid'),
                        #note, False)
                    #mini_motif_2_Mid_played = self.compare_motif(
                        #self._memory, 'mini2',
                        #mini_motifs.get('mini_motif_2_mid'),
                        #note, False)
                    #mini_motif_3_Mid_played = self.compare_motif(
                        #self._memory, 'mini3m',
                        #mini_motifs.get('mini_motif_3_mid'),
                        #note, False)                    

                    #if (mini_motif_1_Mid_played and
                        #self._unmapCounter2 == 0):
                        #self.mapscheme.miniSnippets(1, 'mid')
                    #elif (mini_motif_1_Mid_played and
                          #self._unmapCounter2 > 0):
                        #self.mapscheme.miniSnippets(1, 'mid with unmap')
                    #elif (mini_motif_2_Mid_played and
                          #self._unmapCounter1 == 0):
                        #self.mapscheme.miniSnippets(2, 'mid')
                    #elif (mini_motif_2_Mid_played and
                          #self._unmapCounter1 > 0):
                        #self.mapscheme.miniSnippets(2, 'mid with unmap')
                    #elif (mini_motif_3_Mid_played and
                                          #self._unmapCounter1 == 0 and
                                          #self._unmapCounter2 == 0):
                        #self.mapscheme.miniSnippets(3, 'mid') 
                    #elif (mini_motif_3_Mid_played and
                          #self._unmapCounter1 > 0):
                        #self.mapscheme.miniSnippets(3, 'mid with unmap 1', )
                    #elif (mini_motif_3_Mid_played and
                          #self._unmapCounter2 > 0):
                        #self.mapscheme.miniSnippets(3, 'mid with unmap 2')                        

            ### HI SECTION
            elif section == 'hi':
                if note > self._pianosections[1]:
                    self.memorize(note, 4, False, 'Hi: ')

                    for motif in self._miniMotifsHi:
                        if self._miniMotifsHi[motif]['type'] == 'mel':
                            
                            self._miniMotifsHi[motif]['played'] = self.compare_motif_new(
                                None, motif,
                                mini_motifs_mel.get(motif),
                                note, section)
                            
                            other_minis_count = []
                            mapped_mini = None
                            for m in self._miniMotifsHi:
                                if m != motif:
                                    other_minis_count.append(self._miniMotifsHi[m]['count'])
                                    if self._miniMotifsHi[m]['count'] > 0:
                                        mapped_mini = m
                                        
                            np_others = np.array(other_minis_count)
                                    
                            if self._miniMotifsHi[motif]['played'] and np_others.sum() == 0:
                                self.mapscheme.miniSnippets(motif, section)
                                
                            elif self._miniMotifsHi[motif]['played'] and np_others.sum() > 0:
                                if mapped_mini != None:
                                    self.mapscheme.miniSnippets(motif, section, m)                            

            ### TREMOLO
            elif section == 'tremoloLow':
                if note <= self._pianosections[0]:
                    self.memorize(note, 4, False, 'Tremolo Low: ')

                    if self.count_notes(self._memory, False) == 4 and len(self._memory) > 3:
                        self.tremolo_value(
                            [self._memory[2], self._memory[3]], 'low',
                            self._deltatime, 0.1, target, False)
                        self._deltatime = 0
                        
            elif section == 'tremoloHi':
                if note > self._pianosections[1]:
                    self.memorize(note, 4, False, 'Tremolo Hi: ')

                    if self.count_notes(self._memory, False) == 4 and len(self._memory) > 3:
                        self.tremolo_value(
                            [self._memory[2], self._memory[3]], 'hi',
                            self._deltatime, 0.1, target, False)
                        self._deltatime = 0

            elif section == 'tremoloMid':
                if (note > self._pianosections[0] and
                    note <= self._pianosections[1]):
                    self.memorize(note, 4, False, target, 'Tremolo Mid: ')

                    if self.count_notes(self._memory, False) == 4 and len(self._memory) > 3:
                        self.tremolo_value(
                            [self._memory[2], self._memory[3]], 'mid',
                            self._deltatime, 0.1, target, False)
                        self._deltatime = 0

            elif section == 'params':
                self.memorize(note, 4, False, 'Parameters tremolo: ')

                if self.count_notes(self._memory, False) == 4 and len(self._memory) > 3:
                    self._interval = self.tremolo_value(
                        [self._memory[2], self._memory[3]], 'full',
                        self._deltatime, 0.1, False)
                    self._deltatime = 0

                    return self._interval

            ### FULL REGISTER (used for Main Motifs)
            elif section == 'full':
                # out of trouble enters for the codespace in case of getting stuck
                if note == 108:
                    self.mapscheme.mapping(note, 'Motippets')

                self.memorize(note, 20, False, 'Full-section Memory: ')
                
                for motif in motifs:
                    self._motifsCount[motif]['played'] = self.compare_chordal_motif(
                        None, motif, motifs.get(motif),
                        note, deltatime=self._deltatime, debug=False)
    
                    if self._motifsCount[motif]['played'] and self._motifsCount[motif]['count'] == 0:
                        self.mapscheme.snippets(motif)
                        self._motifsCount[motif]['count'] = 1                     
                    
                    
            ### CONDITIONALS SECTION
            elif section in ('conditional_1', 'conditional_2', 'conditional_3'): #expandable...
                
                if note <= self._pianosections[0]:
                    self.memorizeCond(note, 20, False, 'Low', section)
                    
                if note > self._pianosections[1]:
                    self.memorizeCond(note, 20, False, 'Hi', section)        
                
                if (note > self._pianosections[0] and note <= self._pianosections[1]):
                    self.memorizeCond(note, 20, False, 'Mid', section)
                    
                for motif in self._allConditional_motifs:
                    if motif == section:
                        if self._conditionalCounter == 0:
                            for register in self._memoryCond:
                                if self._conditionalCount[motif]['type'] == 'chord':
                                    self._conditionalCount[motif]['played'] = self.compare_chordal_motif(
                                        self._memoryCond[register][section], motif, conditional_motifs.get(motif),
                                        note, deltatime=self._deltatime, debug=False)
                                else:
                                    self._conditionalCount[motif]['played'] = self.compare_motif_new(
                                        self._memoryCond[register][section], motif, conditional_motifs_mel.get(motif), 
                                        note, debug=False)
                            
                                if self._conditionalCount[motif]['played']:
                                    self.mapscheme.conditional(motif)
                                    self._conditionalCounter += 1        
                                    break
                                

                if self._conditionalCounter > 0:
                    for result in self._conditional_results_all:
                        for register in self._memoryCond:
                            if self._conditionalCount[result]['type'] == 'mel':
                                if result == 'conditional_result_5':
                                    self._conditionalCount[result]['played'] = self.compare_motif_new(
                                        self._memoryCond[register][section], result, conditional_results_motifs_mel.get(result),
                                        note, register, debug=False)
                            else:
                                self._conditionalCount[result]['played'] = self.compare_chordal_motif(
                                    self._memoryCond[register][section], result, conditional_results_motifs.get(result),
                                    note, deltatime=self._deltatime, debug=False)
                    
                            if self._conditionalCount[result]['played'] and self._resultCounter == 0:
                                self.mapscheme.result_new(result, 'comment')
                                self._conditionalsBuffer = []
                                self._resultCounter += 1
                                self._conditionalStatus = result
                                break

                return self._conditionalStatus
                    
                
            ### CONDITIONAL RANGE
            elif section == 'conditional_range': # parses only MIDI for the conditional which looks at the range being played
                self.memorize(note, 999,
                              debugname="Range conditional memory", debug=False)

                self.get_range(self._memory, self._timer, debug=False)

    def memorize(self, midinote, length, debug=False, debugname="Motippets", conditional="off"):
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

    def memorizeCond(self, midinote, length, debug=False, register=None, motif_name=None):
        """Store the incoming midi notes by appending to the memory array.

        :param midinote: the incoming MIDI note message\n
        :param int length: the size of the array to store the midinotes\n
        :param boolean debug: flag to print console debug messages\n
        :param string register: register name ('Low', 'Hi', 'Mid')
        :param string motif_name: the motif name to store values for
        """
        self._memoryCond[register][motif_name].append(midinote)

        if len(self._memoryCond[register][motif_name]) > length:
            self._memoryCond[register][motif_name] = self._memoryCond[register][motif_name][-length:]

        if debug == True:
            print(motif_name, register, ','.join(map(str, self._memoryCond[register][motif_name])))
            

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
                return False

            if len(self._miniMotifs) >= len(motif):
                self._miniMotifs = self._miniMotifs[-len(motif):]
                if self._miniMotifs == motif:
                    compare = True
                    self._unmapCounter1 += 1
                    self._unmapCounter2 = 0
                    self._unmapCounter3 = 0
                    self._unmapCounter3_m = 0
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
                return False

            if len(self._miniMotifs2) >= len(motif):
                self._miniMotifs2 = self._miniMotifs2[-len(motif):]
                if self._miniMotifs2 == motif:
                    compare = True
                    self._unmapCounter2 += 1
                    self._unmapCounter1 = 0
                    self._unmapCounter3 = 0
                    self._unmapCounter3_m = 0
                else:
                    compare = False

                if debug:
                    print('played ->' + str(self._miniMotifs2),
                          '\nmotif 2 ->' + str(motif),
                          '\ncomparison: ' + str(compare))

                return compare

        elif motiftype == 'mini3':
            if note in motif:
                self._miniMotifs3.append(note)
            else:
                self._miniMotifs3 = []
                return False

            if len(self._miniMotifs3) >= len(motif):
                self._miniMotifs3 = self._miniMotifs3[-len(motif):]
                if self._miniMotifs3 == motif:
                    compare = True
                    self._unmapCounter3 += 1
                    self._unmapCounter1 = 0
                    self._unmapCounter2 = 0
                else:
                    compare = False

                if debug:
                    print('played ->' + str(self._miniMotifs3),
                          '\nmotif 2 ->' + str(motif),
                          '\ncomparison: ' + str(compare))

                return compare
            
        elif motiftype == 'mini3m':
            if note in motif:
                self._miniMotifs3m.append(note)
            else:
                self._miniMotifs3m = []
                return False

            if len(self._miniMotifs3m) >= len(motif):
                self._miniMotifs3m = self._miniMotifs3m[-len(motif):]
                if self._miniMotifs3m == motif:
                    compare = True
                    self._unmapCounter3_m += 1
                    self._unmapCounter1 = 0
                    self._unmapCounter2 = 0
                    self._unmapCounter3 = 0                    
                else:
                    compare = False

                if debug:
                    print('played ->' + str(self._miniMotifs3m),
                          '\nmotif 3 ->' + str(motif),
                          '\ncomparison: ' + str(compare))

                return compare            

        elif motiftype == 'result 1':
            if note in motif:
                self._results1.append(note)
            else:
                self._results1 = []
                return False

            if len(self._results1) >= len(motif):
                self._results1 = self._results1[-len(motif):]
                if self._results1 == motif:
                    compare = True
                    self._unmapCounter2 += 1
                else:
                    compare = False

                if debug:
                    print('played ->' + str(self._results1),
                          '\nmotif 2 ->' + str(motif),
                          '\ncomparison: ' + str(compare))

                return compare

        elif motiftype == 'result 2':
            if note in motif:
                self._results2.append(note)
            else:
                self._results2 = []
                return False

            if len(self._results2) >= len(motif):
                self._results2 = self._results2[-len(motif):]
                if self._results2 == motif:
                    compare = True
                    self._unmapCounter2 += 1
                else:
                    compare = False

                if debug:
                    print('played ->' + str(self._results2),
                          '\nmotif 2 ->' + str(motif),
                          '\ncomparison: ' + str(compare))

                return compare

        elif motiftype == 'result 3': #TODO: optimize with a Dictionary
            if note in motif:
                self._results3.append(note)
            else:
                self._results3 = []
                return False

            if len(self._results3) >= len(motif):
                self._results3 = self._results3[-len(motif):]
                if self._results3 == motif:
                    compare = True
                        #self._unmapCounter3 += 1 #?
                else:
                    compare = False

                if debug:
                    print('played ->' + str(self._results3),
                          '\nmotif 3 ->' + str(motif),
                          '\ncomparison: ' + str(compare))

                return compare

        elif motiftype == 'result 5': #TODO: optimize with a Dictionary
            if note in motif:
                self._results5.append(note)
            else:
                self._results5 = []
                return False

            if len(self._results5) >= len(motif):
                self._results5 = self._results5[-len(motif):]
                if self._results5 == motif:
                    compare = True
                        #self._unmapCounter3 += 1 #?
                else:
                    compare = False

                if debug:
                    print('played ->' + str(self._results5),
                          '\nmotif 5 ->' + str(motif),
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

    def compare_motif_new(self, array, motif_name, motif, note, pianosection=None, debug=False):
        """Compare the passed array to a given array

        i.e. detect if a melodic motif is played

        TODO: describe input params
        """
        compare = False
        if array == None:
            if note in motif:
                self._allMotifs[motif_name].append(note)
            else:
                self._allMotifs[motif_name] = []
        else:
            if len(array) > 0:
                copy_array = array.copy()
                last =  copy_array.pop()
                if last in motif:
                    self._allMotifs[motif_name].append(array.pop())
                #else:
                    #print('2', motif_name, self._allMotifs[motif_name])
                    #self._allMotifs[motif_name] = []
                
        if len(self._allMotifs[motif_name]) >= len(motif):
            self._allMotifs[motif_name] = self._allMotifs[motif_name][-len(motif):]
            if self._allMotifs[motif_name] == motif:
                compare = True                
                if pianosection == 'low':
                    self._miniMotifsLow[motif_name]['count'] += 1
                    for m in self._miniMotifsLow:
                        if m != motif_name:
                            self._miniMotifsLow[m]['count'] = 0
                elif pianosection == 'mid':
                    self._miniMotifsMid[motif_name]['count'] += 1
                    for m in self._miniMotifsMid:
                        if m != motif_name:
                            self._miniMotifsMid[m]['count'] = 0   
                elif pianosection == 'hi':
                    self._miniMotifsHi[motif_name]['count'] += 1
                    for m in self._miniMotifsHi:
                        if m != motif_name:
                            self._miniMotifsHi[m]['count'] = 0
                            
                self._allMotifs[motif_name] = []

            if debug:
                print('played -> ', self._allMotifs[motif_name], '\nmotif ->' + \
                    str(motif), '\ncomparison: ' + str(compare))

        return compare
            
            
    def compare_chordal_motif(self, array, motif_name, motif, note, deltatime=0, deltatolerance=0.005, debug=False):
        """Compare chordal motifs

        i.e. MIDI note order doesn't matter

        TODO: describe input/output params
        TODO 2: make sub arrays if function is used again...
        """      
        compare = False
        if array == None:
            if note in motif:
                self._allMotifs[motif_name].append(note)
                self._deltaHelper[motif_name].append(deltatime)
            else:
                self._allMotifs[motif_name] = []
                self._deltaHelper[motif_name] = []
        else:
            if len(array) > 0:
                mem = array.copy()
                if mem.pop() in motif:
                    self._allMotifs[motif_name].append(note)
                    self._deltaHelper[motif_name].append(deltatime)
                #else:
                    #self._allMotifs[motif_name] = []
                    #self._deltaHelper[motif_name] = []

        if debug:
            print('played ->' + str(self._allMotifs[motif_name]))
                      
        if len(self._allMotifs[motif_name]) >= len(motif):
            self._allMotifs[motif_name] = self._allMotifs[motif_name][-len(motif):]
            self._deltaHelper[motif_name] = self._deltaHelper[motif_name][-(len(motif)-1):]

            sum_motif = reduce(
                (lambda total, sumnotes: total + sumnotes),
                motif)
            sum_played = reduce(
                (lambda total, sumnotes: total + sumnotes),
                self._allMotifs[motif_name])
            dif_delta = reduce( (lambda total, sumtimes: (total +
                                                          sumtimes) / len( self._deltaHelper[motif_name]) ),
                                self._deltaHelper[motif_name])
            #print('average: ', dif_delta)

            if sum_motif == sum_played and (dif_delta < deltatolerance and dif_delta > 0):
                compare = True
                self._allMotifs[motif_name] = []
                self._deltaHelper[motif_name] = []                

                if debug:
                    print('played ->' + str(self._allMotifs[motif_name]),
                          '\nmotif ->' + str(motif),
                          '\ncomparison: ' + str(compare),
                          '\nsum played: ' + str(sum_played),
                          '\nsum motif: ' + str(sum_motif),
                          '\ndelta average: ', dif_delta)

        return compare


    def tremolo_value(self, notes, pianosection, deltatime,
                     deltatolerance, target, debug=False):
        """Get the interval of a given tremolo.

        :param array notes: Array of notes to be analysed
        :param string pianosection: the name of the piano range (i.e. low, mid, etc)
        :param float deltatime: the time between the received midi messages
        :param float deltatolerance: the deltatime max threshold
        :param str target: name that references the targeted snippet
        :param boolean debug: wheather to show or hide debug messages

        TODO: this should only return the interval integer and on another place define what to do with it!
        TODO: describe input params
        """
        if debug:
            print('deltatime :' + str(deltatime), 'tolerance :', str(deltatolerance), 'target snippet: ', target)
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
                    if pianosection == 'full':
                        return interval
                    else:
                        self.mapscheme.tremolo(target, interval, pianosection)

    def get_range(self, notes, time, debug=False):
        """ Get the range between the notes played in a time window

        TODO: show range every iteration

        """
        #if time == 30:
        notes.sort()
        lowest_note = notes[0]
        hightest_note = notes[0]
        if time % 2 == 0:
            notes.reverse()
            hightest_note = notes[0]

            self._range = hightest_note - lowest_note

            if debug:
                print('highest note: ', hightest_note, 'lowest note: ', lowest_note,
                      'difference: ', self._range)

        return self._range
