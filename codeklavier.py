#!/usr/bin/env python3
"""
CodeKlavier Masterscript

This script will help you run the code klavier
"""

import getopt
import sys

import CK_configWriter

from hello_world import hello_world
from motippets import motippets

PIECES = ('hello_world', 'motippets')

def showHelp():
    """
    Show the help for running this script.
    """
    print('Hallo')

def perform(config='default_setup.ini', piece='hello_world'):
    """
    Do all the dificult work
    """
    if (piece not in PIECES):
        raise ValueError('This piece doesn\'t exist. Please compose it and retry.')

    eval(piece + '.main(configfile=\'' + config + '\')')
    sys.exit(0)

if __name__ == '__main__':

    showHelp = False
    useConfig = None
    createConfig = None
    play = None

    try:
        options, args = getopt.getopt(sys.argv[1:],'hc:m:p:',['help', 'configfile=', 'makeconfig=', 'play='])
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

    if showHelp:
        showHelp()
        sys.exit(0)

    if createConfig:
        CK_configWriter=createConfig(configfile=createConfig)

    config = useConfig if useConfig else createConfig
    config = condif if config else 'default_setup.ini'

    if play:
        print(config)
        print(play)
        perform(config=config, piece=play)

    sys.exit(0)
