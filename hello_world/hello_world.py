#!/usr/bin/env python3

import configparser
import getopt
import rtmidi
import sys
import time

# CodeKlavier Modules
import CK_configWriter
from CK_Setup import Setup
from hello_classes import HelloWorld
from Mapping import Mapping_HelloWorld

def main(configfile='../default_setup.ini'):
    """
    Start hello world!

    :param int configfile: use this configuration file. Defaults to 'default_setup.ini'.
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
    
    # Use your favourite mapping of the keys
    mapping = Mapping_HelloWorld()
    
    print("\nCodeKlavier is ready and ON.")
    print("You are performing: HELLO WORLD")
    print("\nPress Control-C to exit.")
    
    codeK.set_callback(HelloWorld(myPort, mapping, device_id))
    
    # Loop to program to keep listening for midi input
    try:
        while True:
            time.sleep(0.01)
    except KeyboardInterrupt:
        print('')
    finally:
        print("Bye-Bye :(")
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
        raise ValueError('Chooce either the "configfile-option" or the option to create a configfile. Not both.')
    for o, a in options:
        if o in ('-h', '--help'):
            print('Usage: python3 hello_world.py [OPTION]')
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

    #no options were supplied: run hello_world with default settings
    main()
