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

import CK_configWriter
from CK_Setup import Setup, BColors
from CK_rec import CK_Rec

ck_deltatime_mem = []

VERSIONS = ('hybrid', 'ckalculator')

def doHelp():
    """
    Show the help for running this script.
    """
    print(BColors.HEADER + 'This script will help you to run the 🎹 CodeKlavier 🎹' + BColors.ENDC)
    print('')
    print(BColors.CKGREEN + 'Usage: ./codeklaver.py [OPTION]' + BColors.ENDC)
    print('Where [OPTION] is:')
    print(BColors.BOLD + '-h | --help' + BColors.ENDC)
    print('Show this help text.')
    print('')
    print(BColors.BOLD + '-p | --play' + BColors.WARNING + ' <<name>>' + BColors.ENDC)
    print('Boot CodeKlavier with version <<name>>')
    print('These versions are available: ' + (', ').join(VERSIONS))   
    print('')    
    print(BColors.BOLD + '-r | --rec' + BColors.ENDC)
    print('Boot CodeKlavier to record MIDI for machine learning')
    print('')        
    print(BColors.BOLD + '-t | --test' + BColors.ENDC)
    print('Test and visualize if Codeklavier is receving MIDI')
    print('')       
    print(BColors.UNDERLINE + 'Example:' + BColors.ENDC)
    print(BColors.CKGREEN + './codeklavier.py -p hybrid' + BColors.ENDC)
    print('')

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
        device_id = config['midi'].getint('noteon_id')
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

def boot(configfile='default_setup.ini', version=None):
    """
    Boot a specific version from the CodeKlavier

    :param string configfile: Path to the configuration file (default: default_setup.ini)
    :param string version: name of the version to boot
    """
    if (version not in VERSIONS):
        raise ValueError(BColors.WARNING + 'This version doesn\'t exist. Please retry.' + BColors.ENDC)
    
    module = importlib.import_module(version)
    version = getattr(module, version)
    eval(version.main())
    
if __name__ == '__main__':
    """
    Catch the arguments that were used to start this function.

    Options are h, c, p, t, r
    """

    showHelp = False
    test = False
    record = False
    interactive = False
    useConfig = None
    play = None

    try:
        options, args = getopt.getopt(sys.argv[1:],'h:p:rt:',['help', 'play=', 'rec', 'test'])
        selected_options = [x[0] for x in options]
    except getopt.GetoptError:
        print('Something went wrong parsing the optional arguments')
    
    for o, a in options:
        if o in ('-h', '--help'):
            showHelp = True
        if o in ('-p', '--play'):
            play = a
        if o in ('-t', '--test'):
            test = True
        if o in ('-r', '--rec'):
            record = True            

    if showHelp:
        doHelp()
        sys.exit(0)

    config = 'default_setup.ini'

    if test:
        miditest(configfile=config)
        sys.exit(0)
        
    if record:
        rec = CK_Rec(configfile=config)
        rec.record(framesize=1)
        sys.exit(0)        

    if play:
        boot(configfile=config, version=play)
        sys.exit(0)

    #no arguments -> print help
    doHelp()
    sys.exit(0)
    
    
