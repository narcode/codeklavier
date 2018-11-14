#!/usr/bin/env python3
"""
CodeKlavier Masterscript

This script will help you run the Codeklavier
"""

import configparser
import getopt
import os.path
import sys
import time
import importlib
import re

import CK_configWriter
from CK_Setup import Setup

ck_deltatime_mem = []

PROTOTYPES = ('hello_world', 'motippets', 'hybrid', 'ckalculator', 'text', 'presenter')

def doHelp():
    """
    Show the help for running this script.
    """
    print('This script will help you to run the CodeKlavier.')
    print('')
    print('Usage: ./codeklaver.py [OPTION]')
    print('') 
    print('Where [OPTION] is:')
    print('-c | --configfile <<configfile>>')
    print('Start CodeKlavier with the configuration in <<configfile>>. Note: -c and -m options cannot be used together.')
    print('')
    print('-h | --help')
    print('Show this help text.')
    print('')
    print('-i | --interactive')
    print('Start CodeKlavier in interactive mode')
    print('')
    print('-m | --makeconfig <<configfile>>')
    print('Create a new configfile <<configfile>> and use it to start CodeKlavier. Note: -c and -m options cannot be used together.')
    print('')
    print('-p | --prototype <<name>>')
    print('Boot CodeKlavier with prototype <<name>>')
    print('')
    print('-o | --option <<number>>')
    print('Boot CodeKlavier prototype <<name>> with specific <<option>> (if the prototype supports extra options)')
    print('')    
    print('-r | --rec')
    print('Boot CodeKlavier ready to record MIDI for machine learning')
    print('')        
    print('-t | --test')
    print('Test if Codeklavier is receving MIDI')
    print('')       
    print('Example:')
    print('./codeklavier.py -c custom_settings.ini -p hybrid')

def miditest(configfile='default_setup.ini'):
    """
    Run a basic miditest to see how the CodeKlavier is receiving your midi.

    :param string configfile: Path to the configuration file (default: default_setup.ini)
    """
    #Read config and settings
    config = configparser.ConfigParser()
    config.read(configfile, encoding='utf8')

    try:
        myPort = config['midi'].getint('port')
        device_id = config['midi'].getint('device_id')
    except KeyError:
        raise LookupError('Missing key information in the config file.')

    if (myPort == None or device_id == None):
        raise LookupError('Missing key information in the config file.')

    codeK = Setup()
    codeK.open_port(myPort)
    print('your device id is: ', device_id, '\n')
    print("CodeKlavier is ON. Press Control-C to exit.")
    try:
        while True:
            msg = codeK.get_message()

            if msg:
                message, deltatime = msg
                print('deltatime: ', deltatime, 'msg: ', message)

            time.sleep(0.01)

    except KeyboardInterrupt:
        print('')
    finally:
        print("Bye-Bye :(")
        codeK.end()

def delta_difference(deltatime):   
    # activesense compensation
    global ck_deltatime_mem
    
    ck_deltatime_mem.append(deltatime)
    #print('deltatimes stack: ', ck_deltatetime_mem)
    
    if len(ck_deltatime_mem) > 2:
        ck_deltatime_mem = ck_deltatime_mem[-2:]
        
    if len(ck_deltatime_mem) == 2:
        return ck_deltatime_mem[1] - ck_deltatime_mem[0]
    else:
        return 0  
    
def rec(configfile='default_setup.ini'):
    """
    Run a basic miditest to see how the CodeKlavier is receiving your midi.

    :param string configfile: Path to the configuration file (default: default_setup.ini)
    """
    #Read config and settings
    config = configparser.ConfigParser()
    config.read(configfile, encoding='utf8')

    try:
        myPort = config['midi'].getint('port')
        device_id = config['midi'].getint('device_id')
    except KeyError:
        raise LookupError('Missing key information in the config file.')

    if (myPort == None or device_id == None):
        raise LookupError('Missing key information in the config file.')

    codeK = Setup()
    codeK.open_port(myPort)
    print('your device id is: ', device_id, '\n')
    print("CodeKlavier is RECORDING. Press Control-C to exit.")
    timestamp = time.strftime("%y-%m-%d")
    ck_deltatime = 0
    per_note = 0
    recfile = open('ml_data/_', 'w')
    headers = 'source_id,midi_note,velocity,ck_deltatime,dif_deltatime'
    recfile.write(headers+'\n')
    try:
        while True:
            msg = codeK.get_message()

            if msg:
                message, deltatime = msg
                ck_deltatime += deltatime
                if message[0] == device_id:                    
                    per_note += deltatime
                else:
                    per_note = 0
                if message[0] != 254:
                    dif = delta_difference(per_note)                    
                    midimsg = list(map(str, message))
                    data_line = ','.join(midimsg) + ',' + str(ck_deltatime) + ',' + str(dif) +'\n'
                    clean_line = re.sub(r"\[?\]?", '', data_line)
                    recfile.write(clean_line)
                    print(clean_line)
            #time.sleep(0.01)

    except KeyboardInterrupt:
        print('saving recording...')
    finally:
        recfile.close()
        title = input('Dear CK user, please type a comprehensive title for the recording and press ENTER:');
        usertitle = title+'_'+timestamp+'.csv'
        os.rename("ml_data/_", "ml_data/"+usertitle)
        print("recording saved with title: ", usertitle)
        codeK.end()        

