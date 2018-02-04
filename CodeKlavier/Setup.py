import time
import rtmidi

class BColors:
    """Class with background colors for the terminal.
    """
    HEADER = '\033[95m'
    CKBLUE = '\033[94m'
    CKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Setup(object):

    def __init__(self):
        self.__midiin = rtmidi.MidiIn()
        self.__midiout = rtmidi.MidiOut()
        self.__ports = self.__midiin.get_ports()
        self.__ports_out = self.__midiout.get_ports()

    def print_lines(self, length, lines):
        for i in range(1, lines):
            num = length+(1)
            print('##'*num)
            #TODO: add codeKlavier logo
            time.sleep(0.2)

    def print_welcome(self, length):
        for i in range(1, 5):
            num = length+(1)
            print('##'*num)
            #TODO: add codeKlavier logo
            time.sleep(0.2)

        print("\nWelcome to the Codeklavier!\n")

    def show_ports(self):
        print("These are your detected MIDI devices:", '\n')
        for port in self.__ports:
            print(self.__ports.index(port), " -> ", port)

    def get_port_from_user(self):
        selected_midiport = -1
        while selected_midiport < 0:
            try:
                choice = input("Please choose the MIDI device (number) you want to use and hit Enter:")
                selected_midiport = int(choice)
                if selected_midiport < 0 or selected_midiport >= len(self.__ports):
                    print("Invalid number, please try again:")
                    selected_midiport = -1
                else:
                    return selected_midiport
            except KeyboardInterrupt:
                print('\n', "You want to quit? ¯\('…')/¯  ok, Bye bye.")
                exit()
            except ValueError:
                print("Sorry, type a valid port numer!")

    def open_port(self, pnum):
        print("You have chosen: ", self.__ports[pnum])

        if self.__ports:
            #TODO: do we need to check on the existence of ports?
            self.__midiin.open_port(pnum)
            # ignore sysex, timing but not active sense messages
            self.__midiin.ignore_types(True, True, False)            
        else:
            raise Exception("No midi ports! Maybe open a virtual device?")

    def open_port_out(self, num):
        print("opened midi out port")

        if self.__ports_out:
            self.__midiout.open_port(num)

    def close_port(self):
        self.__midiin.close_port()
        #TODO: add close out port too

    def get_message(self):
        return self.__midiin.get_message()

    def send_message(self, message):
        return self.__midiout.send_message(message)

    def set_callback(self,cb):
        self.__midiin.set_callback(cb)

    def get_device_id(self):
        print("Hit any note to get the device_id.")
        while True:
            msg = self.get_message()
            if msg:
                message, deltatime = msg
                if message[0] != 254: #active sense ignore                
                    device_id = message[0]
                    if device_id:
                        return device_id
            time.sleep(0.01)

    def perform_setup(self):
        self.print_welcome(20)
        self.show_ports()
        myPort = self.get_port_from_user()
        return myPort

    def end(self):
        #print("Bye bye from CodeKlavier setup :(")
        self.close_port()
        del self.__midiin

def main():
    codeK = Setup()
    my_midiport = codeK.perform_setup()
    codeK.open_port(my_midiport)

    if my_midiport >= 0:
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
            codeK.end()

if __name__ == "__main__":
    main()
