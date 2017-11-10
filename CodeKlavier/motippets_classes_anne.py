"""
classes for Motippets.
Second prototype of the CodeKlavier

"""
import rtmidi
from functools import reduce
from .Motifs import Motifs_Anne

# class to handle the midi input
class Motippets(object):
    def __init__(self, port, mapping, noteonid):
        self.port = port
        self.mapscheme = mapping
        self.noteonid = noteonid
        self.__memory = []
        self.__mainMotifs = []
        self.__miniMotifs = []
        self.__miniMotifs2 = []
        self.__pianosectons = [47, 78, 108]
        self.__motif1_counter = 0
        self.__motif2_counter = 0
        self.__motif1_played = False #maybe not needed
        self.__intervalsArray = []
        self.__unmapCounter1 = 0
        self.__unmapCounter2 = 0
        #TODO: make a variable self._motifs = Motifs_Anne and use it throughout
        # the class. This makes it easier to switch between motifs and it is
        # less error prone.

    def parse_midi(self, event, section):
        message, deltatime = event
        if message[2] > 0: #only noteOn

            if (message[0] == 176): #pedal stop (TODO: handle in Mapping class!)
                note = message[1]
                self.mapscheme.mapping(note)

            if (message[0] == self.noteonid):
                note = message[1]

                if section == 'low':
                    if note <= self.__pianosectons[0]:
                        self.memorize(note, 20, True, 'Low: ')



                        mini_motif_1_Low_played = self.compareMotif(self.__memory, 'mini', Motifs_Anne().mini_motif_1_low(), note, True)
                        mini_motif_2_Low_played = self.compareMotif(self.__memory, 'mini2', Motifs_Anne().mini_motif_2_low(), note, True)

                        if mini_motif_1_Low_played and self.__unmapCounter2 == 0:
                            self.mapscheme.miniSnippets(1, 'low')
                        elif mini_motif_1_Low_played and self.__unmapCounter2 > 0:
                            self.mapscheme.miniSnippets(1, 'low with unmap')
                        elif mini_motif_2_Low_played and self.__unmapCounter1 == 0:
                            self.mapscheme.miniSnippets(2, 'low')
                        elif mini_motif_2_Low_played and self.__unmapCounter1 > 0:
                            self.mapscheme.miniSnippets(2, 'low with unmap')


                elif section == 'mid':
                    if note > self.__pianosectons[0] and note <= self.__pianosectons[1]:
                        self.memorize(note, 20, False, 'Mid: ')

                        # see if motif_1 is played:
                        motif1_played = self.compareChordalMotif(self.__memory, Motifs_Anne().motif_1(), note, True)
                        if motif1_played:
                            if self.__motif1_counter == 0:
                                self.mapscheme.snippets(1)
                                self.__motif1_counter = 1
                        mini_motif_1_Mid_played = self.compareMotif(self.__memory, 'mini', Motifs_Anne().mini_motif_1_mid(), note, False)
                        mini_motif_2_Mid_played = self.compareMotif(self.__memory, 'mini2', Motifs_Anne().mini_motif_2_mid(), note, False)

                        #if self.__motif1_played: ??? make a delegate?
                        if mini_motif_1_Mid_played and self.__unmapCounter2 == 0:
                            self.mapscheme.miniSnippets(1, 'mid')
                        elif mini_motif_1_Mid_played and self.__unmapCounter2 > 0:
                            self.mapscheme.miniSnippets(1, 'mid with unmap')
                        elif mini_motif_2_Mid_played and self.__unmapCounter1 == 0:
                            self.mapscheme.miniSnippets(2, 'mid')
                        elif mini_motif_2_Mid_played and self.__unmapCounter1 > 0:
                            self.mapscheme.miniSnippets(2, 'mid with unmap')


                elif section == 'hi':
                    if note > self.__pianosectons[1]:
                        self.memorize(note, 20, True, 'Hi: ')

                        mini_motif_1_Hi_played = self.compareMotif(self.__memory, 'mini', Motifs_Anne().mini_motif_1_hi(), note, True)
                        mini_motif_2_Hi_played = self.compareMotif(self.__memory, 'mini2', Motifs_Anne().mini_motif_2_hi(), note, True)

                        if mini_motif_1_Hi_played and self.__unmapCounter2 == 0:
                            self.mapscheme.miniSnippets(1, 'hi')
                        elif mini_motif_1_Hi_played and self.__unmapCounter2 > 0:
                            self.mapscheme.miniSnippets(1, 'hi with unmap')
                        elif mini_motif_2_Hi_played and self.__unmapCounter1 == 0:
                            self.mapscheme.miniSnippets(2, 'hi')
                        elif mini_motif_2_Hi_played and self.__unmapCounter1 > 0:
                            self.mapscheme.miniSnippets(2, 'hi with unmap')

                elif section == 'tremoloHi':
                    if note > self.__pianosectons[1]:
                        self.memorize(note, 4, False, 'Tremolo Hi: ')

                        if self.countNotes(self.__memory, False) == 4:
                            self.tremoloValue([self.__memory[2], self.__memory[3]], 'hi', deltatime, 0.1, False)

                elif section == 'tremoloMid':
                    if note > self.__pianosectons[0] and note <= self.__pianosectons[1]:
                        self.memorize(note, 4, False, 'Tremolo Mid: ')

                        if self.countNotes(self.__memory, False) == 4:
                            self.tremoloValue([self.__memory[2], self.__memory[3]], 'mid', deltatime, 0.1, False)

                elif section == 'tremoloLow':
                    if note <= self.__pianosectons[0]:
                        self.memorize(note, 4, False, 'Tremolo Low: ')

                        if self.countNotes(self.__memory, False) == 4:
                            self.tremoloValue([self.__memory[2], self.__memory[3]], 'low', deltatime, 0.1, False)
                else:
                    #memorize the last 20 notes of the complete register:
                    self.memorize(note, 20, False, 'Main Memory: ')

                    # see if motif_2 is played:
                    motif2_played = self.compareChordalMotif(self.__memory, Motifs_Anne().motif_2(), note, False)
                    if motif2_played:
                        if self.__motif2_counter == 0:
                            self.mapscheme.snippets(2)
                            self.__motif2_counter = 1


