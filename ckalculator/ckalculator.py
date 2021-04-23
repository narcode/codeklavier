#!/usr/bin/env python3

import getopt
import time
import sys
import rtmidi
import configparser
import CK_configWriter
from CK_Setup import Setup, BColors
from ckalculator_classes import Ckalculator

# increase recursion limit:
sys.setrecursionlimit(3000)

ckalculator_listens = True
ck_deltatime_mem = []
ck_note_dur = {}

def main(configfile='default_setup.ini'):
    """
    start the CKalculator
    """
    global ckalculator_listens, ck_deltatime_mem

    config = configparser.ConfigParser(delimiters=(':'), comment_prefixes=('#'))
    config.read(configfile, encoding='utf8')

    # TODO: optimize...
    try:
        myPort = config['midi'].getint('port')
        noteon_id = config['midi'].getint('noteon_id')
        noteoff_id = config['midi'].getint('noteoff_id')
        pedal_id = config['midi'].getint('pedal_id')
        pedal_sostenuto = config['midi'].getint('pedal_midi_sostenuto')
        staccato = config['articulation'].getfloat('staccato')
        sostenuto = config['articulation'].getfloat('sostenuto')
        chord = config['articulation'].getfloat('chord')
    except KeyError:
        raise LookupError('Missing midi and articulation information in the config file.')

    if (myPort == None or noteon_id == None):
        raise LookupError('Missing port and device id information in the config file.')

    codeK = Setup()
    codeK.print_welcome(27)
    codeK.open_port(myPort)

    codeK.print_lines(20, 1)
    print("Prototype loaded: Ckalculator AR extension 0.3")
    print("CodeKlavier is ready and LISTENING.")
    codeK.print_lines(20, 1)

    print("\nPress Control-C to exit.\n")       
    
    cKalc = Ckalculator(noteon_id, noteoff_id, pedal_id, config=config, print_functions=True, ar_hook=True)
    cKost = Ckalculator(noteon_id, noteoff_id, pedal_id, config=config, ar_hook=True)

    per_note = 0
    ck_deltatime = 0
    articulation = {'chord': chord, 'staccato': staccato, 'sostenuto': sostenuto}

    try:
        while ckalculator_listens:
            msg = codeK.get_message()

            if msg:
                #print(msg)
                message, deltatime = msg
                per_note += deltatime
                ck_deltatime += deltatime
                #print('delta per note:', per_note)
                #print('delta ck:', ck_deltatime)

                if message[0] in (noteoff_id, noteon_id, pedal_id):                          
                            
                    #note offs:
                    if (message[0] == noteoff_id or (message[0] == noteon_id and message[2] == 0)):
                        midinote = message[1]
                        #print(ck_note_dur)
                        if midinote in ck_note_dur:
                            note_duration = ck_deltatime - ck_note_dur.pop(midinote)

                        cKalc.parse_midi(msg, 'full', ck_deltatime_per_note=note_duration,
                                         ck_deltatime=ck_deltatime, articulation=articulation)

                        if len(cKost._functionBody) == 1:

                            if cKost._developedOstinato[1] == 1:
                                cKalc._functionBody['grab_num'] = True
                               
                                if cKalc._numForFunctionBody != None:
                                    cKost._functionBody['arg2'] = cKalc._numForFunctionBody
                                    print('function body complete...')
                                    cKalc.mapscheme.formatAndSend('function body complete...', display=4, 
                                                                  syntax_color='function:')
                                    cKost.storeFunction()
                                    cKalc._functionBody = {}
                                    cKalc._numForFunctionBody = None                                
                            else:
                                print('function with no args complete...')
                                if cKost._arg2Counter == 0:     
                                    cKost._functionBody['arg2'] = ''                                    
                                    cKost.storeFunctionAR()
                                    cKalc._functionBody = {}
                                else:
                                    cKost._functionBody['arg2'] = str(cKalc.ar._parallelTrees)
                                    cKost.storeFunctionAR()
                                    cKalc._functionBody = {}

                        cKost.parse_midi(msg, 'ostinatos', ck_deltatime_per_note=note_duration,
                                         ck_deltatime=ck_deltatime, articulation=articulation, sendToDisplay=False) # needed?

                    if message[0] == pedal_id and message[1] == pedal_sostenuto:
                        per_note = 0
                        cKalc.parse_midi(msg, 'full', ck_deltatime_per_note=0, ck_deltatime=0, articulation=articulation)
                    
                    #note ons:
                    if message[0] == noteon_id:
                        #per_note = 0
                        ck_note_dur[message[1]] = ck_deltatime
                        if message[2] > 0: 
                            dif = delta_difference(ck_deltatime) # not getting real note duration, only dt between events.
                            
                            cKost.parse_midi(msg, 'ostinatos', ck_deltatime_per_note=per_note, 
                                             ck_deltatime=dif, articulation=articulation, sendToDisplay=False)       
                            
                            cKalc._noteon_delta[message[1]] = per_note
                            cKalc._noteon_velocity[message[1]] = message[2]                    


    except KeyboardInterrupt:
        print('')
    finally:
        codeK.end()

def delta_difference(deltatime):
    # activesense compensation
    global ck_deltatime_mem

    ck_deltatime_mem.append(deltatime)
    #print('deltatimes stack: ', ck_deltatime_mem)

    if len(ck_deltatime_mem) > 2:
        ck_deltatime_mem = ck_deltatime_mem[-2:]

        if len(ck_deltatime_mem) == 2:
            dif = ck_deltatime_mem[1] - ck_deltatime_mem[0]
            if dif < 0:
                dif = 0
            return dif
        else:
            return 0


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
