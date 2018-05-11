#!/usr/bin/env python3

import getopt
import time
import sys
import rtmidi
import configparser
import CK_configWriter
from CK_Setup import Setup, BColors
from ckalculator_classes import *

ckalculator_listens = True


def main(configfile='default_setup.ini'):
    """
    start the CKalculator
    """
    global ckalculator_listens
       
    # activesense compensation
    ck_deltatime_mem = []
    ck_deltatime = 0
    ck_deltadif = 0
    
    config = configparser.ConfigParser(delimiters=(':'), comment_prefixes=('#'))
    config.read(configfile)
    
    try:
        myPort = config['midi'].getint('port')
        device_id = config['midi'].getint('device_id')
        noteoff_id = config['midi'].getint('noteoff_id')
    except KeyError:
        raise LookupError('Missing key information in the config file.')
    
    if (myPort == None or device_id == None):
        raise LookupError('Missing key information in the config file.')
    
    codeK = Setup()
    
    codeK.print_lines(20, 1)
    print("Prototype loaded: Ckalculator 0.1")
    print("CodeKlavier is ready and LISTENING.")
    codeK.print_lines(20, 1)
    print("\nPress Control-C to exit.\n")       
    
    cKalc = Ckalculator(device_id, noteoff_id)
    
    try:
        while ckalculator_listens:
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
                            
                            cKalc.parse_midi(msg, 'full', ck_deltatime=ck_deltadif)
                            
            time.sleep(0.01)
                            
    except KeyboardInterrupt:
        print('')
    finally:
        codeK.end()
        
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

                                           
                                           