def perform(configfile='default_setup.ini', prototype='hello_world'):
    """
    Boot a specific prototype from the CodeKlavier

    :param string configfile: Path to the configuration file (default: default_setup.ini)
    :param string prototype: name of the prototype to boot
    """
    if (prototype not in PROTOTYPES):
        raise ValueError('This prototype doesn\'t exist. Please retry.')
    
    module = importlib.import_module(prototype)
    prototype = getattr(module, prototype)
    if option == None:
        eval(prototype.main())
    else:
        eval(prototype.main(option))
    
def perform_interactive(configfile='default_setup.ini'):
    """
    Run Codeklavier in interactive mode.

    :param string configfile: Path to the configuration file (default: default_setup.ini)
    """
    codeK = Setup()
    count = 1
    while True:
        codeK.print_welcome(28)
        print('Type the number of the prototype you want to use,'\
              '\n \'rec\' to start machine learning data recording'\
              '\n \'test\' for a miditest,\n or \'exit\' to quit.')
        print('')
        print('The available prototypes are:')

        for p in PROTOTYPES:
            count = count + 1
            print(' ', count, '.' + p)
        print('')
        pi = input('Type your choice? ')
        if (pi.lower() == 'exit'):
            sys.exit(0)
        if (pi.lower() == 'test'):
            miditest(configfile=configfile)
        if (pi.lower() == 'rec'):
            rec(configfile=configfile)            
        try:
            perform(configfile=configfile, prototype=pi)
        except ValueError:
            print('That is not an available prototype. Try again or \'exit\'')

if __name__ == '__main__':
    """
    Catch the arguments that were used to start this function.

    Options are h, c, p, t, i

    There is no default.ini 'by default'. So if it is the first run and
    default.ini is not yet there then the scripts prompts the user for the
    interactive createConfig and saves it as default. I also noticed that just
    running codeklavier.py without arguments simply exits. It should better
    print the usage options or showhelp() before exiting.
    """

    showHelp = False
    test = False
    interactive = False
    useConfig = None
    createConfig = None
    play = None
    option = None

    try:
        options, args = getopt.getopt(sys.argv[1:],'hc:m:p:rtio:',['help', 'configfile=', 'makeconfig=', 'play=', 'rec', 'test', 'interactive, option'])
        selected_options = [x[0] for x in options]
    except getopt.GetoptError:
        print('Something went wrong with parsing the optional arguments')
    if ('-c' in selected_options or '--configfile' in selected_options) \
        and ('-m' in selected_options or '--makeconfig' in selected_options):
        #cannot deal with creating a new one and using a specified config
        raise ValueError('Chooce either the "configfile-option" or the option to create a configfile. Not both.')
    
    for o, a in options:
        if o in ('-h', '--help'):
            showHelp = True
        if o in ('-c', '--configfile'):
            useConfig = a
        if o in ('-m', '--makeconfig'):
            createConfig = a
        if o in ('-p', '--play'):
            play = a
        if o in ('-o', '--option'):
            option = a 
        if o in ('-t', '--test'):
            test = True
        if o in ('-r', '--rec'):
            record = True            
        if o in ('-i', '--interactive'):
            interactive = True

    if showHelp:
        doHelp()
        sys.exit(0)

    if createConfig:
        CK_configWriter.createConfig(configfile=createConfig)
        print('\nCongratultions! You have created ', createConfig, '\n')

    if (not(createConfig or useConfig or os.path.isfile('default_setup.ini'))):
        #User didn't specify a configfile -> create default
        print('No  setup file specified. Let\'s create the default!')
        CK_configWriter.createConfig(configfile='default_setup.ini')
        createConfig = 'default_setup.ini'

    config = useConfig if useConfig else createConfig
    config = config if config else 'default_setup.ini'

    if test:
        miditest(configfile=config)
        sys.exit(0)
        
    if rec:
        rec(configfile=config)
        sys.exit(0)        

    if play:
        perform(configfile=config, prototype=play)
        sys.exit(0)

    if interactive:
        perform_interactive(configfile=config)
        sys.exit(0)

    #no arguments -> print help
    print('What do you want CodeKlavier to do? Give me something!')
    print('These prototypes are available:')
    for p in PROTOTYPES:
        print(' - ', p)
    print('')
    print('Here is how CodeKlavier works:')
    doHelp()
    sys.exit(0)
    
    