import configparser
import getopt
import sys
import time
import numpy as np
import ckonditionals


from threading import Thread, Event
from CK_config import inifile
from CK_Setup import Setup
from Mapping import *
from motippets_classes import Motippets
from hello_classes import HelloWorld
from Motifs import mini_motifs, mini_motifs_mel, conditional_motifs, conditional_motifs_mel, \
     conditional_results_motifs, conditional_results_motifs_mel

config = configparser.ConfigParser()
config.read(inifile, encoding='utf8')

try:
    myPort = config['midi'].getint('port')
    noteon_id = config['midi'].getint('noteon_id')
    noteoff_id = config['midi'].getint('noteoff_id')
    toggle_note = config['Hello World'].getint('toggle')
    mid_low = config['Motippets register division'].getint('mid_low')
    mid_hi = config['Motippets register division'].getint('mid_hi')
    motifs_playedLimit = config['motif counter'].getint('playlimit')
except KeyError:
    raise LookupError('Missing key information in the config file.')

if (myPort == None or noteon_id == None):
    raise LookupError('Missing key information in the config file.')

# activesense compensation
ck_deltatime_mem = {'all': [], 'low': [], 'mid': [], 'hi': []}
ck_deltatime = {'all': 0, 'low': 0, 'mid': 0, 'hi': 0}
ck_deltadif = {'all': 0, 'low': 0, 'mid': 0, 'hi': 0}

#multiprocessing vars
threads = {}
#notecounter = 0
#range_trigger = 0
#param_interval = 0
#threads_are_perpetual = True
#motippets_is_listening = True
hello_world_on = False
keep_main_alive = True

# motifs
mainMem = None
motifs_played = {}
mini_motifs_played = {'low': {}, 'mid': {}, 'hi': {}}

