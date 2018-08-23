"""
classes for the Buffered Text Typer.
Done For the Huyens Festival 2018 to type poems by Constantijn Huygens

"""
import rtmidi
from Mapping import Mapping_Ckalculator


class TextPrint(object):
    """ class to type one character of a pre-loaded text on every midi note on event
    """

    def __init__(self, port, noteonid, pedal_id):
        """Setup the class

        :param int port: the portnumber
        :param dict mapping: the mapping to use
        :param noteonid: the note-on id
        """
        self.mapscheme = Mapping_Ckalculator(True, False)
        self.port = port
        self.noteonid = noteonid
        self.pedalid = pedal_id
        self.counter = 0

    def printText(self, event, data=None):
        """Deal with the call function

        :param event: ?
        :param data: ?
        """
        message, deltatime = event
        if message[0] != 254:
            if message[2] > 0: #only noteOn
                if (message[0] == self.noteonid):
                    text = self.loadText()
                    
                    if self.counter < len(text):
                        print(text[self.counter])
                        self.mapscheme.formatAndSend(text[self.counter], display=1, spacing=False, spacechar='')
                    
                    self.counter += 1
                    
                #if (message[0] == self.pedalid):
                    #print("pedal event handler not defined yet")
                    
    def loadText(self, path=None):
        """ Load a text from a file
        
        :param path string: the path to the file containing the text
        TODO: add loading, now it's hardcoded text
        """
        text = '\nOP MIJNEN GEBOORT-DAGH\
        \n\
        \n\
Noch eens September, en noch eens die vierde dagh\
Die mij verschijnen sagh!\n\
Hoe veel Septembers, Heer, en hoe veel’ vierde dagen\
Wilt ghij mij noch verdragen?\n\
Ick bidd om geen verlang: ’tkan redelyck bestaen,\n\
Het ghen’ ick heb gegaen:\n\
En van mijn’ wiegh tot hier zijn soo veel dusend schreden\n\
Die ick heb doorgetreden,\n\
(Met vallen, lieve God, en opstaen, soo ghij weett,)\n\
Dat die all ’t selve leed\n\
En all’ de selve vreughd naer mij hadd door te reisen,\n\
Sich drijmael sou bepeisen\n\
Wat besten oorber waer, gelaten of gedaen.\n\
Mij, Heere, laet vrij gaen;\n\
Mijn’ roll is afgespeelt, en all wat kan gebeuren\n\
Van lacchen en van treuren\n\
Is mij te beurt geweest, en all wat beuren sal\n\
Sal ’tselve niet met all,\n\
En d’ oude schaduw zijn van dingen die wat schijnen\n\
En komende verdwijnen.\n\
Wat wacht ick meer op aerd, waerom en scheid’ ick niet?\n\
’K wacht, Heer, dat ghij ’tgebiedt.\n\
Maer, magh ick noch een’ gunst by d’andere begeeren,\n\
Laet mij soo scheiden leeren,\n\
Dat yeder een die ’t siet mijn scheiden en het sijn\n\
Wensch’ eenerhand te zijn.\n'
            
        return text
