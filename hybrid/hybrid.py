#!/usr/bin/env python3

import configparser
import getopt
import sys
import time
import random
from threading import Thread, Event

import CK_configWriter
from CK_Setup import Setup, BColors
from Mapping import *
from motippets_classes import Motippets
from hello_classes import HelloWorld

#globals
config = configparser.ConfigParser()
config.read('default_setup.ini')

try:
    myPort = config['midi'].getint('port')
    device_id = config['midi'].getint('device_id')
    noteoff_id = config['midi'].getint('noteoff_id')
except KeyError:
    raise LookupError('Missing key information in the config file.')

if (myPort == None or device_id == None):
    raise LookupError('Missing key information in the config file.')

# activesense compensation
ck_deltatime_mem = []
ck_deltatime = 0
ck_deltadif = 0

#multiprocessing vars
threads = {}
notecounter = 0
range_trigger = 0
param_interval = 0
threads_are_perpetual = True
motippets_is_listening = True
keep_main_alive = True

def rangeCounter(timer='', operator='', num=1, result_num=1, piano_range=72, debug=True, perpetual=True):
    """
    Calculate the played range within a time window. Perpetual flag makes it run it's loop forever, unless range_trigger is != 1

    :param timer: time window loop
    :param operator: 'more than' or 'less than'
    :param int num: conditional number
    :param int result_num: result number mapped to this conditional
    :param int piano_range: total range for evvaluation in semitones
    :param bool debug: booelan flag to post debug messages
    :param bool perpetual: boolean flag to make the function loop infinetly or 1 shot ## reserved for future versions
    """

    global range_trigger, threads_are_perpetual, param_interval, mapping
    conditionals[num]._conditionalStatus = 0 #reset trigger
    t = 1
    param_interval = 0

    if debug:
        print('thread for range started')
        print("range trig -> ", range_trigger, "result num: ", result_num, "range set to: ", piano_range)


    while threads_are_perpetual:
        if timer == 'random':
            timer = random.randrange(10,45)

        if debug:
            print('cond', num, 'res', result_num, 'timer: ', timer - t, 'loop time: ', timer)
            #mapping.onlyDisplay('cond: ' + str(num) + ' result: ' + str(result_num) + ' looptime: ' + str(timer - t) + '', num)
            mapping.onlyDisplay('conditional looptime: ' + str(timer - t) + '', num)
            #print('Range conditional memory: ', conditionalsRange._memory)
        conditionalsRange._timer += 1
        t += 1

        if t % timer == 0:
            if debug:
                print("Range conditional thread finished")
                print("range was: ", conditionalsRange._range)
            if operator == 'more than':
                if conditionalsRange._range >= piano_range:
                    if result_num == 1:
                        mapping.result(result_num,'code')
                        mainMem._motif2_counter = 0
                        conditionalsRange._memory = []
                        conditionals[num]._conditionalCounter = 0
                        conditionals[num]._resultCounter = 0
                        conditionalsRange._timer = 0
                        break; #stop thread if condition met
                    elif result_num == 2:
                        mapping.result(result_num, 'code')
                        memMid._motif1_counter = 0
                        conditionalsRange._memory = []
                        conditionals[num]._conditionalCounter = 0
                        conditionals[num]._resultCounter = 0
                        conditionalsRange._timer = 0
                        break;
                    elif result_num == 3:
                        mapping.result(result_num, 'code', piano_range) #pass the piano range int as a modulation parameter for the sound synthesis
                    elif result_num == 4:
                        mapping.result(4, 'start')
                        gomb = Thread(target=gong_bomb, name='gomb', args=(piano_range, True))
                        gomb.start()
                    elif result_num == 5:
                        mapping.result(result_num, 'code', piano_range)
                #else:
                    #mapping.customPass('condition not met', ':(')

            elif operator == 'less than':
                if conditionalsRange._range <= piano_range:
                    if result_num == 1:
                        mapping.result(result_num,'code')
                        mainMem._motif2_counter = 0
                        conditionalsRange._memory = []
                        conditionals[num]._conditionalCounter = 0
                        conditionals[num]._resultCounter = 0
                        conditionalsRange._timer = 0
                        break
                    elif result_num == 2:
                        mapping.result(result_num, 'code')
                        memMid._motif1_counter = 0
                        conditionalsRange._memory = []
                        conditionals[num]._conditionalCounter = 0
                        conditionals[num]._resultCounter = 0
                        conditionalsRange._timer = 0
                        break;
                    elif result_num == 3:
                        mapping.result(result_num, 'code', piano_range)
                    elif result_num == 4:
                        mapping.result(4, 'start')
                        gomb = Thread(target=gong_bomb, name='gomb', args=(piano_range, True))
                        gomb.start()
                    elif result_num == 5:
                        mapping.result(result_num, 'code', piano_range)
                #else:
                    #mapping.customPass('condition not met', ':(')


            # reset states:
            conditionalsRange._memory = []
            conditionals[num]._conditionalCounter = 0
            conditionals[num]._resultCounter = 0
            conditionalsRange._timer = 0
            t = 0

        time.sleep(1)


