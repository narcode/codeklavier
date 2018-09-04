"""
Tutorial for the Hello World NKK
"""
import configparser
import getopt
import rtmidi
import sys
import time

# CodeKlavier Modules
import CK_configWriter
from CK_Setup import Setup
from Mapping import Mapping_HelloWorld_NKK
from Instructions import Instructions

def main (configfile='../default_setup.ini'):
    # Start the CodeKlavier
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
    tutorial = Instructions()
    codeK.open_port(myPort)
    codeK.open_port_out(myPort)
    
    # Use your favourite mapping of the keys
    mapping = Mapping_HelloWorld_NKK()
    
    # class to handle the midi input and map it to characters
    #TODO: this is ugly! Move this to the CodeKlavier module
    class HelloWorld(object):
        def __init__(self, port):
            self.port = port
    
        def __call__(self, event, data=None):
            message, deltatime = event
            # print(message)
            if message[2] > 0: #only noteOn
                if (message[0] == device_id):
                    mapping.mapping(message[1])
    
    codeK.set_callback(HelloWorld(myPort))
    
    tutorial.do_tutorial()
    codeK.send_message([0x90, 108, 127]) #send enter to codespace
    tutorial.level_four()
    
    # Loop to program to keep listening for midi input
    try:
        timer = time.time()
        while True:
            time.sleep(0.01)
    except KeyboardInterrupt:
        print('')
    finally:
        # print("Bye-Bye :(")
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
            print('Usage: python3 instructions.py [OPTION]')
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

    #no options were supplied: instructions hello_world with default settings
    main()
