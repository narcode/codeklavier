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

import CK_configWriter
from CK_Setup import Setup

from hello_world import hello_world
from motippets import motippets
from hybrid import hybrid

PROTOTYPES = ('hello_world', 'motippets', 'hybrid')

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
    print('Example:')
    print('./codeklavier.py -c custom_settings.ini -p hello_world')

def miditest(configfile='default_setup.ini'):
    """
    Run a basic miditest to see how the CodeKlavier is receiving your midi.

    :param string configfile: Path to the configuration file (default: default_setup.ini)
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

def perform(configfile='default_setup.ini', prototype='hello_world'):
    """
    Boot a specific prototype from the CodeKlavier

    :param string configfile: Path to the configuration file (default: default_setup.ini)
    :param string prototype: name of the prototype to boot
    """
    if (prototype not in PROTOTYPES):
        raise ValueError('This prototype doesn\'t exist. Please retry.')

    eval(prototype + '.main()')

def perform_interactive(configfile='default_setup.ini'):
    """
    Run Codeklavier in interactive mode.

    :param string configfile: Path to the configuration file (default: default_setup.ini)
    """
    codeK = Setup()
    count = 1
    while True:
        codeK.print_welcome(20)
        print('Type the number of the prototype you want to use,\n \'test\' for a miditest,\n or \'exit\' to quit.')
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

    if play:
        perform(configfile=config, prototype=play)
        sys.exit(0)

    if interactive:
        perform_interactive(configfile=config)
        sys.exit(0)

    #no arguments -> print help
    print('What do you want CodeKlavier to do? Give me something!')
    print('These prototypes are available:')
    for p in PIECES:
        print(' - ', p)
    print('')
    print('Here is how CodeKlavier works:')
    doHelp()
    sys.exit(0)