def set_parameters(value, conditional_func, debug=False):
    """
    function to parse a full range tremolo. This value can be used as a param for the
    other functions.

    :param int value: the interval of the plated tremolo
    :param conditional_func: todo
    :param bool debug: run in debug mode
    """
    global param_interval, range_trigger, mapping
    print('thread started for parameter set')

    if conditional_func == 'amount':
        mapping.customPass('more than 100 notes played in the next ', str(value) + ' seconds?')
    elif conditional_func == 'range':
        mapping.customPass('range set to: ', str(value) + ' semitones...')
    elif conditional_func == 'gomb':
        mapping.customPass('GOMB countdown set to: ', str(value))

    if debug:
        print('value parameter is ', str(value))

    param_interval = value
    parameters._interval = 0
    time.sleep(1) # check if the sleep is needed...
    range_trigger = 1

def noteCounter(timer=10, numberOfnotes=100, result_num=1, debug=True):
    """
    TODO: define func

    :param int timer: todo
    :param int numberOfnotes: todo
    :param int result_num: todo
    :param bool debug: run in debug mode
    """
    print('thread started for result ', result_num, 'number of notes: ', numberOfnotes)

    #reset parameter global once it has passed effectively:
    global param_interval, mapping, notecounter
    param_interval= 0

    for s in range(0, timer):
        if notecounter > numberOfnotes:
            mapping.customPass('Total notes played: ', str(notecounter)+'!!!')

            if result_num == 1:
                mapping.result(result_num, 'code')
                mainMem._motif2_counter = 0 #reset the motif counter so it can be played again...

            elif result_num == 2: #this is for snippet 1 - change the names accordingly
                mapping.result(result_num, 'code')
                memMid._motif1_counter = 0

            elif result_num == 3:
                mapping.result(result_num, 'code', round(notecounter*random.uniform(-2, 10)))

            elif result_num == 4:
                mapping.result(4, 'start')
                gomb = Thread(target=gong_bomb, name='gomb', args=(timer, True))
                gomb.start()

            elif result_num == 5:
                mapping.result(result_num, 'code', random.randint(1, 80))

            break
        else:
            mapping.customPass('notes played: ', str(notecounter))
            conditionals[1]._conditionalStatus = 0
            conditionals[1]._resultCounter = 0
            conditionals[1]._conditionalCounter = 0

        if debug:
            print(notecounter)
        time.sleep(1)

