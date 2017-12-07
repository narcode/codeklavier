import time

from .Setup import BColors

class Instructions(object):

    def __init__(self):
        self.finished = "narcode"

    def print_lines(self, length, lines):
        for i in range(1, lines):
            num = length+(1)
            print('##'*num + BColors.ENDC)
            #TODO: add codeKlavier logo
            time.sleep(0.2)

    def print_welcome(self):
        print("\nWelcome to the CODEKLAVIER 'hello world' installation!\n")

    def print_header(self):
        print(BColors.HEADER + "CODEKLAVIER IS READY AND LISTENING!" + BColors.ENDC + "\nDon't forget to groove along and have a good time!")

    def print_intro(self):
        print("\nHOW IT WORKS: \n\n* All Coding commands start on a new line with a " + BColors.HEADER + "~ " + BColors.ENDC + "and end with a" + BColors.HEADER + " .play" + BColors.ENDC + " to sound.\n* A " + BColors.HEADER + ".stop" + BColors.ENDC + " you can imagine.")
        print("* To re-evaluate a command it should finish with a " + BColors.HEADER + ".stop.play" + BColors.ENDC + " .\n* You can make numbers (n) by repeating 2 different notes more than twice (a tremolo) in the lower part of the piano. \n* You can also add or subtract numbers with the + and -\nand use the keys marked with 1 2 and 3 to derive your desired values.\n* At the top of the keyboard you will find the " + BColors.HEADER + "'Enter'" + BColors.ENDC + " and " + BColors.HEADER + "'Backspace' " + BColors.ENDC + "keys.\n* Don't forget to groove along and have a good time!\n\n")

    def mode(self):
            try:
                command = input("Do you want to run the tutorial? y/n:\n")
                if command == "y" or command == "Y":
                    self.do_tutorial()
                    command = input("Do you want to run the tutorial again? y/n:\n")
                    if command == "y" or command == "Y":
                        self.do_tutorial()
                    elif command == "n" or command == "N":
                        return True
                elif command == "n" or command == "N":
                    self.do_header()
            except ValueError:
                    print("please type 'y' or 'n'...\n")

    def start_levels(self):
        self.print_lines(20,2)
        print(BColors.BOLD + "step 0:" + BColors.ENDC)
        self.print_lines(20,2)
        next_level = -1
        while next_level < 0:
            try:
                input("The very top note is" + BColors.HEADER + " ⏎ (Enter)" + BColors.ENDC + ". All commands MUST start in a new line. Press Enter now.\n")
                time.sleep(0.1)
                next_level = 1
                self.level_one()
            except ValueError:
                print("try again...\n")

    def level_one(self):
        print('')
        self.print_lines(20,2)
        print(BColors.BOLD + "step 1:"+ BColors.ENDC)
        self.print_lines(20,2)
        next_level = -1
        while next_level < 0:
            try:
                command = input("To make your first sound play "+BColors.HEADER+"~hello1.play"+BColors.ENDC+":\n")
                if command == "~hello1.play":
                    next_level = 1
                    self.level_two()
                else:
                    print("try again...\n")
            except ValueError:
                    print("try again...\n")

    def level_two(self):
        print('')
        self.print_lines(20,2)
        print(BColors.BOLD + "step 2:"+BColors.ENDC)
        self.print_lines(20,2)
        next_level = -1
        next_com = -1
        while next_level < 0:
            try:
                command = input("Add an extra layer with"+BColors.HEADER+" ~hello2.play"+BColors.ENDC+":\n")
                if command == "~hello2.play":
                    while next_com < 0:
                        try:
                            com2 = input("\nnow add the 3rd layer with "+BColors.HEADER+"~hello3.play"+BColors.ENDC+":\n")
                            if com2 == "~hello3.play":
                                next_com = 1
                                next_level = 1
                                self.level_three()
                            else:
                                print("try again...\n")
                        except ValueError:
                                print("try again...\n")
                else:
                    print("try again...\n")
            except ValueError:
                    print("try again...\n")

    def level_three(self):
        print('')
        self.print_lines(20,2)
        print(BColors.BOLD + "step 3:"+BColors.ENDC)
        self.print_lines(20,2)
        next_level = -1
        while next_level < 0:
            try:
                command = input("Change the pitch of ~hello1 by playing "+BColors.HEADER+"~h1o=3"+BColors.ENDC+"\nTry a tremolo between the notes C-Eb in the low register:\n")
                if command == "~h1o=3":
                    next_level = 1
                    self.level_four()
                else:
                    print(BColors.WARNING+"\nDid you do a tremolo to type the 3? try again...\n"+BColors.ENDC)
            except ValueError:
                    print("try again...\n")

    def level_four(self):
        print('')
        self.print_lines(20,2)
        print(BColors.BOLD + "step 4:"+BColors.ENDC)
        self.print_lines(20,2)
        print("Yey, We are halfway through this mini introduction!\n")
        next_level = -1
        while next_level < 0:
            try:
                command = input("To change the tempo play "+BColors.HEADER+"t.tempo=n"+BColors.ENDC+"\nfor example: "+BColors.HEADER+"t.tempo=2:\n"+BColors.ENDC)
                if command == "t.tempo=2":
                    print("Great! Now it's twice as fast!\n")
                    next_level = 1
                    self.level_five()
                else:
                    print(BColors.WARNING+"\nDid you change the tempo to 2? try again...\n"+BColors.ENDC)
            except ValueError:
                    print("try again...\n")

    def level_five(self):
        print('')
        self.print_lines(20,2)
        print(BColors.BOLD + "step 5:"+BColors.ENDC)
        self.print_lines(20,2)
        next_level = -1
        while next_level < 0:
            try:
                command = input("To start an ostinato play "+BColors.HEADER+"~ost1.play"+BColors.ENDC+"\n\nPlay "+BColors.HEADER+"~ost1.play:\n"+BColors.ENDC)
                if command == "~ost1.play":
                    next_level = 1
                    self.level_six()
                else:
                    print("try again...\n")
            except ValueError:
                    print("try again...\n")

    def level_six(self):
        print('')
        self.print_lines(20,2)
        print(BColors.BOLD + "step 6:"+BColors.ENDC)
        self.print_lines(20,2)
        print("Well done! You are almost done mastering the commands of the CodeKlavier!:\n")
        next_level = -1
        next_com = -1
        while next_level < 0:
            try:
                command = input("To make the ostinato sound higher, open the pedal listener by playing ~op=n.\nPlay "+BColors.HEADER+"~op1=1"+BColors.ENDC+"\n(remember the 1 is played with a tremolo of a minor second. For example A-Ab):\n")
                if command == "~op1=1":
                    print(BColors.HEADER+"Push the right pedal down "+BColors.ENDC+"and up at various degrees and listen to the ostinato modulate.\n")
                    time.sleep(5)
                    while next_com < 0:
                        try:
                            com2 = input("If you like the pitch, "+BColors.HEADER+"stop the listener"+BColors.ENDC+". You need to close it by changing the value of ~op to a negative value (-n),\nthus playing "+BColors.HEADER+"~op1=2-3\n"+BColors.ENDC)
                            if com2 == "~op1=2-3":
                                time.sleep(0.5)
                                next_com = 1
                                next_level = 1
                                self.level_seven()
                            else:
                                print(BColors.WARNING+"\nDid you do the substraction with tremolos? Please try again...\n"+BColors.ENDC)
                        except ValueError:
                                print("try again...\n")
                else:
                    print("try again...\n")
            except ValueError:
                    print("try again...\n")

    def level_seven(self):
        print('')
        self.print_lines(20,2)
        print(BColors.BOLD + "step 7:"+BColors.ENDC)
        self.print_lines(20,2)
        print("Congratulations! You are at the last step of this mini CodeKlavier Tutorial!\nLet’s try some effects!\n")
        time.sleep(2)
        next_level = -1
        next_com = -1
        while next_level < 0:
            try:
                command = input("You can also make effects to the sound of the ~hellos. Each ~hello has a different corresponding effect.\nTo try it out you must open the effect channel for the ~hello1 by playing "+BColors.HEADER+"~afx2=n"+BColors.ENDC+", where"+BColors.HEADER+" n"+BColors.ENDC+" determines the volume of the effect.\nPlay "+BColors.HEADER+"~afx1=4\n"+BColors.ENDC)
                if command == "~afx1=4":
                    while next_com < 0:
                        try:
                            com2 = input("To control the delay rate of the effect, you should play "+BColors.HEADER+"~del1=6\n"+BColors.ENDC)
                            if com2 == "~del1=6":
                                next_com = 1
                                next_level = 1
                                self.end_levels()
                            else:
                                print("try again...\n")
                        except ValueError:
                                print("try again...\n")
                else:
                    print("try again...\n")
            except ValueError:
                    print("try again...\n")

    def end_levels(self):
        print('')
        self.print_lines(20,2)
        print(BColors.BOLD + "All right! You are ready to CodeKlavier away! as a tip, look for interesting grooves and harmonies. Enjoy!\n"+BColors.ENDC)
        self.print_lines(20,2)
        #lock it here
        self.print_intro()


    def do_tutorial(self):
        try:
            self.print_lines(20, 2)
            self.print_welcome()
            self.print_lines(20, 2)
            self.print_intro()
            self.start_levels()
            # self.end_levels()
            return True
        except KeyboardInterrupt:
            print('\nTutorial cancelled.')
        finally:
            return True

    def do_header(self):
        self.print_lines(20,3)
        self.print_header()
        self.print_lines(20,3)
        print('')