def main():
    """Start the Hybrid version
    """
    global mapping, parameters, conditionalsRange, conditionals, \
           hello_world_on, ck_deltatime, \
           ck_deltatime_mem, codeK, mainMem, memLow, memMid, memHi, \
           tremoloHi, tremoloLow, tremoloMid
    
    codeK = Setup()
    codeK.print_welcome(27)
    codeK.open_port(myPort)    

    codeK.print_lines(20, 1)
    print("Version loaded: Hybrid 0.9")
    print("CodeKlavier is ready and LISTENING.")
    codeK.print_lines(20, 1)
    print("\nPress Control-C to exit.\n")

    # default mapping
    mapping = Mapping_Motippets(False)
    
    # main memory (i.e. listen to the whole register)
    mainMem = Motippets(mapping, noteon_id, noteoff_id, mid_low, mid_hi, motifs_playedLimit)
    
    # midi listening per register
    memLow = Motippets(mapping, noteon_id, noteoff_id, mid_low, mid_hi)
    memMid = Motippets(mapping, noteon_id, noteoff_id, mid_low, mid_hi)
    memHi = Motippets(mapping, noteon_id, noteoff_id, mid_low, mid_hi)
    
    #midi listening for tremolos
    tremoloHi = Motippets(mapping, noteon_id, noteoff_id, mid_low, mid_hi)
    tremoloMid = Motippets(mapping, noteon_id, noteoff_id, mid_low, mid_hi)
    tremoloLow = Motippets(mapping, noteon_id, noteoff_id, mid_low, mid_hi)
    
    #midi listening for conditionals
    conditionals = {}
    for motif in conditional_motifs:
        conditionals[motif] = Motippets(mapping, noteon_id, noteoff_id, mid_low, mid_hi)
        
    for motif in conditional_motifs_mel:
        conditionals[motif] = Motippets(mapping, noteon_id, noteoff_id, mid_low, mid_hi)
    
    conditionalsRange = Motippets(mapping, noteon_id, noteoff_id, mid_low, mid_hi)
    parameters = Motippets(mapping, noteon_id, noteoff_id, mid_low, mid_hi)
    
    try:
        while keep_main_alive:
            while hello_world_on:
                time.sleep(0.01)
                
            while (not ckonditionals.stop_midi):
                msg = codeK.get_message()
    
                if msg:
                    message, deltatime = msg
                    for register in ck_deltatime:
                        ck_deltatime[register] += deltatime
    
                    if message[0] != 254:
    
                        if message[0] == noteon_id:
                            if message[2] > 0 and message[0] == noteon_id:
    
                                ck_deltatime_mem['all'].append(ck_deltatime['all'])
                                
                                if message[1] <= mid_low:
                                    ck_deltatime_mem['low'].append(ck_deltatime['low'])
                                elif message[1] > mid_hi:
                                    ck_deltatime_mem['hi'].append(ck_deltatime['hi'])
                                elif (message[1] > mid_low and message[1] <= mid_hi):
                                    ck_deltatime_mem['mid'].append(ck_deltatime['mid'])
                                    
                                for register in ck_deltatime_mem:  
                                    if len(ck_deltatime_mem[register]) > 2:
                                        ck_deltatime[register] = 0
                                        ck_deltatime_mem[register] = ck_deltatime_mem[register][-2:]
                                        ck_deltatime_mem[register][0] = 0
        
                                    if len(ck_deltatime_mem[register]) == 2:
                                        ck_deltadif[register] = ck_deltatime_mem[register][1] - ck_deltatime_mem[register][0]
                                    else:
                                        ck_deltadif[register] = 0                               
    
                                print(ck_deltadif, ck_deltatime, ck_deltatime_mem)
                                if message[1] == toggle_note:
                                    print('toggle version -> Hello World')
    
                                    codeK.close_port()
    
                                    #mapping = Mapping_HelloWorld()
    
                                    hello_world_on = True
                                    ckonditionals.stop_midi = True
                                    #notecounter = 0
    
                                    threads['toggle_h'] = Thread(target=ck_loop, name='ck loop thread', args=('hello world',))
                                    threads['toggle_h'].start()
    
                                ##motifs:
                                mainMem.parse_midi(msg, 'full', ck_deltadif['all'], ck_deltadif['low'], ck_deltadif['hi'], ck_deltadif['mid'])
                                memLow.parse_midi(msg, 'low', ck_deltadif['all'], ck_deltadif['low'], ck_deltadif['hi'], ck_deltadif['mid'])
                                memMid.parse_midi(msg, 'mid', ck_deltadif['all'], ck_deltadif['low'], ck_deltadif['hi'], ck_deltadif['mid'])
                                memHi.parse_midi(msg, 'hi', ck_deltadif['all'], ck_deltadif['low'], ck_deltadif['hi'], ck_deltadif['mid'])
    
                                for motif in config['chordal main motifs midi']:
                                    motifs_played[motif] = mainMem._motifsCount[motif]['count']
                                    
                                for motif in config['melodic main motifs midi']:
                                    motifs_played[motif] = mainMem._motifsCount[motif]['count']
                                
                                played = np.array(list(motifs_played.values()))
                                
                                for mini in mini_motifs_mel:
                                    top_note = np.array(mini_motifs_mel[mini]).max()
                                    bottom_note = np.array(mini_motifs_mel[mini]).min()
                                    if top_note <= mid_low:
                                        mini_motifs_played['low'][mini] = memLow._miniMotifsLow[mini]['count']
                                    elif bottom_note > mid_low and top_note <= mid_hi:
                                        mini_motifs_played['mid'][mini] = memMid._miniMotifsMid[mini]['count']
                                    elif bottom_note > mid_hi:
                                        mini_motifs_played['hi'][mini] = memHi._miniMotifsHi[mini]['count']
        
                                for mini in mini_motifs:
                                    top_note = np.array(mini_motifs[mini]).max()
                                    bottom_note = np.array(mini_motifs[mini]).min()
                                    if top_note <= mid_low:
                                        mini_motifs_played['low'][mini] = memLow._miniMotifsLow[mini]['count']
                                    elif bottom_note > mid_low and top_note <= mid_hi:
                                        mini_motifs_played['mid'][mini] = memMid._miniMotifsMid[mini]['count']
                                    elif bottom_note > mid_hi:
                                        mini_motifs_played['hi'][mini] = memHi._miniMotifsHi[mini]['count']
                                ##tremolos:
                                if played.any() > 0:
                                    for m in mini_motifs_played['low']:
                                        if mini_motifs_played['low'][m] > 0:
                                            tremoloLow.parse_midi(msg, 'tremoloLow', ck_deltatime_low=ck_deltadif['low'], target=m)
                                    
                                    for m in mini_motifs_played['mid']:
                                        if mini_motifs_played['mid'][m] > 0:
                                            tremoloMid.parse_midi(msg, 'tremoloMid', ck_deltatime_mid=ck_deltadif['mid'], target=m)
                                            
                                    for m in mini_motifs_played['hi']:  
                                        if mini_motifs_played['hi'][m] > 0:
                                            tremoloHi.parse_midi(msg, 'tremoloHi', ck_deltatime_hi=ck_deltadif['hi'], target=m)
    
                                ##conditionals
                                conditional_value = {}
                                conditional_params = None
                                for cond in conditionals:
                                                                            
                                    conditional_value[cond] = conditionals[cond].parse_midi(msg, cond, ck_deltadif['all'], ck_deltadif['low'], ck_deltadif['hi'], ck_deltadif['mid'])   
                                                              
                                    for r in conditionals['conditional_1']._conditional_results_all:
                                        if conditional_value[cond] == r:
                                            conditional_params = parameters.parse_midi(msg, 'params', ck_deltadif['all'], ck_deltadif['low'], ck_deltadif['hi'], ck_deltadif['mid'])                                     
                                            
                                    #set the parameter for the timer:
                                    if isinstance(conditional_params, int) and conditional_params > 0: 
                                        if conditional_value[cond] == 'gomb':
                                            threads['set_param'] = Thread(target=ckonditionals.set_parameters, 
                                                                          name='set countdown value', 
                                                                          args=(conditional_params, 'gomb', 
                                                                                mapping, parameters) )
                                            threads['set_param'].start()
                                        else:
                                            if conditional_value[cond] != None:
                                                if cond in config['snippets code output']:
                                                    conditional_settings = config['conditionals settings'].get(cond).split(',')
                                                    cond_type = conditional_settings[0]
                                                    perpetual = bool(int(conditional_settings[1].strip()))
                                                    if len(conditional_settings) > 2:
                                                        totalNotes = int(conditional_settings[2])
                                                    
                                                threads['set_param'] = Thread(target=ckonditionals.set_parameters, 
                                                                              name='set timer value', 
                                                                              args=(conditional_params, cond_type, 
                                                                                    mapping, parameters) )
                                                threads['set_param'].start()

                                    if ckonditionals.param_interval > 0:
                                        if conditional_value[cond] != None:                                         
                                            if cond_type == 'note_count':
                                                conditionals[cond]._noteCounter = 0
                                                threads[conditional_value[cond]] = Thread(target=ckonditionals.noteCounter, 
                                                                                             name='conditional note counter thread', 
                                                                                             args=(ckonditionals.param_interval, totalNotes, 
                                                                                                   conditional_value[cond], 
                                                                                                   True, mapping, 
                                                                                                   conditionals[cond], mainMem, perpetual) )
                                                threads[conditional_value[cond]].start()
                                                break
                                            
                                            elif cond_type == 'range_more_than':
                                                threads[conditional_value[cond]] = Thread(target=ckonditionals.rangeCounter, 
                                                                                             name='conditional range thread',
                                                                                             args=('random', 'more than', cond, 
                                                                                                   conditional_value[cond], 
                                                                                                   ckonditionals.param_interval, True, perpetual, 
                                                                                                   mapping, conditionals[cond], 
                                                                                                   conditionalsRange, mainMem) )
                                                threads[conditional_value[cond]].start()
                                                break 
                                            
                                            elif cond_type == 'range_less_than':
                                                threads[conditional_value[cond]] = Thread(target=ckonditionals.rangeCounter, 
                                                                                             name='conditional range thread',
                                                                                             args=('random', 'less than', cond, 
                                                                                                   conditional_value[cond], 
                                                                                                   ckonditionals.param_interval, True, perpetual, 
                                                                                                   mapping, conditionals[cond], 
                                                                                                   conditionalsRange, mainMem) )                                                
                                                threads[conditional_value[cond]].start()
                                                break
                                                                                       
                                #range parser
                                if ckonditionals.range_trigger == 1:
                                    conditionalsRange.parse_midi(msg, 'conditional_range')
    
                time.sleep(0.01)
    except KeyboardInterrupt:
        pass
    finally:
        codeK.end()

