"""CodeKlavier recording of midi events in .csv format.

For Machine Learning PIA
"""    

from CK_Setup import Setup
import time
import configparser
import re
import os


class CK_Rec(object):
    """
    Class to handle the recording of midi events in .csv format
    """

    def __init__(self, configfile='../default_setup.ini'):
        self._configfile = configfile
        self._deltamem = []
           
    def delta_difference(self, deltatime_in):   
        # activesense compensation
        ck_deltatime_mem = self._deltamem
        
        ck_deltatime_mem.append(deltatime_in)
        #print('deltatimes stack: ', ck_deltatetime_mem)
        
        if len(ck_deltatime_mem) > 2:
            ck_deltatime_mem = ck_deltatime_mem[-2:]
            
        if len(ck_deltatime_mem) == 2:
            dif = ck_deltatime_mem[1] - ck_deltatime_mem[0]
            if dif < 0:
                dif = 0
            return dif
        else:
            return 0  
    
    def record(self, framesize=10):
        """
        Run a basic miditest to see how the CodeKlavier is receiving your midi.
    
        :param string configfile: Path to the configuration file (default: default_setup.ini)
        """
        
        timestamp = time.strftime("%y-%m-%d")
        ck_deltatime = 0
        per_note = 0
        recfile = open('ml_data/_', 'w')
        headers = ''
        
        #Read config and settings
        config = configparser.ConfigParser()
        config.read(self._configfile, encoding='utf8')
      
        try:
            myPort = config['midi'].getint('port')
            note_on = config['midi'].getint('noteon_id')
            note_off = config['midi'].getint('noteoff_id')
        except KeyError:
            raise LookupError('Missing key information in the config file.')
    
        if (myPort == None or note_on == None):
            raise LookupError('Missing key information in the config file.')      
      
        codeK = Setup()
        codeK.open_port(myPort)
        print('your note on id is: ', note_on, '\n')
        print("CodeKlavier is RECORDING. Press Control-C to save and exit.")
        for i in range(0,framesize):
            if framesize == 1:
                index = ''
            else:
                index = str(i)
            headers += 'midi_note'+index+',velocity'+index+',duration'+index+',label'+index
    
        recfile.write(headers+'\n')
        data_line = ''
        deltatime_mem = {}
        ostinato_length = 9
        note_counter = 1
        
        
        try:
            while True:
                msg = codeK.get_message()
    
                if msg:
                    message, deltatime = msg
                    ck_deltatime += deltatime
                    per_note += deltatime                
                    if message[0] != 254:
                        if message[0] == note_on:
                            deltatime_mem[message[1]] = ck_deltatime
                            velocity = message[2]
                        if message[0] == note_off:
                            if note_counter > 9:
                                note_counter = 1
                            per_note = 0
                            dif = self.delta_difference(per_note)                    
                            #midimsg = list(map(str, message)) #full msg not needed
                            midinote = message[1]
                            label = count/ostinato_length
                            note_duration = ck_deltatime - deltatime_mem.pop(midinote)
                            data_line += str(midinote) + ',' + str(velocity) + ',' + str(note_duration) + ',' + str(label)
                            data_line += '\n'
                            clean_line = re.sub(r"\[?\]?", '', data_line)                
                            print(clean_line)
                            recfile.write(clean_line)
                            data_line = ''
                            note_counter += 1
                        
                time.sleep(0.01)
    
        except KeyboardInterrupt:
            print('saving recording...')
        finally:
            recfile.close()
            title = input('Dear CK user, please type a comprehensive title for the recording and press ENTER:');
            usertitle = title+'_'+timestamp+'.csv'
            os.rename("ml_data/_", "ml_data/"+usertitle)
            print("recording saved with title: ", usertitle)
            codeK.end()        
