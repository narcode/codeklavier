"""
Websocket class and helper functions for communication with browser
"""

import random
import asyncio
from threading import Thread, Event
import math
import numpy as np
import time
from Mapping import Mapping_Websocket

class CkWebsocket(object):
    """Main class for the Websocket"""
    
    def __init__(self):
        self.mapping = Mapping_Websocket()
        self.loop = asyncio.get_event_loop()       
        self.receiveState()        
        
    def run_in_loop(self, json):
        try:
            self.loop.run_until_complete(self.mapping.websocketloop(json))
        except:
            print('error sending')
    
    def receiveState(self):
        try:
            state = self.loop.run_until_complete(self.mapping.receive_new())
            print(state))
                
        except:
            print('error receiving')
                        
    def averageVelocity(self):
        """ calculate an average of velocities and return a normalized value between 0-1"""
        a = np.average(self._velocityMemory)
        norm = (a-1)/(127-1)
        
        if len(self._parallelTrees) == 0:
            self.run_in_loop(self.makeJsonValue(self.currentTree(), norm))
        else:
            string = ''
            comma = ','
            for t in self._parallelTrees:
                if t == len(self._parallelTrees):
                    comma = ''
                string += str(t) + '-vel' + comma
            self.run_in_loop(self.makeJsonValue(string, norm, ''))
            
    def averageSpeed(self, debug=False):
        """ calculate the average speed of the notes played 
        
        """
        value = np.average(np.diff(self._deltaMemory))
        
        if debug:
            print('averge speed:', value, 'mem:', self._deltaMemory);

        if len(self._parallelTrees) == 0:
            self.run_in_loop(self.makeJsonValue(self.currentTree(), value, '-speed'))
        else:
            string = ''
            comma = ','
            for t in self._parallelTrees:
                if t == len(self._parallelTrees):
                    comma = ''
                string += str(t) + '-speed' + comma
            self.run_in_loop(self.makeJsonValue(string, value, ''))
                
    def meanRegister(self, minval=37, maxval=108, maxscale=10):
        """ calculate the mean register of the played notesn a normalized value between minval-maxval"""
        a = np.average(self._memory)
        norm = (a-minval)/(maxval-minval) * maxscale
                
        return int(round(norm))       
      
    def console(self, string, permanent=False):
        """ send a string to the console websocket"""
        if not permanent:
            self.run_in_loop(self.makeJson('console', string))        
        else:
            self.run_in_loop(self.makeJson('consoleStatus', string))             
        
    def makeJsonValue(self, display, value, wstype='-vel'):
        """ make a Json object for sending a Value"""   
        return self.mapping.prepareJsonValue(wstype=wstype, display=str(display), payload=value)

    