def gong_bomb(countdown, debug=False):
    """
    function to kill all running processes and finish the piece with a gong bomb. i.e. a GOMB!

    countdown: the countdown time in seconds
    """
    #reset parameter global once it has passed effectively:
    global param_interval, threads_are_perpetual, mapping
    param_interval= 0
    conditionals[1]._conditionalStatus = 0
    conditionals[1]._resultCounter = 0
    conditionals[1]._conditionalCounter = 0

    if debug:
        print('gong bomb thread started', 'countdown: ', countdown)

    for g in range(0, countdown):
        countdown -= 1
        print(BColors.FAIL + str(countdown) + BColors.ENDC)
        mapping.onlyDisplay(str(countdown), warning=True)

        if countdown == 0: #boom ASCII idea by @borrob!
            threads_are_perpetual = False #stop all perpetual threads
            motippets_is_listening = False #stop listening for input
            #stop all snippets
            mapping.result(4, 'huygens')
            mapping.result(1, 'code')
            mapping.result(2, 'code')
            print("")
            print(BColors.WARNING + "  ____   ____   ____  __  __ _ ")
            print(" |  _ \ / __ \ / __ \|  \/  | |")
            print(" | |_) | |  | | |  | | \  / | |")
            print(" |  _ <| |  | | |  | | |\/| | |")
            print(" | |_) | |__| | |__| | |  | |_|")
            print(" |____/ \____/ \____/|_|  |_(_)      THE END ¯\('…')/¯" + BColors.ENDC)
            print("")
            mapping.result(4, 'code')

        time.sleep(1)

