#!/usr/bin/env python3

import time
from threading import Thread, Event

import sys
import os
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from Setup import Setup
from Mapping import Mapping_Motippets
from motippets_classes import Motippets

# Start the CodeKlavier
codeK = Setup()
myPort = codeK.perform_setup()
codeK.open_port(myPort)
device_id = codeK.get_device_id()
print('your device id is: ', device_id, '\n')

# Use your favourite mapping of the keys

mapping = Mapping_Motippets()

print("\nCodeKlavier is ready and ON.")
print("You are performing: Motippets")
print("\nPress Control-C to exit.")

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

#multiprocessing vars
threads = {}
notecounter = 0
range_trigger = 0
param_interval = 0
threads_are_perpetual = True


#TODO: move this functions to a better place?
def set_parameters(value, conditional_func, debug=True):
    """
    function to parse a full range tremolo. This value can be used as a param for the 
    other functions.
    
    value: the interval of the plated tremolo
    """   
    global param_interval, range_trigger
    print('thread started for parameter set')
        
    if conditional_func == 'amount':
        mapping.customPass('// more than 100 notes played in the next ', str(value) + ' seconds?')
    elif conditional_func == 'range':
        mapping.customPass('// range set to: ', str(value) + ' semitones...')
    
    if debug:
        print('value parameter is ', str(value))
        
    param_interval = value        
    parameters._interval = 0 
    time.sleep(1) # check if the sleep is needed...
    range_trigger = 1

    
def parallelism(timer=10, numberOfnotes=100, result_num=1, debug=True):
    """
    TODO: define func
    """
    print('thread started for result ', result_num, 'number of notes: ', numberOfnotes)
    
    #reset parameter global once it has passed effectively:
    param_interval = 0
    
    for s in range(0, timer):
        if notecounter > numberOfnotes:
            mapping.customPass('//WOW! I played: ', str(notecounter)+'!!!')
            
            if result_num == 1:
                mapping.result(result_num, 'code')
                mainMem._motif2_counter = 0 #reset the motif counter so it can be played again...
                
            elif result_num == 2: #this is for snippet 1 - change the names accordingly
                mapping.result(result_num, 'code')
                memMid._motif1_counter = 0
                
            elif result_num == 3:
                mapping.result(result_num, 'code')
                               
            break
        else:
            mapping.customPass('notes played: ', str(notecounter))
            conditionals[1]._conditionalStatus = 0
            conditionals[1]._resultCounter = 0
            conditionals[1]._conditionalCounter = 0
            
        if debug:        
            print(notecounter)
        time.sleep(1)
    
def rangeCounter(timer=30, operator='', num=1, result_num=1, piano_range=72, debug=True, perpetual=True):
    """
   alculate the played range within a time window. Perpetual flag makes it run it's loop forever, unless range_trigger is != 1
   
   timer: time window loop
   operator: 'more than' or 'less than'
   num = conditional number
   result_num: result number mapped to this conditional
   piano_range: total range for evvaluation in semitones
   debug: booelan flag to post debug messages
   perpetual: boolean flag to make the function loop infinetly or 1 shot ## reserved for future versions
    """
    
    global range_trigger, threads_are_perpetual
    conditionals[num]._conditionalStatus = 0 #reset trigger
    t = 1
    
    if debug:
        print('thread for range started')
    print("range trig -> ", range_trigger, "result num: ", result_num, "range set to: ", piano_range)

    
    while threads_are_perpetual: 
        if debug:
            print('timer: ', t)
            print('Range conditional memory: ', conditionalsRange._memory)
        conditionalsRange._timer += 1
        t += 1
        
        if t % timer == 0:
            if debug:
                print("Range conditional thread finished")
                print("range was: ", conditionalsRange._range)
            if operator == 'more than':   
                if conditionalsRange._range >= piano_range:   
                    if result_num == 1:
                        mapping.result(1,'code')
                    elif result_num == 2:
                        mapping.result(2, 'code')
                    elif result_num == 3:
                        mapping.result(3, 'code')
                else:
                    mapping.customPass('condition not met', ':(')
                        
            elif operator == 'less than': 
                if conditionalsRange._range <= piano_range:
                    if result_num == 1:
                        mapping.result(1,'less than')
                        range_trigger = 0 
                        break # secret thread stop!
                    elif result_num == 2:
                        mapping.result(2, 'less than')
                    elif result_num == 3:
                        mapping.result(3, 'less than') 
                else:
                    mapping.customPass('condition not met', ':(')
                
                
            # reset states:    
            #range_trigger = 0    
            conditionalsRange._memory = []
            conditionals[num]._conditionalCounter = 0
            conditionals[num]._resultCounter = 0
            conditionalsRange._timer = 0
            t = 0        
        
        time.sleep(1)
    

        