def ck_loop(version='hello world'):
    """
    the main loop thread for the Codeklavier to listen to incoming midi messages

    :param string version: The name of the version to process
    """
    global mapping, parameters, conditionalsRange, conditionals, \
           hello_world_on, ck_deltatime, \
           ck_deltatime_mem, codeK, mainMem, memLow, memMid, memHi, \
           tremoloHi, tremoloLow, tremoloMid        

    codeK_thread = Setup()
    codeK_thread.open_port(myPort)

    #go to the end of the codespace screen
    mapping.goDown()
    
    if version == 'hello world':
        try:
            while hello_world_on:
                msg = codeK_thread.get_message()

                if msg:
                    message, deltatime = msg

                    if message[0] != 254 and message[0] != 208:
                        if message[2] > 0: #only noteOn
                            if (message[0] == noteon_id):

                                if message[1] == toggle_note:
                                    print('toggle version -> Motippets')

                                    codeK_thread.close_port()

                                    #mapping = Mapping_Motippets()

                                    hello_world_on = False
                                    ckonditionals.stop_midi = False
                                    #notecounter = 0

                                    threads['toggle_m'] = Thread(target=ck_loop, name='ck loop thread', args=('motippets',))
                                    threads['toggle_m'].start()

                                mapping.mapping(message[1])
                                
                                #range parser
                                if ckonditionals.range_trigger == 1:
                                    conditionalsRange.parse_midi(msg, 'conditional_range')

                time.sleep(0.01)

        except KeyboardInterrupt:
            print('')
        finally:
            #print('hybrid thread stopped')
            codeK_thread.end()

    elif version == 'motippets':
        # reset deltatimes
        ck_deltatime = {'all': 0, 'low': 0, 'mid': 0, 'hi': 0}
        ck_deltatime_mem = {'all': [], 'low': [], 'mid': [], 'hi': []}

        try:
            while (not ckonditionals.stop_midi):
                msg = codeK_thread.get_message()

                if msg:
                    message, deltatime = msg
                    for register in ck_deltatime:
                        ck_deltatime[register] += deltatime
                    
                    if message[0] != 254:

                        if message[0] == noteon_id:
                            if message[2] > 0 and message[0] == noteon_id:
    
                                ck_deltatime_mem['all'].append(ck_deltatime['all'])
                                
                                if message[1] <= mid_low:
                                    ck_deltatime_mem['low'].append(ck_deltatime['low'])
                                elif message[1] > mid_hi:
                                    ck_deltatime_mem['hi'].append(ck_deltatime['hi'])
                                elif (message[1] > mid_low and message[1] <= mid_hi):
                                    ck_deltatime_mem['mid'].append(ck_deltatime['mid'])
                                    
                                for register in ck_deltatime_mem:  
                                    if len(ck_deltatime_mem[register]) > 2:
                                        ck_deltatime[register] = 0
                                        ck_deltatime_mem[register] = ck_deltatime_mem[register][-2:]
                                        ck_deltatime_mem[register][0] = 0
        
                                    if len(ck_deltatime_mem[register]) == 2:
                                        ck_deltadif[register] = ck_deltatime_mem[register][1] - ck_deltatime_mem[register][0]
                                    else:
                                        ck_deltadif[register] = 0
    
                                if message[1] == toggle_note:
                                    print('toggle version -> Hello World')
    
                                    codeK_thread.close_port()
    
                                    #mapping = Mapping_HelloWorld()
    
                                    ckonditionals.stop_midi = True
                                    hello_world_on = True
                                    #notecounter = 0
    
                                    threads['toggle_h'] = Thread(target=ck_loop, name='ck loop thread', args=('hello world',))
                                    threads['toggle_h'].start()
    
                                ##motifs:
                                mainMem.parse_midi(msg, 'full', ck_deltadif['all'], ck_deltadif['low'], ck_deltadif['hi'], ck_deltadif['mid'])
                                memLow.parse_midi(msg, 'low', ck_deltadif['all'], ck_deltadif['low'], ck_deltadif['hi'], ck_deltadif['mid'])
                                memMid.parse_midi(msg, 'mid', ck_deltadif['all'], ck_deltadif['low'], ck_deltadif['hi'], ck_deltadif['mid'])
                                memHi.parse_midi(msg, 'hi', ck_deltadif['all'], ck_deltadif['low'], ck_deltadif['hi'], ck_deltadif['mid'])
    
                                for motif in config['chordal main motifs midi']:
                                    motifs_played[motif] = mainMem._motifsCount[motif]['count']
                                    
                                for motif in config['melodic main motifs midi']:
                                    motifs_played[motif] = mainMem._motifsCount[motif]['count']                                    
                                    
                                played = np.array(list(motifs_played.values()))
                                    
                                for mini in mini_motifs_mel:
                                    top_note = np.array(mini_motifs_mel[mini]).max()
                                    bottom_note = np.array(mini_motifs_mel[mini]).min()
                                    if top_note <= mid_low:
                                        mini_motifs_played['low'][mini] = memLow._miniMotifsLow[mini]['count']
                                    elif bottom_note > mid_low and top_note <= mid_hi:
                                        mini_motifs_played['mid'][mini] = memMid._miniMotifsMid[mini]['count']
                                    elif bottom_note > mid_hi:
                                        mini_motifs_played['hi'][mini] = memHi._miniMotifsHi[mini]['count']
                                        
                                        
                                for mini in mini_motifs:
                                    top_note = np.array(mini_motifs[mini]).max()
                                    bottom_note = np.array(mini_motifs[mini]).min()
                                    if top_note <= mid_low:
                                        mini_motifs_played['low'][mini] = memLow._miniMotifsLow[mini]['count']
                                    elif bottom_note > mid_low and top_note <= mid_hi:
                                        mini_motifs_played['mid'][mini] = memMid._miniMotifsMid[mini]['count']
                                    elif bottom_note > mid_hi:
                                        mini_motifs_played['hi'][mini] = memHi._miniMotifsHi[mini]['count']
            
                                ##tremolos:
                                if played.any() > 0:
                                    for m in mini_motifs_played['low']:
                                        if mini_motifs_played['low'][m] > 0:
                                            tremoloLow.parse_midi(msg, 'tremoloLow', ck_deltadif['low'], m)
                                    
                                    for m in mini_motifs_played['mid']:
                                        if mini_motifs_played['mid'][m] > 0:
                                            tremoloMid.parse_midi(msg, 'tremoloMid', ck_deltadif['mid'], m)
                                            
                                    for m in mini_motifs_played['hi']:  
                                        if mini_motifs_played['hi'][m] > 0:
                                            tremoloHi.parse_midi(msg, 'tremoloHi', ck_deltadif['hi'], m)
        
                                ##conditionals
                                conditional_value = {}
                                conditional_params = None
                                for cond in conditionals:
                                            
                                    conditional_value[cond] = conditionals[cond].parse_midi(msg, cond, ck_deltadif['all'], 
                                                                                            ck_deltadif['low'], ck_deltadif['hi'], 
                                                                                            ck_deltadif['mid'])                                      
                                                                  
                                    for r in conditionals['conditional_1']._conditional_results_all:
                                        if conditional_value[cond] == r:
                                            conditional_params = parameters.parse_midi(msg, 'params', ck_deltadif['all'], 
                                                                                       ck_deltadif['low'], ck_deltadif['hi'], 
                                                                                       ck_deltadif['mid'])
                                                
                                    #set the parameter for the timer:
                                    if isinstance(conditional_params, int) and conditional_params > 0: 
                                        if conditional_value[cond] == 'gomb':
                                            threads['set_param'] = Thread(target=ckonditionals.set_parameters, 
                                                                              name='set countdown value', 
                                                                              args=(conditional_params, 'gomb', 
                                                                                    mapping, parameters) )
                                            threads['set_param'].start()
                                        else:
                                            if conditional_value[cond] != None:
                                                if cond in config['snippets code output']:
                                                    conditional_settings = config['conditionals settings'].get(cond).split(',')
                                                    cond_type = conditional_settings[0]
                                                    perpetual = bool(int(conditional_settings[1].strip()))
                                                    if len(conditional_settings) > 2:
                                                        totalNotes = int(conditional_settings[2])
                                                    
                                                threads['set_param'] = Thread(target=ckonditionals.set_parameters, 
                                                                                  name='set timer value', 
                                                                                  args=(conditional_params, cond_type, 
                                                                                        mapping, parameters) )
                                                threads['set_param'].start()
    
                                    if ckonditionals.param_interval > 0:
                                        if conditional_value[cond] != None:                                         
                                            if cond_type == 'note_count':
                                                conditionals[cond]._noteCounter = 0
                                                threads[conditional_value[cond]] = Thread(target=ckonditionals.noteCounter, 
                                                                                                 name='conditional note counter thread', 
                                                                                                 args=(ckonditionals.param_interval, totalNotes, 
                                                                                                       conditional_value[cond], 
                                                                                                       True, mapping, 
                                                                                                       conditionals[cond], mainMem, perpetual) )
                                                threads[conditional_value[cond]].start()
                                                break
                                                
                                            elif cond_type == 'range_more_than':
                                                threads[conditional_value[cond]] = Thread(target=ckonditionals.rangeCounter, 
                                                                                                 name='conditional range thread',
                                                                                                 args=('random', 'more than', cond, 
                                                                                                       conditional_value[cond], 
                                                                                                       ckonditionals.param_interval, True, perpetual, 
                                                                                                       mapping, conditionals[cond], 
                                                                                                       conditionalsRange, mainMem) )
                                                threads[conditional_value[cond]].start()
                                                break 
                                            
                                            elif cond_type == 'range_less_than':
                                                threads[conditional_value[cond]] = Thread(target=ckonditionals.rangeCounter, 
                                                                                          name='conditional range thread',
                                                                                          args=('random', 'less than', cond, 
                                                                                                conditional_value[cond], 
                                                                                                ckonditionals.param_interval, True, perpetual, 
                                                                                                mapping, conditionals[cond], 
                                                                                                conditionalsRange, mainMem) )                                                
                                                threads[conditional_value[cond]].start()
                                                break
                                                                                           
                                #range parser
                                if ckonditionals.range_trigger == 1:
                                    conditionalsRange.parse_midi(msg, 'conditional_range')
    
                time.sleep(0.01)

        except KeyboardInterrupt:
            pass
        finally:
            codeK_thread.end()

if (__name__ == '__main__'):
    main()

