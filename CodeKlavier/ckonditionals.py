"""
Functions that handle CK conditional constructs.
"""
import time
import random
import configparser
from CK_Setup import BColors
from CK_config import inifile
from threading import Thread, Event

threads_are_perpetual = True
param_interval = 0
range_trigger = 0
notecounter = {}
stop_midi = False

config = configparser.ConfigParser()
config.read(inifile, encoding='utf8')

def rangeCounter(timer=None, operator='', motif_name=None, result_name=None,
                 piano_range=72, debug=False, perpetual=True, mapping=None,
                 conditional=None, rangeParser=None, mainmotifs=None):
    """
    Calculate the played range within a time window. Perpetual flag makes it run it's loop forever, unless range_trigger is != 1

    :param timer: time window loop or 'random'
    :param operator: 'more than' or 'less than'
    :param str num: the name of the conditional motif
    :param str result_num: the name of the result motif
    :param int piano_range: total range for evvaluation in semitones
    :param bool debug: booelan flag to post debug messages
    :param bool perpetual: boolean flag to make the function loop infinetly or 1 shot ## reserved for future versions
    :param obj mapping: an instance of a Mapping class
    :param obj mapping: an instance of a Motippets class
    :param obj mapping: an instance of a Motippets class dealing with the piano range
    :param obj mainmotifs: an instance of a Motippets class dealing witht he main motifs
    """

    global range_trigger, threads_are_perpetual, param_interval
    conditional._conditionalStatus = None #reset trigger

    t = 1
    param_interval = 0
    rangeParser_memory = []
    syntax_colors = {'conditional_1': 'loop', 'conditional_2': 'loop2', 'conditional_3': 'loop3', 
                     'conditional_4': 'loop', 'conditional_5': 'loop2'}
    if timer in config['motippets random limits']:
        rand_limits = [float(l) for l in config['motippets random limits'].get(timer).split(',')]

    if timer == 'random':
        timer = random.randrange(rand_limits[0],rand_limits[1])

    if debug:
        print('thread for range started')
        print("range trig -> ", range_trigger, "result num: ", result_name, "range set to: ", piano_range)

    if perpetual:
        threads_are_perpetual = True
            
        while threads_are_perpetual:
            if debug:
                print('cond', motif_name, 'res', result_name, 'timer: ', timer - t, 'loop time: ', timer)
                if timer == t+1:
                    mapping.customPass('conditional looptime: ' + str(timer - t) + '', syntax_colors[motif_name],
                                       display_only=True, flash=True, display=4)
                else:
                    mapping.customPass('conditional looptime: ' + str(timer - t) + '', syntax_colors[motif_name], display_only=True, display=4)
    
            rangeParser._timer += 1
            t += 1
    
            if t % timer == 0:
                if debug:
                    print("Range conditional thread finished")
                    print("range was: ", rangeParser._range)
                if operator == 'more than':
                    if rangeParser._range >= piano_range:
                        parseFlags(result_name, 'true', rangeParser._range, mapping, mainmotifs, conditional)
                    else:
                        parseFlags(result_name, 'false', rangeParser._range, mapping, mainmotifs, conditional)
                    #else:
                        #mapping.customPass('condition not met', ':(')
    
                elif operator == 'less than':
                    if rangeParser._range <= piano_range:
                        parseFlags(result_name, 'true', rangeParser._range, mapping, mainmotifs, conditional)
                    else:
                        parseFlags(result_name, 'false', rangeParser._range, mapping, mainmotifs, conditional)
    
                # reset states:
                rangeParser._memory = []
                conditional._conditionalCounter = 0
                conditional._resultCounter = 0
                #conditionals[motif_name]._conditionalCounter = 0
                #conditionals[motif_name]._resultCounter = 0
                rangeParser._timer = 0
                t = 0
    
            time.sleep(1)
    else:
        for s in range(0, timer):
                
            if debug:
                print('cond', motif_name, 'res', result_name, 'timer: ', timer - t, 'loop time: ', timer)
                if timer == t+1:
                    mapping.customPass('conditional looptime: ' + str(timer - t) + '', syntax_colors[motif_name],
                                       display_only=True, flash=True, display=4)
                else:
                    mapping.customPass('conditional looptime: ' + str(timer - t) + '', syntax_colors[motif_name], display_only=True, display=4)
    
            rangeParser._timer += 1
            t += 1
    
            if t % timer == 0:
                if debug:
                    print("Range conditional thread finished")
                    print("range was: ", rangeParser._range)
                if operator == 'more than':
                    if rangeParser._range >= piano_range:
                        parseFlags(result_name, 'true', rangeParser._range, mapping, mainmotifs, conditional)
                    else:
                        parseFlags(result_name, 'false', rangeParser._range, mapping, mainmotifs, conditional)
                    #else:
                        #mapping.customPass('condition not met', ':(')
    
                elif operator == 'less than':
                    if rangeParser._range <= piano_range:
                        parseFlags(result_name, 'true', rangeParser._range, mapping, mainmotifs, conditional)
                    else:
                        parseFlags(result_name, 'false', rangeParser._range, mapping, mainmotifs, conditional)
    
                # reset states:
                rangeParser._memory = []
                conditional._conditionalCounter = 0
                conditional._resultCounter = 0
                #conditionals[motif_name]._conditionalCounter = 0
                #conditionals[motif_name]._resultCounter = 0
                rangeParser._timer = 0
                t = 0    
                
            time.sleep(1)

