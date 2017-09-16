import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Instructions(object):

    def __init__(self):
        self.finished = "narcode"

    def print_lines(self, length, lines):
        for i in range(1, lines):
            num = length+(1)
            print('##'*num + bcolors.ENDC)
            #TODO: add codeKlavier logo
            time.sleep(0.2)

    def print_welcome(self):
        print("\nWelcome to the CODEKLAVIER 'hello world' installation!\n")

    def print_header(self):
        print(bcolors.HEADER + "CODEKLAVIER IS READY AND LISTENING!" + bcolors.ENDC + "\nDon't forget to groove along and have a good time!")

    def print_intro(self):
        print("\nHOW IT WORKS: \n\n* All Coding commands start on a new line with a " + bcolors.HEADER + "~ " + bcolors.ENDC + "and end with a" + bcolors.HEADER + " .play" + bcolors.ENDC + " to sound.\n* A " + bcolors.HEADER + ".stop" + bcolors.ENDC + " you can imagine.")
        print("* To re-evaluate a command it should finish with a " + bcolors.HEADER + ".stop.play" + bcolors.ENDC + " .\n* You can make numbers (n) by repeating 2 different notes more than twice (a tremolo) in the lower part of the piano. \n* You can also add or subtract numbers with the + and -\nand use the keys marked with 1 2 and 3 to derive your desired values.\n* At the top of the keyboard you will find the " + bcolors.HEADER + "'Enter'" + bcolors.ENDC + " and " + bcolors.HEADER + "'Backspace' " + bcolors.ENDC + "keys.\n* Don't forget to groove along and have a good time!\n\n")

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
        print(bcolors.BOLD + "step 0:" + bcolors.ENDC)
        self.print_lines(20,2)
        next_level = -1
        while next_level < 0:
            try:
                input("The very top note is" + bcolors.HEADER + " ⏎ (Enter)" + bcolors.ENDC + ". All commands MUST start in a new line. Press Enter now.\n")
                time.sleep(0.1)
                next_level = 1
                self.level_one()
            except ValueError:
                print("try again...\n")

    def level_one(self):
        print('')
        self.print_lines(20,2)
        print(bcolors.BOLD + "step 1:"+ bcolors.ENDC)
        self.print_lines(20,2)
        next_level = -1
        while next_level < 0:
            try:
                command = input("To make your first sound play "+bcolors.HEADER+"~hello1.play"+bcolors.ENDC+":\n")
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
        print(bcolors.BOLD + "step 2:"+bcolors.ENDC)
        self.print_lines(20,2)
        next_level = -1
        next_com = -1
        while next_level < 0:
            try:
                command = input("Add an extra layer with"+bcolors.HEADER+" ~hello2.play"+bcolors.ENDC+":\n")
                if command == "~hello2.play":
                    while next_com < 0:
                        try:
                            com2 = input("\nnow add the 3rd layer with "+bcolors.HEADER+"~hello3.play"+bcolors.ENDC+":\n")
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
        print(bcolors.BOLD + "step 3:"+bcolors.ENDC)
        self.print_lines(20,2)
        next_level = -1
        while next_level < 0:
            try:
                command = input("Change the pitch of ~hello1 by playing "+bcolors.HEADER+"~h1o=3"+bcolors.ENDC+"\nTry a tremolo between the notes C-Eb in the low register:\n")
                if command == "~h1o=3":
                    next_level = 1
                    self.level_four()
                else:
                    print(bcolors.WARNING+"\nDid you do a tremolo to type the 3? try again...\n"+bcolors.ENDC)
            except ValueError:
                    print("try again...\n")

    def level_four(self):
        print('')
        self.print_lines(20,2)
        print(bcolors.BOLD + "step 4:"+bcolors.ENDC)
        self.print_lines(20,2)
        print("Yey, We are halfway through this mini introduction!\n")
        next_level = -1
        while next_level < 0:
            try:
                command = input("To change the tempo play "+bcolors.HEADER+"t.tempo=n"+bcolors.ENDC+"\nfor example: "+bcolors.HEADER+"t.tempo=2:\n"+bcolors.ENDC)
                if command == "t.tempo=2":
                    print("Great! Now it's twice as fast!\n")
                    next_level = 1
                    self.level_five()
                else:
                    print(bcolors.WARNING+"\nDid you change the tempo to 2? try again...\n"+bcolors.ENDC)
            except ValueError:
                    print("try again...\n")

    def level_five(self):
        print('')
        self.print_lines(20,2)
        print(bcolors.BOLD + "step 5:"+bcolors.ENDC)
        self.print_lines(20,2)
        next_level = -1
        while next_level < 0:
            try:
                command = input("To start an ostinato play "+bcolors.HEADER+"~ost1.play"+bcolors.ENDC+"\n\nPlay "+bcolors.HEADER+"~ost1.play:\n"+bcolors.ENDC)
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
        print(bcolors.BOLD + "step 6:"+bcolors.ENDC)
        self.print_lines(20,2)
        print("Well done! You are almost done mastering the commands of the CodeKlavier!:\n")
        next_level = -1
        next_com = -1
        while next_level < 0:
            try:
                command = input("To make the ostinato sound higher, open the pedal listener by playing ~op=n.\nPlay "+bcolors.HEADER+"~op1=1"+bcolors.ENDC+"\n(remember the 1 is played with a tremolo of a minor second. For example A-Ab):\n")
                if command == "~op1=1":
                    print(bcolors.HEADER+"Push the right pedal down "+bcolors.ENDC+"and up at various degrees and listen to the ostinato modulate.\n")
                    time.sleep(5)
                    while next_com < 0:
                        try:
                            com2 = input("If you like the pitch, "+bcolors.HEADER+"stop the listener"+bcolors.ENDC+". You need to close it by changing the value of ~op to a negative value (-n),\nthus playing "+bcolors.HEADER+"~op1=2-3\n"+bcolors.ENDC)
                            if com2 == "~op1=2-3":
                                time.sleep(0.5)
                                next_com = 1
                                next_level = 1
                                self.level_seven()
                            else:
                                print(bcolors.WARNING+"\nDid you do the substraction with tremolos? Please try again...\n"+bcolors.ENDC)
                        except ValueError:
                                print("try again...\n")
                else:
                    print("try again...\n")
            except ValueError:
                    print("try again...\n")

    def level_seven(self):
        print('')
        self.print_lines(20,2)
        print(bcolors.BOLD + "step 7:"+bcolors.ENDC)
        self.print_lines(20,2)
        print("Congratulations! You are at the last step of this mini CodeKlavier Tutorial!\nLet’s try some effects!\n")
        time.sleep(2)
        next_level = -1
        next_com = -1
        while next_level < 0:
            try:
                command = input("You can also make effects to the sound of the ~hellos. Each ~hello has a different corresponding effect.\nTo try it out you must open the effect channel for the ~hello1 by playing "+bcolors.HEADER+"~afx2=n"+bcolors.ENDC+", where"+bcolors.HEADER+" n"+bcolors.ENDC+" determines the volume of the effect.\nPlay "+bcolors.HEADER+"~afx1=4\n"+bcolors.ENDC)
                if command == "~afx1=4":
                    while next_com < 0:
                        try:
                            com2 = input("To control the delay rate of the effect, you should play "+bcolors.HEADER+"~del1=6\n"+bcolors.ENDC)
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
        print(bcolors.BOLD + "All right! You are ready to CodeKlavier away! as a tip, look for interesting grooves and harmonies. Enjoy!\n"+bcolors.ENDC)
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
