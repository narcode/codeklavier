import rtmidi
import numpy as np
from functools import reduce
from Motifs import motifs, motifs_mel, conditional_motifs, conditional_motifs_mel, mini_motifs, \
     mini_motifs_mel, conditional_results_motifs, conditional_results_motifs_mel

class Motippets(object):
    """Class to handle the midi input.

    classes for Motippets.
    Second prototype of the CodeKlavier
    """

    def __init__(self, mapping, noteonid, noteoffid, mid_low, mid_hi, playedlimit=1):
        """The method to initialise the class and prepare the class variables.
        """
        self.mapscheme = mapping
        self.noteonid = noteonid
        self.noteoffid = noteoffid
        self._memory = []
        self._memoryCond = {'low': [], 'hi': [], 'mid': []}
        self._memoryCondDeltas = {'deltalow': [], 'deltahi': [], 'deltamid': []}

        self._pianosections = [mid_low, mid_hi]
        self._playedlimt = playedlimit

        #motifs:
        self._allMotifs = {}
        self._deltaHelper = {}
        self._motifsCount = {}

        for motif in motifs:
            self._motifsCount[motif] = {'played': False, 'count': 0, 'type': 'chord'}
            self._allMotifs[motif] = []
            self._deltaHelper[motif] = []

        for motif in motifs_mel:
            self._motifsCount[motif] = {'played': False, 'count': 0, 'type': 'mel'}
            self._allMotifs[motif] = []
            self._deltaHelper[motif] = []

        self._allMainMotifs = motifs.copy()
        self._allMainMotifs.update(motifs_mel)

        self._conditionalCount = {}
        for motif in conditional_motifs:            
            self._allMotifs[motif] = {}
            self._deltaHelper[motif] = {}
            self._conditionalCount[motif] = {'played': False, 'count': 0, 'type': 'chord'}

        for motif in conditional_motifs_mel:
            self._allMotifs[motif] = {}
            self._deltaHelper[motif] = {}
            self._conditionalCount[motif] = {'played': False, 'count': 0, 'type': 'mel'}

        for motif in conditional_results_motifs:
            self._allMotifs[motif] = {}
            self._deltaHelper[motif] = {}
            self._conditionalCount[motif] = {'played': False, 'count': 0, 'type': 'chord'}

        for motif in conditional_results_motifs_mel:
            self._allMotifs[motif] = {}
            self._deltaHelper[motif] = {}
            self._conditionalCount[motif] = {'played': False, 'count': 0, 'type': 'mel'}

        self._allConditional_motifs = conditional_motifs.copy()
        self._allConditional_motifs.update(conditional_motifs_mel)
        self._conditional_results_all = conditional_results_motifs.copy()
        self._conditional_results_all.update(conditional_results_motifs_mel)

        for c in self._allConditional_motifs:
            top_note = np.array(self._allConditional_motifs[c]).max()
            bottom_note = np.array(self._allConditional_motifs[c]).min()
            
            if (bottom_note < self._pianosections[0] 
                and top_note > self._pianosections[0]) or (bottom_note < self._pianosections[1] 
                                                           and top_note > self._pianosections[1]):
                print('your motif ' + c + ' is in between registers. Please adjust')
                
            for register in ['low', 'hi', 'mid']:
                self._allMotifs[c][register] = []
                self._deltaHelper[c][register] = []

        for r in self._conditional_results_all:
            top_note = np.array(self._conditional_results_all[r]).max()
            bottom_note = np.array(self._conditional_results_all[r]).min()
            
            if (bottom_note < self._pianosections[0] 
                and top_note > self._pianosections[0]) or (bottom_note < self._pianosections[1] 
                                                           and top_note > self._pianosections[1]):
                print('your motif ' + r + ' is in between registers. Please adjust')
                
            for register in ['low', 'hi', 'mid']:
                self._allMotifs[r][register] = []
                self._deltaHelper[r][register] = []

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

        for motif in mini_motifs:
            self._allMotifs[motif] = []
            self._deltaHelper[motif] = []

            top_note = np.array(mini_motifs[motif]).max()
            bottom_note = np.array(mini_motifs[motif]).min()
            if top_note <= self._pianosections[0]:
                self._miniMotifsLow[motif] = {'played': False, 'count': 0, 'type': 'chord'}
            elif bottom_note > self._pianosections[0] and top_note <= self._pianosections[1]:
                self._miniMotifsMid[motif] = {'played': False, 'count': 0, 'type': 'chord'}
            elif bottom_note > self._pianosections[1]:
                self._miniMotifsHi[motif] = {'played': False, 'count': 0, 'type': 'chord'}
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
        self._noteCounter = 0
        self._deltatime = 0
        self._deltatime_low = 0
        self._deltatime_mid = 0
        self._deltatime_hi = 0
        self._timer = 0
        self._range = 0

    def parse_midi(self, event, section, ck_deltatime=0, ck_deltatime_low=0, ck_deltatime_hi=0, ck_deltatime_mid=0, target=None):
        """Parse the midi signal and process it depending on the register.

        :param tuple event: describes the midi event that was received
        :param string section: the MIDI piano range (i.e. low register, mid or high)
        :param float ck_deltatime: the deltatime between incoming note-on MIDI messages (whole register)
        :param float ck_deltatime_low: the deltatime between incoming note-on MIDI messages (only low register)
        :param float ck_deltatime_hi: the deltatime between incoming note-on MIDI messages (only hi register)
        :param float ck_deltatime_mid: the deltatime between incoming note-on MIDI messages (only mid register)
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
            self._noteCounter += 1

            ### LOW SECTION
            if section == 'low':
                if note <= self._pianosections[0]:
                    self.memorize(note, 4, False, 'low: ')

                    for motif in self._miniMotifsLow:
                        if self._miniMotifsLow[motif]['type'] == 'mel':

                            self._miniMotifsLow[motif]['played'] = self.compare_motif(
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

                        else:
                            self._miniMotifsLow[motif]['played'] = self.compare_chordal_motif(None, motif,
                                                                                              mini_motifs.get(motif),
                                                                                              note, deltatime=self._deltatime,
                                                                                              pianosection='low', debug=False)
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

                            self._miniMotifsMid[motif]['played'] = self.compare_motif(
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

                        else:
                            self._miniMotifsMid[motif]['played'] = self.compare_chordal_motif(None, motif,
                                                                                              mini_motifs.get(motif),
                                                                                              note, deltatime=self._deltatime,
                                                                                              pianosection='mid',
                                                                                              debug=False)
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

            ### HI SECTION
            elif section == 'hi':
                if note > self._pianosections[1]:
                    self.memorize(note, 4, False, 'Hi: ')

                    for motif in self._miniMotifsHi:
                        if self._miniMotifsHi[motif]['type'] == 'mel':

                            self._miniMotifsHi[motif]['played'] = self.compare_motif(
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
                        else:
                            self._miniMotifsLow[motif]['played'] = self.compare_chordal_motif(None, motif,
                                                                                              mini_motifs.get(motif),
                                                                                              note, deltatime=self._deltatime,
                                                                                              pianosection='hi', debug=False)
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
                            ck_deltatime_low, 0.1, target, True)
                        self._deltatime = 0

            elif section == 'tremoloHi':
                if note > self._pianosections[1]:
                    self.memorize(note, 4, False, 'Tremolo Hi: ')

                    if self.count_notes(self._memory, True) == 4 and len(self._memory) > 3:
                        print(self._deltatime_hi)
                        self.tremolo_value(
                            [self._memory[2], self._memory[3]], 'hi',
                            ck_deltatime_hi, 0.1, target, True)
                        self._deltatime = 0

            elif section == 'tremoloMid':
                if (note > self._pianosections[0] and
                    note <= self._pianosections[1]):
                    self.memorize(note, 4, False, target, 'Tremolo Mid: ')

                    if self.count_notes(self._memory, False) == 4 and len(self._memory) > 3:
                        self.tremolo_value(
                            [self._memory[2], self._memory[3]], 'mid',
                            ck_deltatime_mid, 0.1, target, True)
                        self._deltatime = 0

            elif section == 'params':
                self.memorize(note, 4, False, 'Parameters tremolo: ')

                if self.count_notes(self._memory, False) == 4 and len(self._memory) > 3:
                    self._interval = self.tremolo_value(
                        [self._memory[2], self._memory[3]], 'full',
                        ck_deltatime, 0.1, True)
                    self._deltatime = 0

                    return self._interval

            ### FULL REGISTER (used for Main Motifs)
            elif section == 'full':
                # out of trouble enters for the codespace in case of getting stuck
                if note == 108:
                    self.mapscheme.mapping(note, 'Motippets')

                self.memorize(note, 20, False, 'Full-section Memory: ')

                for motif in self._allMainMotifs:
                    if self._motifsCount[motif]['type'] == 'chord':
                        self._motifsCount[motif]['played'] = self.compare_chordal_motif(
                            None, motif, motifs.get(motif),
                            note, deltatime=self._deltatime, debug=False)

                        if self._motifsCount[motif]['played'] and self._motifsCount[motif]['count'] < self._playedlimt:
                            self.mapscheme.snippets(motif)
                            self._motifsCount[motif]['count'] += 1
                    else:
                        self._motifsCount[motif]['played'] = self.compare_motif(None, motif,
                                                                                motifs_mel.get(motif),
                                                                                note)
                        if self._motifsCount[motif]['played'] and self._motifsCount[motif]['count'] < self._playedlimt:
                            self.mapscheme.snippets(motif)
                            self._motifsCount[motif]['count'] += 1

            ### CONDITIONALS SECTION
            elif section in self._allConditional_motifs:
                
                if note <= self._pianosections[0]:
                    self.memorizeCond(note, 20, False, 'low')
                    self.memorizeCond(ck_deltatime_low, 20, False, 'deltalow', True)

                if note > self._pianosections[1]:
                    self.memorizeCond(note, 20, False, 'hi')
                    self.memorizeCond(ck_deltatime_hi, 20, False, 'deltahi', True)

                if (note > self._pianosections[0] and note <= self._pianosections[1]):
                    self.memorizeCond(note, 20, False, 'mid')
                    self.memorizeCond(ck_deltatime_mid, 20, False, 'deltamid', True)

                for motif in self._allConditional_motifs:
                    if motif == section:
                        if self._conditionalCounter == 0:
                            for register in self._memoryCond:
                                if self._conditionalCount[motif]['type'] == 'chord':
                                    self._conditionalCount[motif]['played'] = self.compare_chordal_motif(
                                        self._memoryCond[register], motif, conditional_motifs.get(motif),
                                        note, deltatime=self._memoryCondDeltas['delta'+register], pianosection=register, debug=False)
                                else:
                                    self._conditionalCount[motif]['played'] = self.compare_motif(
                                        self._memoryCond[register], motif, conditional_motifs_mel.get(motif),
                                        note, pianosection=register, debug=False)

                                if self._conditionalCount[motif]['played']:
                                    self.mapscheme.conditional(motif)
                                    self._conditionalCounter += 1
                                    break


                if self._conditionalCounter > 0:
                    for result in self._conditional_results_all:
                        for register in self._memoryCond:
                            if self._conditionalCount[result]['type'] == 'mel':
                                self._conditionalCount[result]['played'] = self.compare_motif(
                                    self._memoryCond[register], result, conditional_results_motifs_mel.get(result),
                                    note, pianosection=register, debug=False)
                            else:
                                self._conditionalCount[result]['played'] = self.compare_chordal_motif(
                                    self._memoryCond[register], result, conditional_results_motifs.get(result),
                                    note, deltatime=self._memoryCondDeltas['delta'+register], pianosection=register, debug=False)

                            if self._conditionalCount[result]['played'] and self._resultCounter == 0:
                                self.mapscheme.result(result, 'comment')
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

        :param midinote: the incoming MIDI note message
        :param int length: the size of the array to store the midinotes
        :param boolean debug: flag to print console debug messages
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

    def memorizeCond(self, midinote, length, debug=False, pianosection=None, delta=False):
        """Store the incoming midi notes by appending to the memory array.

        :param midinote: the incoming MIDI note message
        :param int length: the size of the array to store the midinotes
        :param boolean debug: flag to print console debug messages
        :param string pianosection: register name ('low', 'hi', 'mid')
        """
        if not delta:                
            self._memoryCond[pianosection].append(midinote)
    
            if len(self._memoryCond[pianosection]) > length:
                self._memoryCond[pianosection] = self._memoryCond[pianosection][-length:]
                
            if debug == True:
                print(pianosection, ','.join(map(str, self._memoryCond[pianosection])))            
        else:
            self._memoryCondDeltas[pianosection].append(midinote)
    
            if len(self._memoryCondDeltas[pianosection]) > length:
                self._memoryCondDeltas[pianosection] = self._memoryCondDeltas[pianosection][-length:]            

            if debug == True:
                print(pianosection, ','.join(map(str, self._memoryCondDeltas[pianosection])))


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

    def compare_motif(self, array, motif_name, motif, note, pianosection=None, debug=False):
        """Compare the passed array to a given array

        Detect if a melodic motif was played

        :param list array: the array of notes to use as input. None is realtime note, one at a time.
        :param str motif_name: the name of the motif to compare
        :param list motif: the motif to compare to (an array of midi notes)
        :param int note: the incoming midi note
        :param str pianosection: ('low', 'mid' or 'hi')
        :param register note: the incoming midi note
        :param boolean debug: flag to print console debug messages
        """
        compare = False
        if array == None:
            if note in motif:
                self._allMotifs[motif_name].append(note)
            else:
                self._allMotifs[motif_name] = []

            played = self._allMotifs[motif_name]

        else:
            if len(array) >= len(motif):
                played = array[-len(motif):]
            else:
                played = []
                #last = array[-1:][0]
                #if last in motif:
                    #self._allMotifs[motif_name][pianosection].append(last)
                #else:
                    #self._allMotifs[motif_name][pianosection] = []

            #played = self._allMotifs[motif_name][pianosection]

        if len(played) >= len(motif):
            played = played[-len(motif):]
            if played == motif:
                compare = True
                if array == None:
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

            if debug:
                print('played -> ', played, '\nmotif ->' + \
                    str(motif), '\ncomparison: ' + str(compare))

        return compare


    def compare_chordal_motif(self, array, motif_name, motif, note, deltatime=0, deltatolerance=0.005,
                              pianosection=None, debug=False):
        """Compare chordal motifs

        i.e. MIDI note order doesn't matter

        TODO: describe input/output params
        """
        compare = False
        if array == None and not isinstance(deltatime, list):
            if note in motif:
                self._allMotifs[motif_name].append(note)
                self._deltaHelper[motif_name].append(deltatime)
            else:
                self._allMotifs[motif_name] = []
                self._deltaHelper[motif_name] = []

            played = self._allMotifs[motif_name]
            deltas = self._deltaHelper[motif_name]

        else:
            if isinstance(deltatime, list):
                if len(array) >= len(motif):
                    played = array[-len(motif):]
                    deltas = deltatime[-(len(motif)-1):]
                else:
                    played = []
                    deltas = []                    
            else:
                played = []
                deltas = []
                #if last in motif:
                    #self._allMotifs[motif_name][pianosection].append(last)
                    #self._deltaHelper[motif_name][pianosection].append(deltatime)
                #else:
                    #self._allMotifs[motif_name][pianosection] = []
                    #self._deltaHelper[motif_name][pianosection] = []

            #played = self._allMotifs[motif_name][pianosection]
            #deltas = self._deltaHelper[motif_name][pianosection]
            
        if len(played) >= len(motif):
            played = played[-len(motif):]
            deltas = deltas[-(len(motif)-1):]

            sum_motif = reduce(
                (lambda total, sumnotes: total + sumnotes),
                motif)
            sum_played = reduce(
                (lambda total, sumnotes: total + sumnotes),
                played)
            dif_delta = reduce( (lambda total, sumtimes: (total +
                                                          sumtimes) / len(deltas) ),
                                deltas)

            if sum_motif == sum_played and (dif_delta < deltatolerance and dif_delta > 0):
                compare = True
                if pianosection == 'low':
                    if motif_name in self._miniMotifsLow:
                        self._miniMotifsLow[motif_name]['count'] += 1
                        for m in self._miniMotifsLow:
                            if m != motif_name:
                                self._miniMotifsLow[m]['count'] = 0
                elif pianosection == 'mid':
                    if motif_name in self._miniMotifsMid:
                        self._miniMotifsMid[motif_name]['count'] += 1
                        for m in self._miniMotifsMid:
                            if m != motif_name:
                                self._miniMotifsMid[m]['count'] = 0
                elif pianosection == 'hi':
                    if motif_name in self._miniMotifsHi:
                        self._miniMotifsHi[motif_name]['count'] += 1
                        for m in self._miniMotifsHi:
                            if m != motif_name:
                                self._miniMotifsHi[m]['count'] = 0

                if debug:
                    print('played ->' + str(played),
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
        """
        if debug:
            print('deltatime :' + str(deltatime), 'tolerance :', str(deltatolerance), 'target snippet: ', target)
        if deltatime < deltatolerance:
            interval = abs(notes[1] - notes[0])
            self._intervalsArray.append(interval)
            self._intervalsArray = self._intervalsArray[-2:]

            print(self._intervalsArray)

            interval_reduce = reduce(
                                (lambda total, sumnotes: total - sumnotes),
                                self._intervalsArray)
            
            print(interval_reduce)

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