def parseFlags(snippet_name, boolean, value, mapping, mainmotifs, conditional):
    """
    function to parse any optional flags set in the .ini file for the passed motif-snippet

    :param str snippet_name: the motif name corresponding to the snippet
    :param str boolean: true or false
    :param any value: pipped value from the parent function
    :param obj mapping: an instance of a Motippets class
    :param obj mainmotifs: an instance of a Motippets class dealing witht the main motifs
    :param obj conditional: an instance of a Motippets class dealing witht the conditional motifs
    """
    global threads_are_perpetual

    flags = [r.strip() for r in config['snippets code output'].get(snippet_name+'_'+boolean).split(',')]

    if snippet_name in config['snippets special flags']:
        special_flags = [r.strip() for r in config['snippets special flags'].get(snippet_name+'_'+boolean).split(',')]

        if 'reset' in special_flags:
            mainmotifs._motifsCount[flags[2]]['count'] = 0

    if 'gomb' in flags:
        mapping.result(snippet_name, boolean, flags='gomb')
        gomb = Thread(target=gong_bomb, name='gomb', args=(value, snippet_name, conditional, mapping, True))
        gomb.start()

    else:
        if 'grab_value' in flags:
            if len(flags) > 3:
                if flags[4] in config['motippets random limits']:
                    rand_limits = [float(l) for l in config['motippets random limits'].get(flags[4]).split(',')]
                    mapping.result(snippet_name, boolean, random.uniform(rand_limits[0], rand_limits[1]))
                else:
                    mapping.result(snippet_name, boolean, value)
        else:
            if 'loop_stop' in flags:
                threads_are_perpetual = False
            mapping.result(snippet_name, boolean)


def set_parameters(value, conditional_func, mapping=None, parameters=None, ini_param=None, debug=False):
    """
    function to parse a full range tremolo. This value can be used as a param for the
    other functions.

    :param int value: the interval of the plated tremolo
    :param conditional_func: the type of conditional (from built-in types)
    :param obj mapping: an instance of a Mapping class
    :param obj mapping: an instance of a Motippets class dealing with parameters parsing
    :param bool debug: run in debug mode
    """
    global param_interval, range_trigger
    #mapping
    print('thread started for parameter set', 'func:', conditional_func)

    if conditional_func == 'note_count':
        mapping.customPass('more than ' + str(ini_param) + ' notes played in the next ' + str(value) + ' seconds?', flash=True)
    elif conditional_func in ('range_more_than', 'range_less_than'):
        mapping.customPass('range set to: ' + str(value) + ' semitones...', flash=True)
    elif conditional_func == 'gomb':
        mapping.customPass('GOMB countdown set to: ' + str(value), flash=True)

    if debug:
        print('value parameter is ', str(value))

    param_interval = value
    parameters._interval = 0
    #time.sleep(1) # check if the sleep is needed...
    range_trigger = 1