# Loop to program to keep listening for midi input
try:
    while True:
        msg = codeK.get_message()

        if msg:
            message, deltatime = msg
            if message[0] != 254:
                if message[2] > 0 and message[0] == device_id:
                    notecounter += 1
                
                ##motifs:
                mainMem.parse_midi(msg, 'full')
                memLow.parse_midi(msg, 'low')
                memMid.parse_midi(msg, 'mid')
                memHi.parse_midi(msg, 'hi')
                
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
                        tremoloLow.parse_midi(msg, 'tremoloLow', 1)
                    elif minimotif2_low_mapped > 0:
                        tremoloLow.parse_midi(msg, 'tremoloLow', 2)
                    elif minimotif3_low_mapped > 0:
                        tremoloLow.parse_midi(msg, 'tremoloLow', 3)
                    
                    if minimotif1_mid_mapped > 0:
                        tremoloMid.parse_midi(msg, 'tremoloMid', 1)
                    elif minimotif2_mid_mapped > 0:
                        tremoloMid.parse_midi(msg, 'tremoloMid', 2)  
                    
                    if minimotif1_hi_mapped > 0:
                        tremoloHi.parse_midi(msg, 'tremoloHi', 1)
                    elif minimotif2_hi_mapped > 0:
                        tremoloHi.parse_midi(msg, 'tremoloHi', 2)                         
                
                ##conditionals 
                conditional_value = conditionals[1].parse_midi(msg, 'conditional 1')
                conditional2_value = conditionals[2].parse_midi(msg, 'conditional 2') 
                conditional3_value = conditionals[3].parse_midi(msg, 'conditional 3')
                                
                if isinstance(conditional_value, int) and conditional_value > 0:    
                    conditional_params = parameters.parse_midi(msg, 'params')                    
                   
                    #set the parameter for the timer:
                    # amount of notes not?
                    if isinstance(conditional_params, int) and conditional_params > 0:
                        threads['set_param'] = Thread(target=set_parameters, name='set timer value', args=(conditional_params, 'amount'))
                        threads['set_param'].start()
                                                
                    if param_interval > 0:
                        notecounter = 0 # reset the counter
                        threads[conditional_value] = Thread(target=parallelism, name='conditional note counter thread', args=(param_interval, 100, conditional_value, True))
                        threads[conditional_value].start()
                
                if isinstance(conditional2_value, int) and conditional2_value > 0:
                    conditionalsRange._conditionalStatus = conditional2_value
                    conditional_params = parameters.parse_midi(msg, 'params')                                        
                    
                    # set range parameter:
                    if isinstance(conditional_params, int) and conditional_params > 0:
                        threads['set_param'] = Thread(target=set_parameters, name='set timer value', args=(conditional_params, 'range'))
                        threads['set_param'].start()   
                        
                    if param_interval > 0:
                        threads[conditional2_value] = Thread(target=rangeCounter, name='conditional range thread', args=(31, 'more than', 2, conditional2_value, param_interval))
                        threads[conditional2_value].start()
                            
                if isinstance(conditional3_value, int) and conditional3_value > 0:
                    conditionalsRange._conditionalStatus = conditional3_value
                    conditional_params = parameters.parse_midi(msg, 'params')                                        
                    
                    # set range parameter:
                    if isinstance(conditional_params, int) and conditional_params > 0:
                        threads['set_param'] = Thread(target=set_parameters, name='set timer value', args=(conditional_params, 'range'))
                        threads['set_param'].start()   
                        
                    if param_interval > 0:
                        threads[conditional3_value] = Thread(target=rangeCounter, name='conditional range thread', args=(31, 'less than', 3, conditional3_value, param_interval))
                        threads[conditional3_value].start()
                    
                    #range parser
                if range_trigger == 1:
                    conditionalsRange.parse_midi(msg, 'conditional_range')   
             
        time.sleep(0.01) #check
        
except KeyboardInterrupt:
    print('')
finally:
    print("Bye-Bye :(")
    codeK.end()