def main():
    """Start the Hybrid prototype

    :param string configfile: The configurationfile to use. Defaults to default_setup.ini
    """
    global mapping, parameters, conditionalsRange, conditionals, \
           param_interval, threads_are_perpetual, range_trigger, \
           notecounter, hello_world_on, noteCounter, ck_deltatime, \
           ck_deltatime_mem, codeK, mainMem, memLow, memMid, memHi, \
           tremoloHi, tremoloLow, tremoloMid
    
    codeK = Setup()
    codeK.print_welcome(27)
    codeK.open_port(myPort)    

    codeK.print_lines(20, 1)
    print("Prototype loaded: Hybrid 0.3")
    print("CodeKlavier is ready and LISTENING.")
    codeK.print_lines(20, 1)
    print("\nPress Control-C to exit.\n")

    # default mapping
    mapping = Mapping_Motippets(False)
    
    # main memory (i.e. listen to the whole register)
    mainMem = Motippets(mapping, device_id)
    
    # midi listening per register
    memLow = Motippets(mapping, device_id)
    memMid = Motippets(mapping, device_id)
    memHi = Motippets(mapping, device_id)
    
    #midi listening for tremolos
    tremoloHi = Motippets(mapping, device_id)
    tremoloMid = Motippets(mapping, device_id)
    tremoloLow = Motippets(mapping, device_id)
    
    #midi listening for conditionals
    conditionals = {1: Motippets(mapping, device_id),
                    2: Motippets(mapping, device_id),
                    3: Motippets(mapping, device_id)}
    
    conditionalsRange = Motippets(mapping, device_id)
    parameters = Motippets(mapping, device_id)
    
    try:
        while keep_main_alive:
            while motippets_is_listening:
                msg = codeK.get_message()
    
                if msg:
                    message, deltatime = msg
                    ck_deltatime += deltatime
    
                    if message[0] != 254:
    
                        #note offs:
                        #if (message[0] == noteoff_id or message[2] == 0):
                            #ck_deltatime = 0
    
                        if message[0] == device_id:
                            if message[2] > 0 and message[0] == device_id:
                                notecounter += 1
    
                                ck_deltatime_mem.append(ck_deltatime)
                                #print('deltatimes before: ', ck_deltatime_mem)
    
                                if len(ck_deltatime_mem) > 2:
                                    ck_deltatime = 0
                                    ck_deltatime_mem = ck_deltatime_mem[-2:]
                                    ck_deltatime_mem[0] = 0
    
                                if len(ck_deltatime_mem) == 2:
                                    ck_deltadif = ck_deltatime_mem[1] - ck_deltatime_mem[0]
                                else:
                                    ck_deltadif = 0
    
                                if message[1] == 106:
                                    print('toggle prototype -> Hello World')
    
                                    codeK.close_port()
    
                                    #mapping = Mapping_HelloWorld()
    
                                    hello_world_on = True
                                    notecounter = 0
    
                                    threads['toggle_h'] = Thread(target=ck_loop, name='ck loop thread', args=('hello world',))
                                    threads['toggle_h'].start()
    
                                ##motifs:
                                mainMem.parse_midi(msg, 'full', ck_deltadif)
                                memLow.parse_midi(msg, 'low', ck_deltadif)
                                memMid.parse_midi(msg, 'mid', ck_deltadif)
                                memHi.parse_midi(msg, 'hi', ck_deltadif)
    
                                motif1_played = memMid._motif1_counter
                                motif2_played = mainMem._motif2_counter
    
                                minimotif1_low_mapped = memLow._unmapCounter1
                                minimotif2_low_mapped = memLow._unmapCounter2
                                minimotif3_low_mapped = memLow._unmapCounter3
    
                                minimotif1_mid_mapped = memMid._unmapCounter1
                                minimotif2_mid_mapped = memMid._unmapCounter2
    
                                minimotif1_hi_mapped = memHi._unmapCounter1
                                minimotif2_hi_mapped = memHi._unmapCounter2
    
                                ##tremolos:
                                if motif1_played > 0 or motif2_played > 0:
                                    if minimotif1_low_mapped > 0:
                                        tremoloLow.parse_midi(msg, 'tremoloLow', ck_deltadif, 1)
                                    elif minimotif2_low_mapped > 0:
                                        tremoloLow.parse_midi(msg, 'tremoloLow', ck_deltadif, 2)
                                    elif minimotif3_low_mapped > 0:
                                        tremoloLow.parse_midi(msg, 'tremoloLow', ck_deltadif, 3)
    
                                    if minimotif1_mid_mapped > 0:
                                        tremoloMid.parse_midi(msg, 'tremoloMid', ck_deltadif, 1)
                                    elif minimotif2_mid_mapped > 0:
                                        tremoloMid.parse_midi(msg, 'tremoloMid', ck_deltadif, 2)
    
                                    if minimotif1_hi_mapped > 0:
                                        tremoloHi.parse_midi(msg, 'tremoloHi', ck_deltadif, 1)
                                    elif minimotif2_hi_mapped > 0:
                                        tremoloHi.parse_midi(msg, 'tremoloHi', ck_deltadif, 2)
    
                                ##conditionals
                                conditional_value = conditionals[1].parse_midi(msg, 'conditional 1', ck_deltadif)
                                conditional2_value = conditionals[2].parse_midi(msg, 'conditional 2', ck_deltadif)
                                conditional3_value = conditionals[3].parse_midi(msg, 'conditional 3', ck_deltadif)
    
                                if isinstance(conditional_value, int) and conditional_value > 0:
                                    conditional_params = parameters.parse_midi(msg, 'params', ck_deltadif)
    
                                    #set the parameter for the timer:
                                    if isinstance(conditional_params, int) and conditional_params > 0:
                                        if conditional_value != 4:
                                            threads['set_param'] = Thread(target=set_parameters, name='set timer value', args=(conditional_params, 'amount'))
                                            threads['set_param'].start()
                                        elif conditional_value == 4: #gong bomb
                                            threads['set_param'] = Thread(target=set_parameters, name='set countdown value', args=(conditional_params, 'gomb'))
                                            threads['set_param'].start()
    
                                    if param_interval > 0:
                                        #if conditional_value != 4:
                                        notecounter = 0 # reset the counter
                                        threads[conditional_value] = Thread(target=noteCounter, name='conditional note counter thread', args=(param_interval, 100, conditional_value, True))
                                        threads[conditional_value].start()
                                        #elif conditional_value == 4:
                                        #start the countdown
                                        #gomb = Thread(target=gong_bomb, name='gomb', args=(param_interval, True))
                                        #gomb.start()
    
                                if isinstance(conditional2_value, int) and conditional2_value > 0:
                                    conditionalsRange._conditionalStatus = conditional2_value
                                    conditional_params = parameters.parse_midi(msg, 'params', ck_deltadif)
    
                                    # set range parameter:
                                    if isinstance(conditional_params, int) and conditional_params > 0:
                                        if conditional_value != 4:
                                            threads['set_param'] = Thread(target=set_parameters, name='set timer value', args=(conditional_params, 'range'))
                                            threads['set_param'].start()
                                        elif conditional_value == 4: #gong bomb
                                            threads['set_param'] = Thread(target=set_parameters, name='set countdown value', args=(conditional_params, 'gomb'))
                                            threads['set_param'].start()
    
                                    if param_interval > 0:
                                        threads[conditional2_value] = Thread(target=rangeCounter, name='conditional range thread',
                                                                                 args=('random', 'more than', 2, conditional2_value, param_interval))
                                        threads[conditional2_value].start()
    
                                if isinstance(conditional3_value, int) and conditional3_value > 0:
                                    conditionalsRange._conditionalStatus = conditional3_value
                                    conditional_params = parameters.parse_midi(msg, 'params', ck_deltadif)
    
                                        # set range parameter:
                                    if isinstance(conditional_params, int) and conditional_params > 0:
                                        if conditional_value != 4:
                                            threads['set_param'] = Thread(target=set_parameters, name='set timer value', args=(conditional_params, 'range'))
                                            threads['set_param'].start()
                                        elif conditional_value == 4: #gong bomb
                                            threads['set_param'] = Thread(target=set_parameters, name='set countdown value', args=(conditional_params, 'gomb'))
                                            threads['set_param'].start()
    
                                    if param_interval > 0:
                                        threads[conditional3_value] = Thread(target=rangeCounter, name='conditional range thread',
                                                                             args=('random', 'less than', 3, conditional3_value, param_interval))
                                        threads[conditional3_value].start()
    
                                #range parser
                                if range_trigger == 1:
                                    conditionalsRange.parse_midi(msg, 'conditional_range')
    
                time.sleep(0.01) #check

    except KeyboardInterrupt:
        print('')
    finally:
        codeK.end()

