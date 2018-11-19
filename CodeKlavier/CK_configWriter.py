"""
Write a configfile for CodeKlavier
"""

import configparser
from CK_Setup import Setup

def createConfig(configfile='my_settings.ini'):
    """Create a basic configfile

    TODO!!: avoid that the created configfile overwrites the existing file
    (if present)!

    :param string configfile: path and name of the configfile
    """
    codeK = Setup()
    codeK.show_ports()
    myPort = codeK.get_port_from_user()
    codeK.open_port(myPort)
    device_id = codeK.get_device_id()

    config = configparser.ConfigParser()
    config.add_section('midi')
    config['midi']['port'] = str(myPort)
    config['midi']['noteon_id'] = str(device_id)

    with open(configfile, 'w') as f:
        config.write(f)
