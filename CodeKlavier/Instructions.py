import time

class Instructions(object):

    # def __init__(self):

    def print_lines(self, length, lines):
        for i in range(1, lines):
            num = length+(1)
            print('##'*num)
            #TODO: add codeKlavier logo
            time.sleep(0.2)

    def print_welcome(self):
        print("\nWelcome to the CODEKLAVIER 'hello world' installation!\n")


    def print_intro(self):
        print("\nHOW IT WORKS: \n\n* All Coding commands start on a new line with a ~ \nand end with a .play to sound. \n* A .stop you can imagine.")
        print("* To re-evaluate a command it should finish with a .stop.play . \n* You can make numbers (n) by repeating 2 different notes more than twice (a tremollo) in the lower part of the piano. \n* You can also add or subtract numbers with the + and -\nand use the keys marked with 1 2 and 3 to derive your desired values.\n* At the top of the keyboard you will find the 'Enter' and 'Backspace' keys.\n* Don't forget to groove along and have a good time!\n\n")

    def start_levels(self):
        self.print_lines(20,2)
        print("step 1:\n")
        next_level = -1
        while next_level < 0:
            try:
                command = input("To make your first sound play '~hello1.play': ")
                if command == "~hello1.play":
                    next_level = 1
                    self.level_two()
                else:
                    print("try again...\n")
            except ValueError:
                    print("try again...\n")

    def level_two(self):
        self.print_lines(20,3)
        print("step 2:\n")
        next_level = -1
        next_com = -1
        while next_level < 0:
            try:
                command = input("Add an extra layer with ~hello2.play: ")
                if command == "~hello2.play":
                    while next_com < 0:
                        try:
                            com2 = input("\nnow add the 3rd layer with ~hello3.play: ")
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
        self.print_lines(20,4)
        print("step 3:\n")
        print("You can change the pitch of the individual pulses for a value between 0 and 28. To allocate the new pitch play ~h1o=n  for ~hello1, ~h2o=n  for ~hello2, and ~h3o=n for ~hello3.\n")
        next_level = -1
        while next_level < 0:
            try:
                command = input("Let's try to change the pitch of ~hello1\nPlay ~h1o=3\nYou can play the '3' as a temolo of a third.\nTry a tremolo between the notes C-Eb in the low register: ")
                if command == "~h1o=3":
                    print("Nice one! keep changing pitches to find harmonies you like\n")
                    next_level = 1
                    # we exit here to send an enter
                else:
                    print("try again...\n")
            except ValueError:
                    print("try again...\n")

    def level_four(self):
        self.print_lines(20,5)
        print("step 4:\n")
        print("Yey, We are halfway through this mini introduction!\n")
        next_level = -1
        while next_level < 0:
            try:
                command = input("To change the tempo play t.tempo=n\nfor example: t.tempo=2: ")
                if command == "t.tempo=2":
                    print("Great! Now it's twice as fast!\n")
                    next_level = 1
                    self.level_five()
                else:
                    print("try again...\n")
            except ValueError:
                    print("try again...\n")

    def level_five(self):
        self.print_lines(20,6)
        print("step 5:\n")
        next_level = -1
        while next_level < 0:
            try:
                command = input("To start an ostinato play ~ost.play.\n(Later on you can launch another 2 of these ostinatos with ~ost2.play and ~ost3.play).\nPlay ~ost1.play: ")
                if command == "~ost1.play":
                    next_level = 1
                    self.level_six()
                else:
                    print("try again...\n")
            except ValueError:
                    print("try again...\n")

    def level_six(self):
        self.print_lines(20,7)
        print("step 6:\n")
        print("Well done! You are almost done mastering the commands for the CodeKlavier!:\n")
        next_level = -1
        next_com = -1
        while next_level < 0:
            try:
                command = input("To make the ostinato sound higher, open the pedal listener by playing ~op=n and find the pitch you are after by pushing the right pedal down at various degrees.\n To lock the pitch and stop the listener, you need to change the value of ~op to a negative value (-n), thus playing ~op=-n.\n This is a good time to make subtraction equations. Try it now, Play ~op1=1\n(remember the 1 is played with a tremolo of a minor second. For example A-Ab): ")
                if command == "~op1=1":
                    print("Yes! Now push down the pedal and relase it so to listen to the pitch changes...\n")
                    time.sleep(5)
                    while next_com < 0:
                        try:
                            com2 = input("Choose a pitch you like and lock it by sustaining the pedal position while playing ~op=1-3\n(play the '1' with a new minor second tremolo then the minus sign '-' followed by a tremolo of a minor third, for example G-Bb): ")
                            if com2 == "~op1=1-3":
                                print("The same can be done with ~op2 for ~ost2 and ~op3 for ~ost3.\nYou can also make the ostinato sound lower by applying the same principle of ~op but using ~neer=n and ~neer2=n or ~neer3=n respectively.\n")
                                time.sleep(3)
                                next_com = 1
                                next_level = 1
                                self.level_seven()
                            else:
                                print("try again...\n")
                        except ValueError:
                                print("try again...\n")
                else:
                    print("try again...\n")
            except ValueError:
                    print("try again...\n")

    def level_seven(self):
        self.print_lines(20,8)
        print("step 7:\n")
        print("Congratulations! You are at the last step of this mini CodeKlavier Tutorial!\n")
        time.sleep(2)
        next_level = -1
        next_com = -1
        while next_level < 0:
            try:
                command = input("Did you know that you can also make effects to the sound of the ~hellos???\nEach ~hello has a different corresponding effect.\n To try it out you must open the effect channel for the ~hello by playing ~afxN=n, where N determines the ~hello sound and n determines the volume of the effect.\nTo control the delay decay of the effect, you should play  ~delN=n.\n Let's try out an example for ~hello2:\nPlay ~afx2=4: ")
                if command == "~afx2=4":
                    while next_com < 0:
                        try:
                            com2 = input("and now ~del2=6: ")
                            if com2 == "~del2=6":
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
        self.print_lines(20,9)
        print("All right! You are ready to CodeKlavier away! as a tip, look for interesting grooves and harmonies. Enjoy!:\n")


    def do_tutorial(self):
        self.print_lines(20, 2)
        self.print_welcome()
        self.print_lines(20, 2)
        self.print_intro()
        self.start_levels()
