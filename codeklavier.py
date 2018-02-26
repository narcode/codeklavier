#!/usr/bin/env python3
"""
CodeKlavier Masterscript

This script will help you run the code klavier
"""

import configparser
import getopt
import sys
import time

import CK_configWriter
from CK_Setup import Setup

from hello_world import hello_world
from motippets import motippets

PIECES = ('hello_world', 'motippets')

def showHelp():
    """
    Show the help for running this script.
    """
    print('Hallo')

def miditest(configfile='default_setup.ini'):
    """
    Run a basic miditest to see if everything is working.
    """
    #Read config and settings
    config = configparser.ConfigParser()
    config.read(configfile)
    
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

def perform(configfile='default_setup.ini', piece='hello_world'):
    """
    Do all the dificult work
    """
    if (piece not in PIECES):
        raise ValueError('This piece doesn\'t exist. Please compose it and retry.')

    eval(piece + '.main(configfile=\'' + configfile + '\')')

def perform_interactive(configfile='default_setup.ini'):
    """
    Run codeklavier in interactive mode.
    """
    while True:
        print('Welcome to CodeKlavier.')
        print('Type the name of the piece you want to play, \'test\' for a miditest, or \'exit\' to quit.')
        print('')
        print('The available pieces are:')
        for p in PIECES:
            print('  - ' + p)
        print('')
        pi = input('Your choice? ')
        if (pi.lower() == 'exit'):
            sys.exit(0)
        if (pi.lower() == 'test'):
            miditest(configfile=configfile)
        try:
            perform(configfile=configfile, piece=pi)
        except ValueError:
            print('That is not an available piece. Try again or \'exit\'')

if __name__ == '__main__':

    showHelp = False
    test = False
    interactive = False
    useConfig = None
    createConfig = None
    play = None

    try:
        options, args = getopt.getopt(sys.argv[1:],'hc:m:p:ti',['help', 'configfile=', 'makeconfig=', 'play=', 'test', 'interactive'])
        selected_options = [x[0] for x in options]
    except getopt.GetoptError:
        print('Something went wrong with parsing the options')
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
        if o in ('-t', '--test'):
            test = True
        if o in ('-i', '--interactive'):
            interactive = True

    if showHelp:
        showHelp()
        sys.exit(0)

    if createConfig:
        CK_configWriter=createConfig(configfile=createConfig)

    config = useConfig if useConfig else createConfig
    config = config if config else 'default_setup.ini'

    if test:
        miditest(configfile=config)
        sys.exit(0)

    if play:
        perform(configfile=config, piece=play)
        sys.exit(0)

    if interactive:
        perform_interactive(configfile=config)
        sys.exit(0)

    sys.exit(0)
