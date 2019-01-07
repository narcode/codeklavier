import rtmidi
from functools import reduce
from Motifs import motifs as Motifs

class Motippets(object):
    """Class to handle the midi input.

    classes for Motippets.
    Second prototype of the CodeKlavier
    """

    def __init__(self, mapping, noteonid):
        """The method to initialise the class and prepare the class variables.

        TODO: post-ICLC experiment how to nest arrays so as to not hvae to init so many empty arrays!
        --> Perhaps change to a dict?
        """
        self.mapscheme = mapping
        self.noteonid = noteonid
        self.noteoffid = 153 #TODO: pass is in init...
        self._memory = []
        self._mainMotifs = []
        self._mainMotifs2 = []
        self._mainMotifs1 = []
        self._miniMotifs = []
        self._miniMotifs2 = []
        self._miniMotifs3 = []
        self._miniMotifs3m = []
        self._deltaHelper = []
        self._deltaHelper1 = []
        self._deltaHelper2 = []
        self._results1 = []
        self._results2 = []
        self._results3 = []
        self._results5 = []
        self._pianosections = [49, 78, 108]
        self._motif1_counter = 0
        self._motif2_counter = 0
        self._intervalsArray = []
        self._interval = 0
        self._unmapCounter1 = 0
        self._unmapCounter2 = 0
        self._unmapCounter3 = 0
        self._unmapCounter3_m = 0
        self._conditionalCounter = 0
        self._conditionalsBuffer = []
        self._resultCounter = 0
        self._conditionalStatus = 0
        self._deltatime = 0
        self._timer = 0
        self._range = 0

    def parse_midi(self, event, section, ck_deltatime=0, target=0):
        """Parse the midi signal and process it depending on the register.

        :param tuple event: describes the midi event that was received
        :param string section: the MIDI piano range (i.e. low register, mid or high)
        :param float ck_deltatime: the deltatime between incoming note-on MIDI messages
        :param int target: target the parsing for a specific snippet. 0 is no target
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

                    mini_motif_1_Low_played = self.compare_motif(
                        self._memory, 'mini',
                        Motifs.get('mini_motif_1_low'),
                        note, False)

                    mini_motif_2_Low_played = self.compare_motif(
                        self._memory, 'mini2',
                        Motifs.get('mini_motif_2_low'),
                        note, False)

                    mini_motif_3_Low_played = self.compare_motif(
                        self._memory, 'mini3',
                        Motifs.get('mini_motif_3_low'),
                        note, False)

                    if (mini_motif_1_Low_played and
                        self._unmapCounter2 == 0 and
                        self._unmapCounter3 == 0):
                        self.mapscheme.miniSnippets(1, 'low')
                    elif (mini_motif_1_Low_played and
                          self._unmapCounter2 > 0):
                        self.mapscheme.miniSnippets(1, 'low with unmap 2')
                    elif (mini_motif_1_Low_played and
                          self._unmapCounter3 > 0):
                        self.mapscheme.miniSnippets(1, 'low with unmap 3')

                    elif (mini_motif_2_Low_played and
                          self._unmapCounter1 == 0 and
                          self._unmapCounter3 == 0):
                        self.mapscheme.miniSnippets(2, 'low')
                    elif (mini_motif_2_Low_played and
                                  self._unmapCounter1 > 0):
                        self.mapscheme.miniSnippets(2, 'low with unmap 1')
                    elif (mini_motif_2_Low_played and
                          self._unmapCounter3 > 0):
                        self.mapscheme.miniSnippets(2, 'low with unmap 3')

                    elif (mini_motif_3_Low_played and
                          self._unmapCounter1 == 0 and
                          self._unmapCounter2 == 0):
                        self.mapscheme.miniSnippets(1, 'low amp')
                    elif (mini_motif_3_Low_played and
                          self._unmapCounter1 > 0 ):
                        self.mapscheme.miniSnippets(1, 'low amp with unmap 1')
                    elif (mini_motif_3_Low_played and
                          self._unmapCounter2 > 0 ):
                        self.mapscheme.miniSnippets(1, 'low amp with unmap 2')

            ### MID SECTION
            elif section == 'mid':
                if (note > self._pianosections[0] and
                    note <= self._pianosections[1]):
                    self.memorize(note, 9, False, 'Mid: ')

                    # see if motif_1 is played:
                    motif1_played = self.compare_chordal_motif(
                        self._memory, Motifs.get('motif_1'),
                        note, deltatime=self._deltatime, deltatolerance=0.005, debug=False)

                    if motif1_played and self._motif1_counter == 0:
                        self.mapscheme.snippets(1)
                        self._motif1_counter = 1

                    mini_motif_1_Mid_played = self.compare_motif(
                        self._memory, 'mini',
                        Motifs.get('mini_motif_1_mid'),
                        note, False)
                    mini_motif_2_Mid_played = self.compare_motif(
                        self._memory, 'mini2',
                        Motifs.get('mini_motif_2_mid'),
                        note, False)
                    mini_motif_3_Mid_played = self.compare_motif(
                        self._memory, 'mini3m',
                        Motifs.get('mini_motif_3_mid'),
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
                    elif (mini_motif_3_Mid_played and
                                          self._unmapCounter1 == 0 and
                                          self._unmapCounter2 == 0):
                        self.mapscheme.miniSnippets(3, 'mid') 
                    elif (mini_motif_3_Mid_played and
                          self._unmapCounter1 > 0):
                        self.mapscheme.miniSnippets(3, 'mid with unmap 1', )
                    elif (mini_motif_3_Mid_played and
                          self._unmapCounter2 > 0):
                        self.mapscheme.miniSnippets(3, 'mid with unmap 2')                        

            ### HI SECTION
            elif section == 'hi':
                if note > self._pianosections[1]:
                    self.memorize(note, 4, False, 'Hi: ')

                    mini_motif_1_Hi_played = self.compare_motif(
                        self._memory, 'mini',
                        Motifs.get('mini_motif_1_hi'),
                        note, False)
                    mini_motif_2_Hi_played = self.compare_motif(
                        self._memory, 'mini2',
                        Motifs.get('mini_motif_2_hi'),
                        note, False)

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

            ### TREMOLO
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

            elif section == 'tremoloLow':
                if note <= self._pianosections[0]:
                    self.memorize(note, 4, False, 'Tremolo Low: ')

                    if self.count_notes(self._memory, False) == 4 and len(self._memory) > 3:
                        self.tremolo_value(
                            [self._memory[2], self._memory[3]], 'low',
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

            ### FULL REGISTER
            elif section == 'full':
                # out of trouble enters for the codespace in case of getting stuck
                if note == 108:
                    self.mapscheme.mapping(note, 'Motippets')

                self.memorize(note, 20, False, 'Full-section Memory: ')

                # check if motif_2 is played:
                motif2_played = self.compare_chordal_motif(
                    self._memory, Motifs.get('motif_2'), note,
                    deltatime=self._deltatime, debug=False)
                if motif2_played:
                    if self._motif2_counter == 0:
                        self.mapscheme.snippets(2)
                        self._motif2_counter = 1

            ### CONDITIONALS SECTION

            #### CONDITIONAL 1
            elif section == 'conditional 1':

                if note <= self._pianosections[0]: ### LOW SECTION
                    self.memorize(note, 12, False, 'Conditional Memory: ')

                    if self._conditionalCounter == 0:
                        conditional2_played = self.compare_chordal_motif(
                            self._memory,
                            Motifs.get('conditional_1'),
                            note, 0, deltatime=self._deltatime, debug=False)

                        if conditional2_played:
                                    self.mapscheme.conditional(1)
                                    self._memory = []
                                    self._conditionalCounter += 1

                    if self._conditionalCounter > 0:
                        result3_played = self.compare_chordal_motif(self._memory,
                                                                    Motifs.get('conditional_result_3'),
                                                                    note, 1, self._deltatime, debug=False)

                        result4_played = self.compare_chordal_motif(self._memory,
                                                                    Motifs.get('conditional_result_4'),
                                                                    note, 2, self._deltatime, debug=False)

                        result5_played = self.compare_motif(self._memory, 'result 5',
                                                            Motifs.get('conditional_result_5'),
                                                            note, False)

                        if result3_played and self._resultCounter == 0:
                            self.mapscheme.result(3, 'comment')
                            self._conditionalsBuffer = []
                            self._resultCounter += 1
                            self._conditionalStatus = 3
                        elif result4_played and self._resultCounter == 0:
                            self.mapscheme.result(4, 'comment')
                            self._conditionalsBuffer = []
                            self._resultCounter += 1
                            self._conditionalStatus = 4
                        elif result5_played and self._resultCounter == 0:
                            self.mapscheme.result(5, 'comment')
                            self._conditionalsBuffer = []
                            self._resultCounter += 1
                            self._conditionalStatus = 5

                        return self._conditionalStatus


                if note > self._pianosections[1]: ### hi register
                    self.memorize(note, 20, False, 'Conditional Memory High: ')

                    result2_played = self.compare_motif(self._memory, 'result 2',
                                                        Motifs.get('conditional_result_2'),
                                                        note, False)

                    if result2_played and self._resultCounter == 0:
                        if self._conditionalCounter > 0:
                            self.mapscheme.result(2, 'comment')
                            self._conditionalsBuffer = []
                            self._resultCounter += 1
                            self._conditionalStatus = 2

                        return self._conditionalStatus

                if (note > self._pianosections[0] and note <= self._pianosections[1]):

                    self.memorize(note, 20, False, 'Conditional Memory Mid: ')

                    result1_played = self.compare_motif(self._memory, 'result 1',
                                                        Motifs.get('conditional_result_1'),
                                                        note, False)

                    if result1_played and self._resultCounter == 0:
                        if self._conditionalCounter > 0:
                            self.mapscheme.result(1, 'comment')
                            self._conditionalsBuffer = []
                            self._resultCounter += 1
                            self._conditionalStatus = 1

                        return self._conditionalStatus

                return self._conditionalStatus # is this needed with the isinstance check in the main loop?

            ### CONDITONAL 2
            elif section == 'conditional 2':

                if note <= self._pianosections[0]:
                    self.memorize(note, 20, False, 'Conditional 2 Memory: ') ## or 999 mem length?

                    if self._conditionalCounter == 0:
                        conditional_played = self.compare_motif(
                            self._memory,'conditional 2',
                            Motifs.get('conditional_2'),
                            note, False)

                        if conditional_played:
                            self.mapscheme.conditional(2)
                            self._memory = []
                            self._conditionalCounter += 1

                    if self._conditionalCounter > 0:
                        result3_played = self.compare_chordal_motif(self._memory,
                                                                    Motifs.get('conditional_result_3'),
                                                                    note, 1, self._deltatime, debug=False)

                        result4_played = self.compare_chordal_motif(self._memory,
                                                                    Motifs.get('conditional_result_4'),
                                                                    note, 2, self._deltatime, debug=False)

                        result5_played = self.compare_motif(self._memory, 'result 5',
                                                            Motifs.get('conditional_result_5'),
                                                            note, False)

                        if result3_played and self._resultCounter == 0:
                            self.mapscheme.result(3, 'comment')
                            self._conditionalsBuffer = []
                            self._resultCounter += 1
                            self._conditionalStatus = 3
                        elif result4_played and self._resultCounter == 0:
                            self.mapscheme.result(4, 'comment')
                            self._conditionalsBuffer = []
                            self._resultCounter += 1
                            self._conditionalStatus = 4
                        elif result5_played and self._resultCounter == 0:
                            self.mapscheme.result(5, 'comment')
                            self._conditionalsBuffer = []
                            self._resultCounter += 1
                            self._conditionalStatus = 5

                    return self._conditionalStatus

                if note > self._pianosections[1]:
                    self.memorize(note, 20, False, 'Conditional Memory High: ')

                    result2_played = self.compare_motif(self._memory, 'result 2',
                                                        Motifs.get('conditional_result_2'),
                                                        note, False)

                    if result2_played and self._resultCounter == 0:
                        if self._conditionalCounter > 0:
                            self.mapscheme.result(2, 'comment')
                            self._conditionalsBuffer = []
                            self._resultCounter += 1
                            self._conditionalStatus = 2

                        return self._conditionalStatus

                if (note > self._pianosections[0] and note <= self._pianosections[1]):

                        self.memorize(note, 20, False, 'Conditional Memory Mid: ')

                        result1_played = self.compare_motif(self._memory, 'result 1',
                                                            Motifs.get('conditional_result_1'),
                                                            note, False)

                        if result1_played and self._resultCounter == 0:
                            if self._conditionalCounter > 0:
                                self.mapscheme.result(1, 'comment')
                                self._conditionalsBuffer = []
                                self._resultCounter += 1
                                self._conditionalStatus = 1

                            return self._conditionalStatus

                return self._conditionalStatus

            ### CONDITONAL 3
            elif section == 'conditional 3':

                if note > self._pianosections[1]:
                    self.memorize(note, 20, False, 'Conditional 3 Memory Hi: ')

                    if self._conditionalCounter == 0:
                        conditional_played = self.compare_motif(
                            self._memory,'conditional 3',
                            Motifs.get('conditional_3'),
                            note, False)

                        if conditional_played:
                            self.mapscheme.conditional(3)
                            self._memory = []
                            self._conditionalCounter += 1

                    if self._conditionalCounter > 0:

                        result2_played = self.compare_motif(self._memory, 'result 2',
                                                            Motifs.get('conditional_result_2'),
                                                            note, False)

                        if result2_played and self._resultCounter == 0:
                            if self._conditionalCounter > 0:
                                self.mapscheme.result(2, 'comment')
                                self._conditionalsBuffer = []
                                self._resultCounter += 1
                                self._conditionalStatus = 2

                            return self._conditionalStatus

                if note <= self._pianosections[0]:
                    self.memorize(note, 20, False, 'Conditional 3 Memory: ')

                    if self._conditionalCounter > 0:
                        result3_played = self.compare_chordal_motif(self._memory,
                                                                    Motifs.get('conditional_result_3'),
                                                                    note, 0, self._deltatime, 0.01, False)

                        result4_played = self.compare_chordal_motif(self._memory,
                                                                    Motifs.get('conditional_result_4'),
                                                                    note, 1, self._deltatime, 0.01, False)

                        result5_played = self.compare_motif(self._memory, 'result 5',
                                                            Motifs.get('conditional_result_5'),
                                                            note, False)

                        if result3_played and self._resultCounter == 0:
                            self.mapscheme.result(3, 'comment')
                            self._conditionalsBuffer = []
                            self._resultCounter += 1
                            self._conditionalStatus = 3
                        elif result4_played and self._resultCounter == 0:
                                    self.mapscheme.result(4, 'comment')
                                    self._conditionalsBuffer = []
                                    self._resultCounter += 1
                                    self._conditionalStatus = 4
                        elif result5_played and self._resultCounter == 0:
                            self.mapscheme.result(5, 'comment')
                            self._conditionalsBuffer = []
                            self._resultCounter += 1
                            self._conditionalStatus = 5

                        return self._conditionalStatus

                if (note > self._pianosections[0] and note <= self._pianosections[1]):
                    self.memorize(note, 20, False, 'Conditional Memory Mid: ')

                    result1_played = self.compare_motif(self._memory, 'result 1',
                                                        Motifs.get('conditional_result_1'),
                                                        note, False)

                    if result1_played and self._resultCounter == 0:
                        if self._conditionalCounter > 0:
                            self.mapscheme.result(1, 'comment')
                            self._conditionalsBuffer = []
                            self._resultCounter += 1
                            self._conditionalStatus = 1

                        return self._conditionalStatus

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
                    self._unmapCounter3 = 0
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

    def compare_chordal_motif(self, array, motif, note, num=0, deltatime=0, deltatolerance=0.005, debug=False):
        """Compare chordal motifs

        i.e. MIDI note order doesn't matter

        TODO: describe input/output params
        TODO 2: make sub arrays if function is used again...
        """
        compare = False
        if num == 0:
            if note in motif:
                self._mainMotifs.append(note)
                self._deltaHelper.append(deltatime)
            else:
                self._mainMotifs = []
                self._deltaHelper = []

            if len(self._mainMotifs) >= len(motif):
                self._mainMotifs = self._mainMotifs[-len(motif):]
                self._deltaHelper = self._deltaHelper[-(len(motif)-1):]

                sum_motif = reduce(
                    (lambda total, sumnotes: total + sumnotes),
                    motif)
                sum_played = reduce(
                    (lambda total, sumnotes: total + sumnotes),
                    self._mainMotifs)
                dif_delta = reduce( (lambda total, sumtimes: (total +
                                                              sumtimes) / len( self._deltaHelper) ), self._deltaHelper)
                #print('average: ', dif_delta)

                if sum_motif == sum_played and (dif_delta < deltatolerance and dif_delta > 0):
                    compare = True

                    if debug:
                        print('played ->' + str(self._mainMotifs),
                              '\nmotif ->' + str(motif),
                              '\ncomparison: ' + str(compare),
                              '\nsum played: ' + str(sum_played),
                              '\nsum motif: ' + str(sum_motif),
                              '\ndelta average: ', dif_delta)
        elif num == 1:
            if note in motif:
                self._mainMotifs1.append(note)
                self._deltaHelper1.append(deltatime)
            else:
                self._mainMotifs1 = []
                self._deltaHelper1 = []

            if len(self._mainMotifs1) >= len(motif):
                self._mainMotifs1 = self._mainMotifs1[-len(motif):]
                self._deltaHelper1 = self._deltaHelper1[-(len(motif)-1):]

                sum_motif = reduce(
                    (lambda total, sumnotes: total + sumnotes),
                    motif)
                sum_played = reduce(
                    (lambda total, sumnotes: total + sumnotes),
                    self._mainMotifs1)
                dif_delta = reduce(
                     (lambda total, sumtimes: (total + sumtimes) / len(self._deltaHelper1)), self._deltaHelper1)
                if sum_motif == sum_played and (dif_delta < deltatolerance and dif_delta > 0):
                    compare = True

                    if debug:
                        print('played ->' + str(self._mainMotifs1),
                              '\nmotif ->' + str(motif),
                              '\ncomparison: ' + str(compare),
                              '\nsum played: ' + str(sum_played),
                              '\nsum motif: ' + str(sum_motif),
                              '\ndelta average: ', dif_delta)

        else:
            if note in motif:
                self._mainMotifs2.append(note)
                self._deltaHelper2.append(deltatime)
            else:
                self._mainMotifs2 = []
                self._deltaHelper2 = []

            if len(self._mainMotifs2) >= len(motif):
                self._mainMotifs2 = self._mainMotifs2[-len(motif):]
                self._deltaHelper2 = self._deltaHelper2[-(len(motif)-1):]

                sum_motif = reduce(
                    (lambda total, sumnotes: total + sumnotes),
                    motif)
                sum_played = reduce(
                    (lambda total, sumnotes: total + sumnotes),
                    self._mainMotifs2)
                dif_delta = reduce( (lambda total, sumtimes: (total +
                                                              sumtimes) / len( self._deltaHelper2)), self._deltaHelper2)

                if sum_motif == sum_played and (dif_delta < deltatolerance and dif_delta > 0):
                    compare = True

                    if debug:
                        print('played_1 ->' + str(self._mainMotifs2),
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
        :param int target: integer that references the targeted snippet
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
                    if pianosection == 'hi':
                        if target == 1:
                            self.mapscheme.tremolo('hi_1', interval)
                        elif target == 2:
                            self.mapscheme.tremolo('hi_2', interval)
                    elif pianosection == 'mid':
                        if target == 1:
                            self.mapscheme.tremolo('mid_1', interval)
                        elif target == 2:
                            self.mapscheme.tremolo('mid_2', interval)
                        elif target == 3:
                            self.mapscheme.tremolo('mid_3', interval)                            
                    elif pianosection == 'low':
                        if target == 1:
                            self.mapscheme.tremolo('low_1', interval)
                        elif target == 2:
                            self.mapscheme.tremolo('low_2', interval)
                        elif target == 3:
                            self.mapscheme.tremolo('low_3', interval)
                    elif pianosection == 'full':
                        return interval

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