def ck_loop(prototype='hello world'):
    """
    the main loop thread for the Codeklavier to listen to incoming midi messages

    :param string prototype: The name of the prototype to process
    """
    global mapping, parameters, conditionalsRange, conditionals, \
           param_interval, threads_are_perpetual, range_trigger, \
           notecounter, hello_world_on, noteCounter, motippets_is_listening, \
           ck_deltatime, ck_deltatime_mem

    codeK_thread = Setup()
    codeK_thread.open_port(myPort)

    print('port', myPort)

    #go to the end of the codespace screen
    mapping.goDown()

    if prototype == 'hello world':
        try:
            while hello_world_on:
                msg = codeK_thread.get_message()

                if msg:
                    message, deltatime = msg

                    if message[0] != 254 and message[0] != 208:
                        if message[2] > 0: #only noteOn
                            if (message[0] == device_id):

                                if message[1] == 106:
                                    print('toggle prototype -> Motippets')

                                    codeK_thread.close_port()

                                    #mapping = Mapping_Motippets()

                                    hello_world_on = False
                                    motippets_is_listening = True
                                    notecounter = 0

                                    threads['toggle_m'] = Thread(target=ck_loop, name='ck loop thread', args=('motippets',))
                                    threads['toggle_m'].start()

                                mapping.mapping(message[1])

                time.sleep(0.01)

        except KeyboardInterrupt:
            print('')
        finally:
            #print('hybrid thread stopped')
            codeK_thread.end()

    elif prototype == 'motippets':
        # reset deltatimes
        ck_deltatime = 0
        ck_deltatime_mem = []

        try:
            while motippets_is_listening:
                msg = codeK_thread.get_message()

                if msg:
                    message, deltatime = msg
                    ck_deltatime += deltatime

                    if message[0] == device_id:
                        if message[2] > 0 and message[0] == device_id:
                            notecounter += 1

                            ck_deltatime_mem.append(ck_deltatime)

                            if len(ck_deltatime_mem) > 2:
                                ck_deltatime = 0
                                ck_deltatime_mem = ck_deltatime_mem[-2:]
                                ck_deltatime_mem[0] = 0

                            if len(ck_deltatime_mem) == 2:
                                ck_deltadif = ck_deltatime_mem[1] - ck_deltatime_mem[0]
                            else:
                                ck_deltadif = 0

                            if message[1] == 106:
                                print('toggle prototype -> Hello World')

                                codeK_thread.close_port()

                                #mapping = Mapping_HelloWorld()

                                motippets_is_listening = False
                                hello_world_on = True
                                notecounter = 0

                                threads['toggle_h'] = Thread(target=ck_loop, name='ck loop thread', args=('hello world',))
                                threads['toggle_h'].start()

                            ##motifs:
                            mainMem.parse_midi(msg, 'full', ck_deltadif)
                            memLow.parse_midi(msg, 'low', ck_deltadif)
                            memMid.parse_midi(msg, 'mid', ck_deltadif)
                            memHi.parse_midi(msg, 'hi', ck_deltadif)

                            motif1_played = memMid._motif1_counter
                            motif2_played = mainMem._motif2_counter

                            minimotif1_low_mapped = memLow._unmapCounter1
                            minimotif2_low_mapped = memLow._unmapCounter2
                            minimotif3_low_mapped = memLow._unmapCounter3

                            minimotif1_mid_mapped = memMid._unmapCounter1
                            minimotif2_mid_mapped = memMid._unmapCounter2

                            minimotif1_hi_mapped = memHi._unmapCounter1
                            minimotif2_hi_mapped = memHi._unmapCounter2

                            ##tremolos:
                            if motif1_played > 0 or motif2_played > 0:

                                if minimotif1_low_mapped > 0:
                                    tremoloLow.parse_midi(msg, 'tremoloLow', ck_deltadif, 1)
                                elif minimotif2_low_mapped > 0:
                                    tremoloLow.parse_midi(msg, 'tremoloLow', ck_deltadif, 2)
                                elif minimotif3_low_mapped > 0:
                                    tremoloLow.parse_midi(msg, 'tremoloLow', ck_deltadif, 3)

                                if minimotif1_mid_mapped > 0:
                                    tremoloMid.parse_midi(msg, 'tremoloMid', ck_deltadif, 1)
                                elif minimotif2_mid_mapped > 0:
                                    tremoloMid.parse_midi(msg, 'tremoloMid', ck_deltadif, 2)

                                if minimotif1_hi_mapped > 0:
                                    tremoloHi.parse_midi(msg, 'tremoloHi', ck_deltadif, 1)
                                elif minimotif2_hi_mapped > 0:
                                    tremoloHi.parse_midi(msg, 'tremoloHi', ck_deltadif, 2)

                            ##conditionals
                            conditional_value = conditionals[1].parse_midi(msg, 'conditional 1', ck_deltadif)
                            conditional2_value = conditionals[2].parse_midi(msg, 'conditional 2', ck_deltadif)
                            conditional3_value = conditionals[3].parse_midi(msg, 'conditional 3', ck_deltadif)

                            if isinstance(conditional_value, int) and conditional_value > 0:
                                conditional_params = parameters.parse_midi(msg, 'params', ck_deltadif)

                                #set the parameter for the timer:
                                if isinstance(conditional_params, int) and conditional_params > 0:
                                    if conditional_value != 4:
                                        threads['set_param'] = Thread(target=set_parameters, name='set timer value', args=(conditional_params, 'amount'))
                                        threads['set_param'].start()
                                    elif conditional_value == 4: #gong bomb
                                        threads['set_param'] = Thread(target=set_parameters, name='set countdown value', args=(conditional_params, 'gomb'))
                                        threads['set_param'].start()

                                if param_interval > 0:
                                    #if conditional_value != 4:
                                    notecounter = 0 # reset the counter
                                    threads[conditional_value] = Thread(target=noteCounter, name='conditional note counter thread', args=(param_interval, 100, conditional_value, True))
                                    threads[conditional_value].start()
                                    #elif conditional_value == 4:
                                    #start the countdown
                                    #gomb = Thread(target=gong_bomb, name='gomb', args=(param_interval, True))
                                    #gomb.start()

                            if isinstance(conditional2_value, int) and conditional2_value > 0:
                                conditionalsRange._conditionalStatus = conditional2_value
                                conditional_params = parameters.parse_midi(msg, 'params', ck_deltadif)

                                # set range parameter:
                                if isinstance(conditional_params, int) and conditional_params > 0:
                                    if conditional_value != 4:
                                        threads['set_param'] = Thread(target=set_parameters, name='set timer value', args=(conditional_params, 'range'))
                                        threads['set_param'].start()
                                    elif conditional_value == 4: #gong bomb
                                        threads['set_param'] = Thread(target=set_parameters, name='set countdown value', args=(conditional_params, 'gomb'))
                                        threads['set_param'].start()

                                if param_interval > 0:
                                    threads[conditional2_value] = Thread(target=rangeCounter, name='conditional range thread',
                                                                         args=('random', 'more than', 2, conditional2_value, param_interval))
                                    threads[conditional2_value].start()

                            if isinstance(conditional3_value, int) and conditional3_value > 0:
                                conditionalsRange._conditionalStatus = conditional3_value
                                conditional_params = parameters.parse_midi(msg, 'params', ck_deltadif)

                                # set range parameter:
                                if isinstance(conditional_params, int) and conditional_params > 0:
                                    if conditional_value != 4:
                                        threads['set_param'] = Thread(target=set_parameters, name='set timer value', args=(conditional_params, 'range'))
                                        threads['set_param'].start()
                                    elif conditional_value == 4: #gong bomb
                                        threads['set_param'] = Thread(target=set_parameters, name='set countdown value', args=(conditional_params, 'gomb'))
                                        threads['set_param'].start()

                                if param_interval > 0:
                                    threads[conditional3_value] = Thread(target=rangeCounter, name='conditional range thread',
                                                                         args=('random', 'less than', 3, conditional3_value, param_interval))
                                    threads[conditional3_value].start()

                            #range parser
                            if range_trigger == 1:
                                conditionalsRange.parse_midi(msg, 'conditional_range')

                time.sleep(0.01) #check

        except KeyboardInterrupt:
            print('')
        finally:
            #print('hybrid thread stopped')
            codeK_thread.end()

