#!/usr/bin/env python3

"""miditest.py

This file is a tester for the midisignals from your input device. It quickly helps you 
check if your midi input device is being registered and it's messages received. 
This file is not a formal part of the CodeKlavier. However, if you can see the 
midi messages being printed after running this script then you can rest assured that
the CodeKlavier will run with your midi setup.
"""

#TODO: add docstrings and comments

import time
import rtmidi

def print_welcome():
    for i in range(1, 5):
        num = 20+(1)
        print('##'*num)
        #TODO: add codeKlavier logo
        time.sleep(0.2)
    
    print('\n', "Welcome to the Codeklavier...", '\n')

def show_ports(ports):
    print("These are your detected MIDI devices:", '\n')
    for port in ports:
        print(ports.index(port), " -> ", port)

def get_port_from_user(ports):
    selected_midiport = -1
    while selected_midiport < 0:
        try:
            choice = input("Please choose the MIDI device (number) you want to use and hit Enter:")
            selected_midiport = int(choice)
            if selected_midiport < 0 or selected_midiport >= len(ports):
                print("Invalid number, please try again:")
                selected_midiport = -1
            else:
                return selected_midiport
        except KeyboardInterrupt:
            print('\n', "You want to quit? Fine with me!. Bye bye.")
            return -1
        except ValueError:
            print("Sorry, type a valid port numer!")

def open_port(midi, ports, pnum):
    print("You have chosen: ", ports[pnum])
    
    if ports:
        #TODO: do we need to check on the existence of ports?
        midi.open_port(pnum)
    else:
        raise Exception("No midi ports! Don't know what to do!")

def run(midi):
    print("CodeKlavier is ON. Press Control-C to exit.")
    try:
        timer = time.time()
        while True:
            msg = midi.get_message()
            
            if msg:
                message, deltatime = msg
                print('deltatime: ', deltatime, 'msg: ', message)
    
            time.sleep(0.01)

    except KeyboardInterrupt:
        print('')
    finally:
        print("Bye-Bye :(")
        midi.close_port()
        del midi

def main():
    midiin = rtmidi.MidiIn()
    ports = midiin.get_ports()

    print_welcome()
    show_ports(ports)
    my_midiport = get_port_from_user(ports)
    if my_midiport >= 0:
        open_port(midiin, ports, my_midiport)
        run(midiin)

if __name__ == "__main__":
    main()