def noteCounter(timer=10, numberOfnotes=100, result_name=None, debug=True, mapping=None,
                conditional=None, mainmotifs=None, perpetual=False):
    """
    Fucntion that counts the numberOfNotes within the timer window

    :param int timer: Total seconds for countdown timer
    :param int numberOfnotes: Minimum nomber of notes to pass the conditional
    :param int result_name: corresponding result_name motif
    :param bool debug: print debug messages
    :param obj mapping: an instance of a Mapping class
    :param obj conditional: an instance of a Motippets class
    :param obj mainmotifs: an instance of a Motippets class dealing witht he main motifs
    :param bool perpetual: boolean flag to make the function loop infinetly or 1 shot ## reserved for future versions
    """
    global param_interval, threads_are_perpetual, notecounter

    print('thread started for result', result_name, 'number of notes:', numberOfnotes)

    conditional._conditionalCounter = 0
    conditional._resultCounter = 0
    conditional._conditionalStatus = None

    param_interval= 0

    if perpetual:
        threads_are_perpetual = True

        while threads_are_perpetual:
            conditional._noteCounter = 0
            for s in range(0, timer):

                if not threads_are_perpetual:
                    break

                if conditional._noteCounter > numberOfnotes:
                    mapping.customPass('Total notes played: ' + str(conditional._noteCounter)+'!!!')
                    parseFlags(result_name, 'true', timer, mapping, mainmotifs, conditional)
                    break
                else:
                    mapping.customPass('notes played: ' + str(conditional._noteCounter), display_only=True, display=4)

                if debug:
                    print(result_name, conditional._noteCounter)
                time.sleep(1)

            if conditional._noteCounter < numberOfnotes:
                parseFlags(result_name, 'false', timer, mapping, mainmotifs, conditional)

    else:
        for s in range(0, timer):
            if conditional._noteCounter > numberOfnotes:
                mapping.customPass('Total notes played: ' + str(conditional._noteCounter)+'!!!')

                parseFlags(result_name, 'true', timer, mapping, mainmotifs, conditional)
                break
            else:
                mapping.customPass('notes played: ' + str(conditional._noteCounter), display_only=True, display=4)

            if debug:
                print(result_name, conditional._noteCounter)
            time.sleep(1)

        if conditional._noteCounter < numberOfnotes:
            parseFlags(result_name, 'false', timer, mapping, mainmotifs, conditional)


def gong_bomb(countdown, result_name, conditional, mapping, debug=False):
    """
    function to kill all running processes and finish the piece with a gong bomb. i.e. a GOMB!

    :param int countdown: Total seconds for countdown timer
    :param int result_name: corresponding result_name motif
    :param bool debug: print debug messages
    :param obj conditional: an instance of a Mapping class
    :param obj conditional: an instance of a Motippets class
    """
    global param_interval, threads_are_perpetual, stop_midi
    param_interval= 0
    conditional._conditionalStatus = 0
    conditional._resultCounter = 0
    conditional._conditionalCounter = 0

    if debug:
        print('gong bomb thread started', 'countdown: ', countdown)

    for g in range(0, countdown):

        #if not stop_midi:
            #break

        countdown -= 1
        print(BColors.FAIL + str(countdown) + BColors.ENDC)
        mapping.customPass(str(countdown), 'warning')

        if countdown == 0:
            threads_are_perpetual = False #stop all perpetual threads
            stop_midi = False #stop listening for MIDI input

            #stop all snippets
            mapping.result(result_name, 'true')
            time.sleep(0.2)
            print("")
            print(BColors.WARNING + "  ____   ____   ____  __  __ _ ")
            print(" |  _ \ / __ \ / __ \|  \/  | |")
            print(" | |_) | |  | | |  | | \  / | |")
            print(" |  _ <| |  | | |  | | |\/| | |")
            print(" | |_) | |__| | |__| | |  | |_|")
            print(" |____/ \____/ \____/|_|  |_(_)" + BColors.ENDC)
            print("")
            mapping.gomb()

        time.sleep(1)