if (__name__ == '__main__'):
    try:
        options, args = getopt.getopt(sys.argv[1:],'hc:m:',['help', 'configfile=', 'makeconfig='])
        selected_options = [x[0] for x in options]
    except getopt.GetoptError:
        print('Something went wrong with parsing the options')
    if ('-c' in selected_options or '--configfile' in selected_options) \
        and ('-m' in selected_options or '--makeconfig' in selected_options):
        #cannot deal with creating a new one and using a specified config
        raise ValueError('Choose either the "configfile-option" or the option to create a configfile. Not both.')
    for o, a in options:
        if o in ('-h', '--help'):
            print('Usage: python3 motippets.py [OPTION]')
            print('')
            print('Where [OPTION] is:')
            print('  -h | --help')
            print('    Print this help text.')
            print('')
            print('  -c <<file>> | --configgile <<file>>')
            print('    Use configuration file <<file>>. You can write this configuration file with the -m option')
            print('')
            print('  -m <<filename>> | --makeconfig <<filename>>')
            print('    Create a configfile and use it. If <<filename>> already exits, it will be over written.')
            sys.exit(0)
        if o in ('-c', '--configfile'):
            #use existing configfile
            main(configfile=a)
        if o in ('-m', '--makeconfig'):
            #create new configfile and use it
            CK_configWriter.createConfig(configfile=a)
            main(configfile=a)

    #no options were supplied: run motippets with default settings
    main()