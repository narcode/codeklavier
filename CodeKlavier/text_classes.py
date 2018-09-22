"""
classes for the Buffered Text Typer.
Done For the Huyens Festival 2018 to type poems by Constantijn Huygens

"""
import rtmidi
from Mapping import Mapping_Ckalculator


class TextPrint(object):
    """ class to type one character of a pre-loaded text on every midi note on event
    """

    def __init__(self, port, noteonid, pedal_id, text_id):
        """Setup the class

        :param int port: the portnumber
        :param int dict mapping: the mapping to use
        :param int noteonid: the note-on id
        :param int text_id: the id of the text to load
        """
        self.mapscheme = Mapping_Ckalculator(True, False)
        self.port = port
        self.noteonid = noteonid
        self.pedalid = pedal_id
        self.text = text_id
        self.counter = 0

    def printText(self, event, data=None):
        """Deal with the call function

        :param event: ?
        :param data: ?
        """
        message, deltatime = event
        if message[0] != 254:
            if (message[0] == self.noteonid and message[2] > 0):
                text = self.loadText(text_id=self.text)
                
                if self.counter < len(text):
                    print(text[self.counter])
                    self.mapscheme.formatAndSend(text[self.counter], display=1, spacing=False, spacechar='')
                
                self.counter += 1
                
            #if (message[0] == self.pedalid):
                #print("pedal event handler not defined yet")
                    
    def loadText(self, path=None, text_id=1):
        """ Load a text from a file
        
        :param path string: the path to the file containing the text
        "param text_id int: choose the text to load
        TODO: add loading, now it's hardcoded text
        """
        if text_id == '1':
            text = 'OP MIJNEN GEBOORT-DAGH\n\n\
Noch eens September, en noch eens die vierde dagh\n\
Die mij verschijnen sagh!\n\
Hoe veel Septembers, Heer, en hoe veel’ vierde dagen\n\
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
        else:
            text = 'DROOMEN YDELHEIT\n\n\
Wie weet wat droomen is? ick weet het; en wie niet,\n\
Die op sijn selven, neen; die in syn selven siet?\n\
Siet innewaerts, en denckt wat dencken is: dat’s droomen.\n\
Die sonder dencken is, is aen syn’ dood gekomen.\n\
Maer slapen scheelt soo veel van dood zijn, als de dood\n\
Van swijmen, en ’t geroll, van ’tliggen van een’ kloot.\n\
Wij dencken slapende: maer dampen die doen slapen\n\
Doen dat wij ons in ons aen schaduwen vergapen.\n\
De Reden doet wat, maer belemmert en verwert;\n\
Soo komt dat droomen ernst, en dencken duncken werdt.\n\
Gaet en bouwt redenen van hopen of van schroomen\n\
Op bij de Sonn of by de Maen gesufte droomen:\n\
Wat dunckt u, is ’t niet seer all eenerley gedrocht,\n\
Of wat ick hebb gedacht, of wat mij heeft gedocht?'
            
        return text