# store the incoming midi notes
    def memorize(self, midinote, length, debug, debugname):
        # append incoming midinotes to the memory array
        self.__memory.append(midinote)

        if len(self.__memory) > length:
            self.__memory = self.__memory[-length:]

        if debug == True:
            print(debugname + ','.join(map(str, self.__memory)))

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
                self.__miniMotifs.append(note)
            else:
                self.__miniMotifs = []

            if len(self.__miniMotifs) >= len(motif):
                self.__miniMotifs = self.__miniMotifs[-len(motif):]
                if self.__miniMotifs == motif:
                    compare = True
                    self.__unmapCounter1 += 1
                else:
                    compare = False

                if debug == True:
                    print('played ->' + str(self.__miniMotifs), '\nmotif ->' + str(motif), '\ncomparison: ' + str(compare))

                return compare

        elif motiftype == 'mini2':
            if note in motif:
                self.__miniMotifs2.append(note)
            else:
                self.__miniMotifs2 = []

            if len(self.__miniMotifs2) >= len(motif):
                self.__miniMotifs2 = self.__miniMotifs2[-len(motif):]
                if self.__miniMotifs2 == motif:
                    compare = True
                    self.__unmapCounter2 += 1
                else:
                    compare = False

                if debug == True:
                    print('played ->' + str(self.__miniMotifs2), '\nmotif 2 ->' + str(motif), '\ncomparison: ' + str(compare))

                return compare
        else:
            if note in motif:
                self.__mainMotifs.append(note)
            else:
                self.__mainMotifs = []

            if len(self.__mainMotifs) >= len(motif):
                self.__mainMotifs = self.__mainMotifs[-len(motif):]
                if self.__mainMotifs == motif:
                    compare = True
                else:
                    compare = False

                if debug == True:
                    print('played ->' + str(self.__mainMotifs), '\nbig motif ->' + str(motif), '\ncomparison: ' + str(compare))

                return compare

# compate chordal motifs (i.e. MIDI note order doesn't matter)
    def compareChordalMotif(self, array, motif, note, debug):
        if note in motif:
            self.__mainMotifs.append(note)
        else:
            self.__mainMotifs = []

        if len(self.__mainMotifs) >= len(motif):
            self.__mainMotifs = self.__mainMotifs[-len(motif):]
            sum_motif = reduce((lambda total, sumnotes: total + sumnotes), motif)
            sum_played = reduce((lambda total, sumnotes: total + sumnotes), self.__mainMotifs)
            if sum_motif == sum_played:
                compare = True
            else:
                compare = False

            if debug == True:
                print('played ->' + str(self.__mainMotifs), '\nmotif ->' + str(motif), '\ncomparison: ' + str(compare), '\nsum played: ' + str(sum_played),
                      '\nsum motif: ' + str(sum_motif))

            return compare

# get the interval of a given tremolo
    def tremoloValue(self, notes, pianosection, deltatime, deltatolerance, debug):
        if deltatime < deltatolerance:
            interval = abs(notes[1]-notes[0])
            self.__intervalsArray.append(interval)
            self.__intervalsArray = self.__intervalsArray[-2:]

            #print('intervals array: ' + str(self.__intervalsArray))
            interval_reduce = reduce((lambda total, sumnotes: total - sumnotes), self.__intervalsArray)

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
