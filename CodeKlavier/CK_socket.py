#!/usr/bin/env python3

"""
CK listening server to display code from a specific piano register.

* originally used for Madrid INSONORA Festival 2018

TODO: Classify this
"""

import socket
import getopt
import sys
import re
import time

# Gui
from threading import Thread
import tkinter
ck_display = {}
f = {}

# Gui settings (TODO: move to an ini or config file)
normal = {'relief': tkinter.SUNKEN, 'bd': 5, 'highlightbackground': 'white', 'highlightthickness': 4, 'background': 'black', 'fg': 'cyan'}
flash = {'relief': tkinter.RAISED, 'bd': 0, 'highlightbackground': 'cyan', 'highlightthickness': 15}

#server socket
listen = True
s = {}
codedump = {}
s['1'] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s['2'] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s['3'] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s['4'] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s['5'] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#s.setblocking(False)

def main():
    """
    create the UDP server and display based on commandline arguments
    """
    global root, display

    display = 0
    top = False

    try:
        options, args = getopt.getopt(sys.argv[1:],'hd:t',['help', 'display='])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    for o, a in options:
        if o in ('-h', '--help'):
            showUsage()
            sys.exit(2)
        elif o == '-t':
            top = True
        elif o in ('-d', '--display'):
                try:
                    if int(a) < 6 and int(a) > 0:
                        display = a
                    else:
                        print('argument should be either 1, 2, 3, 4 or 5')
                        sys.exit(2)
                except ValueError:
                    print('argument should be either 1, 2, 3, 4 or 5')
                    sys.exit(2)
        else:
            assert False, 'unhandled option'

    if int(display) > 0:
        # Gui window
        root = tkinter.Tk()
        root.title('CK PARALLEL CODING DISPLAY')
        root.attributes('-topmost', top)
        root.geometry("1920x900")
        root.config(background=normal.get('background'))

        # onClose event:
        root.protocol("WM_DELETE_WINDOW", stopThreads)

    if int(display) == 1:
        # TODO: use settings files to configure ck_diplay (like code block for int(display)=5
        f[display] = tkinter.Frame(root, height=900, width=1920)
        f[display].pack(fill=tkinter.BOTH, side=tkinter.LEFT)
        f[display].pack_propagate(1)
        ck_display[display] = tkinter.Text(f[display], height=6, width=150)
        ck_display[display].pack(fill=tkinter.Y, side=tkinter.LEFT)
        ck_display[display].configure(bg='black',fg='white',wrap=tkinter.WORD,spacing1=0.3, font='MENLO 25')

        ck_display[display].insert(tkinter.END, "\n")
        s[display].bind(('localhost', 1111))
        print('CK display 1 listening on port 1111')

        # display thread:
        codedump[display] = Thread(target=displayCode, args=('1'))
        codedump[display].start()

        tkinter.mainloop()
        closeDisplay(display)

    elif int(display) == 2:
        print('CK displays 1 & 2 listening on port 1111 & 2222')

        for x in range(1, int(display)+1):

            s[str(x)].bind(('localhost', x*1111))

           # TODO: use settings files to configure ck_diplay (like code block for int(display)=5
            f[str(x)] = tkinter.Frame(root, height=900, width=1920/2)
            f[str(x)].pack(fill=tkinter.Y, side=tkinter.LEFT)
            f[str(x)].pack_propagate(0)
            ck_display[str(x)] = tkinter.Text(f[str(x)], height=6, width=50)
            ck_display[str(x)].pack(fill=tkinter.Y, side=tkinter.LEFT)
            ck_display[str(x)].configure(bg='black',fg='cyan',wrap=tkinter.WORD,spacing1=0.3, font='MENLO 20')
            ck_display[str(x)].insert(tkinter.END, "Snippet "+str(x)+" \n")

            codedump[str(x)] = Thread(target=displayCode, args=(str(x)))
            codedump[str(x)].start()

        tkinter.mainloop()
        closeDisplay(display)

    elif int(display) == 3:
        print('CK displays 1-3 used for CKalculator legacy', 'Listening on ports 1111, 2222 & 3333')

        root.geometry("1920x400")
        s_width = root.winfo_screenwidth()
        s_height = root.winfo_screenheight()

        for x in range(1, int(display)+1):

            s[str(x)].bind(('localhost', x*1111))

            f[str(x)] = tkinter.Frame(root, height=s_height, width=s_width/3)
            f[str(x)].pack(fill=tkinter.Y, side=tkinter.LEFT)
            f[str(x)].pack_propagate(0)
            f[str(x)].configure(bg='black', bd=3)

            ck_display[str(x)] = tkinter.Text(f[str(x)], height=6, width=50)
            ck_display[str(x)].pack(expand=True, fill=tkinter.BOTH)
            #ck_display[display].tag_config('var', foreground='white')

            # syntax colors
            ck_display[str(x)].tag_config('add', foreground='cyan')
            ck_display[str(x)].tag_config('min', foreground='white')
            ck_display[str(x)].tag_config('div', foreground='#b3649d')
            ck_display[str(x)].tag_config('mul', foreground='#6477b3')
            ck_display[str(x)].tag_config('eval', foreground='#67b371')
            ck_display[str(x)].tag_config('pred', foreground='#ebb18a')
            ck_display[str(x)].tag_config('succ', foreground='#a3a3a3')
            ck_display[str(x)].tag_config('zero', foreground='#eb218a')
            ck_display[str(x)].tag_config('result', foreground='green')
            ck_display[str(x)].tag_config('equal', foreground='green')
            ck_display[str(x)].tag_config('gt', foreground='green')
            ck_display[str(x)].tag_config('lt', foreground='green')
            ck_display[str(x)].tag_config('int', foreground='white')
            ck_display[str(x)].tag_config('error', foreground='red', font='MENLO 60')
            ck_display[str(x)].tag_config('e_debug', foreground='red', font='MENLO 20')
            ck_display[str(x)].tag_config('r_debug', foreground='cyan', font='MENLO 20')


           # TODO: use settings files to configure ck_diplay (like code block for int(display)=5
            if x == 1:
                ck_display[str(x)].configure(bg='black', bd=5, fg='cyan',wrap=tkinter.WORD,spacing1=0.3, font='MENLO 20', relief=tkinter.SUNKEN)
                ck_display[str(x)].insert(tkinter.END, "Functions \n")
            elif x == 2:
                ck_display[str(x)].configure(bg='black', bd=5, fg='cyan',wrap=tkinter.WORD,spacing1=0.3, font='MENLO 20', relief=tkinter.SUNKEN)
                ck_display[str(x)].insert(tkinter.END, "Stack \n")
            elif x == 3:
                ck_display[str(x)].configure(bg='black', bd=5, fg='cyan',wrap=tkinter.WORD,spacing1=0.3, font='MENLO 80', relief=tkinter.SUNKEN)
                ck_display[str(x)].insert(tkinter.END, "Result \n")


            codedump[str(x)] = Thread(target=displayCode, args=(str(x)))
            codedump[str(x)].start()

        tkinter.mainloop()
        closeDisplay(display)

    elif int(display) == 4:
        print('CK displays 1-4 used for CKalculator. Listening on ports 1111, 2222, 3333, 4444')

        root.geometry("1920x400")
        s_width = root.winfo_screenwidth()
        s_height = root.winfo_screenheight()

        for x in range(1, int(display)+1):

            s[str(x)].bind(('localhost', x*1111))

            f[str(x)] = tkinter.Frame(root, height=s_height, width=s_width/4)
            f[str(x)].pack(fill=tkinter.Y, side=tkinter.LEFT)
            f[str(x)].pack_propagate(0)
            f[str(x)].configure(bg='white', bd=3)

        for x in range(1, int(display)+1):

            if x == 1:
                ck_display['title'+str(x)] = tkinter.Text(f['1'], height=1, width=50)
                ck_display['title'+str(x)].pack(expand=False, fill=tkinter.BOTH)
                ck_display[str(x)] = tkinter.Text(f['1'], height=6, width=50)
                ck_display[str(x)].pack(expand=True, fill=tkinter.BOTH)
            elif x == 2:
                ck_display['title'+str(x)] = tkinter.Text(f['2'], height=1, width=50)
                ck_display['title'+str(x)].pack(expand=False, fill=tkinter.BOTH)
                ck_display[str(x)] = tkinter.Text(f['2'], height=6, width=50)
                ck_display[str(x)].pack(expand=True, fill=tkinter.BOTH)
            elif x == 3:
                ck_display['title'+str(x)] = tkinter.Text(f['3'], height=1, width=50)
                ck_display['title'+str(x)].pack(expand=False, fill=tkinter.BOTH)
                ck_display[str(x)] = tkinter.Text(f['3'], height=6, width=50)
                ck_display[str(x)].pack(expand=True, fill=tkinter.BOTH)
            elif x == 4:
                ck_display['title'+str(x)] = tkinter.Text(f['4'], height=1, width=50)
                ck_display['title'+str(x)].pack(expand=False, fill=tkinter.BOTH)
                ck_display[str(x)] = tkinter.Text(f['4'], height=6, width=50)
                ck_display[str(x)].pack(expand=True, fill=tkinter.BOTH)

            # syntax colors
            ck_display[str(x)].tag_config('add', foreground='cyan')
            ck_display[str(x)].tag_config('min', foreground='black')
            ck_display[str(x)].tag_config('div', foreground='#b3649d')
            ck_display[str(x)].tag_config('mul', foreground='#6477b3')
            ck_display[str(x)].tag_config('eval', foreground='#67b371')
            ck_display[str(x)].tag_config('pred', foreground='#ebb18a')
            ck_display[str(x)].tag_config('succ', foreground='black')
            ck_display[str(x)].tag_config('zero', foreground='#eb218a')
            ck_display[str(x)].tag_config('result', foreground='green')
            ck_display[str(x)].tag_config('equal', foreground='green')
            ck_display[str(x)].tag_config('gt', foreground='green')
            ck_display[str(x)].tag_config('lt', foreground='green')
            ck_display[str(x)].tag_config('int', foreground='black')
            ck_display[str(x)].tag_config('error', foreground='red', font='MENLO 60')
            ck_display[str(x)].tag_config('e_debug', foreground='red', font='MENLO 20')
            ck_display[str(x)].tag_config('r_debug', foreground='cyan', font='MENLO 20')
            ck_display[str(x)].tag_config('function', foreground='black', font='MENLO 20')
            ck_display[str(x)].tag_config('saved', foreground='cyan', font='MENLO 20')


            if x == 1:
                #ck_display[str(x)].configure(bg='black', bd=5, fg='cyan',wrap=tkinter.WORD,spacing1=0.3, font='MENLO 20', relief=tkinter.SUNKEN)
                #ck_display[str(x)].insert(tkinter.END, "λ Functions \n")
                ck_display['title'+str(x)].configure(bg='white', bd=5, fg='cyan',wrap=tkinter.WORD,spacing1=0.3, font='MENLO 30', relief=tkinter.SUNKEN)
                ck_display['title'+str(x)].insert(tkinter.END, "λ Functions \n\n", 'title')
                ck_display[str(x)].configure(bg='white', bd=5, fg='cyan',wrap=tkinter.WORD,spacing1=0.3, font='MENLO 20', relief=tkinter.SUNKEN)
                ck_display[str(x)].insert(tkinter.END, "", 'title')
            elif x == 2:
                ck_display['title'+str(x)].configure(bg='white', bd=5, fg='cyan',wrap=tkinter.WORD,spacing1=0.3, font='MENLO 30', relief=tkinter.SUNKEN)
                ck_display['title'+str(x)].insert(tkinter.END, "Stack \n\n", 'title')
                ck_display[str(x)].configure(bg='white', bd=5, fg='cyan',wrap=tkinter.WORD,spacing1=0.3, font='MENLO 20', relief=tkinter.SUNKEN)
                ck_display[str(x)].insert(tkinter.END, "", 'title')
            elif x == 3:
                ck_display['title'+str(x)].configure(bg='white', bd=5, fg='cyan',wrap=tkinter.WORD,spacing1=0.3, font='MENLO 60', relief=tkinter.SUNKEN)
                ck_display['title'+str(x)].insert(tkinter.END, "Result \n\n", 'title')
                ck_display[str(x)].configure(bg='white', bd=5, fg='cyan',wrap=tkinter.WORD,spacing1=0.3, font='MENLO 80', relief=tkinter.SUNKEN)
                ck_display[str(x)].insert(tkinter.END, "", 'title')

                #ck_display[str(x)].configure(bg='black', bd=5, fg='cyan',wrap=tkinter.WORD,spacing1=0.3, font='MENLO 80', relief=tkinter.SUNKEN)
                #ck_display[str(x)].insert(tkinter.END, "Result \n")
            elif x == 4:
                ck_display['title'+str(x)].configure(bg='white', bd=5, fg='cyan',wrap=tkinter.WORD,spacing1=0.3, font='MENLO 30', relief=tkinter.SUNKEN)
                ck_display['title'+str(x)].insert(tkinter.END, "Piano functions \n\n", 'title')
                ck_display[str(x)].configure(bg='white', bd=5, fg='cyan',wrap=tkinter.WORD,spacing1=0.3, font='MENLO 80', relief=tkinter.SUNKEN)
                ck_display[str(x)].insert(tkinter.END, "", 'title')


            codedump[str(x)] = Thread(target=displayCode, args=(str(x)))
            codedump[str(x)].start()


        tkinter.mainloop()

        closeDisplay(display)

    elif int(display) == 5:
        print('CK displays 1-5 listening on ports 1111, 2222, 3333, 4444, 5555')

        s_width = root.winfo_screenwidth()
        s_height = root.winfo_screenheight()

        for x in range(1, int(display)):

            print('x is: ', x);

            s[str(x)].bind(('localhost', x*1111))

            f[str(x)] = tkinter.Frame(root, height=s_height, width=s_width/4)
            f[str(x)].pack(fill=tkinter.NONE, side=tkinter.LEFT)
            f[str(x)].pack_propagate(0)
            f[str(x)].configure(bg='black', bd=3)

        for x in range(1, int(display)):

            if x == 1:
                ck_display['title'+str(x)] = tkinter.Text(f['1'], height=1, width=50)
                ck_display['title'+str(x)].pack(expand=False, fill=tkinter.BOTH)
                ck_display[str(x)] = tkinter.Text(f['1'], height=6, width=50)
                ck_display[str(x)].pack(expand=True, fill=tkinter.BOTH)
            elif x == 2:
                ck_display['title'+str(x)] = tkinter.Text(f['2'], height=1, width=50)
                ck_display['title'+str(x)].pack(expand=False, fill=tkinter.BOTH)
                ck_display[str(x)] = tkinter.Text(f['2'], height=6, width=50)
                ck_display[str(x)].pack(expand=True, fill=tkinter.BOTH)
            elif x == 3:
                ck_display['title'+str(x)] = tkinter.Text(f['3'], height=1, width=50)
                ck_display['title'+str(x)].pack(expand=False, fill=tkinter.BOTH)
                ck_display[str(x)] = tkinter.Text(f['3'], height=6, width=50)
                ck_display[str(x)].pack(expand=True, fill=tkinter.BOTH)
            elif x == 4:
                ck_display['title'+str(x)] = tkinter.Text(f['4'], height=1, width=50)
                ck_display['title'+str(x)].pack(expand=False, fill=tkinter.BOTH)
                ck_display[str(x)] = tkinter.Text(f['4'], height=6, width=50)
                ck_display[str(x)].pack(expand=True, fill=tkinter.BOTH)
            elif x == 5:
                ck_display['title'+str(x)] = tkinter.Text(f['5'], height=1, width=50)
                ck_display['title'+str(x)].pack(expand=False, fill=tkinter.BOTH)
                ck_display[str(x)] = tkinter.Text(f['5'], height=6, width=50)
                ck_display[str(x)].pack(expand=True, fill=tkinter.BOTH)

            # syntax colors
            ck_display[str(x)].tag_config('title', foreground='cyan')
            ck_display[str(x)].tag_config('snippets', foreground='white')
            ck_display[str(x)].tag_config('low', foreground='#b3649d')
            ck_display[str(x)].tag_config('mid', foreground='#6477b3')
            ck_display[str(x)].tag_config('hi', foreground='#67b371')
            ck_display[str(x)].tag_config('primitive', foreground='#ebb18a')
            ck_display[str(x)].tag_config('comment', foreground='#a3a3a3')
            ck_display[str(x)].tag_config('loop', foreground='cyan')
            ck_display[str(x)].tag_config('warning', foreground='red', font='MENLO 30')
            ck_display[str(x)].tag_config('boom', foreground='red', font='MENLO 30')
            ck_display[str(x)].tag_config('loop2', foreground='#80f7a6')
            ck_display[str(x)].tag_config('loop3', foreground='#00b3ff')


            if x ==1:
                ck_display['title'+str(x)].configure(bg=normal.get('background'),
                                                     bd=normal.get('bd'),
                                                     fg=normal.get('fg'),
                                                     wrap=tkinter.WORD,
                                                     spacing1=0.3,
                                                     font='MENLO 30',
                                                     relief=normal.get('relief'))
                ck_display['title'+str(x)].insert(tkinter.END, "Disklavier\n\n", 'title')
                ck_display[str(x)].configure(bg=normal.get('background'),
                                             highlightbackground=normal.get('highlightbackground'),
                                             highlightthickness=normal.get('highlightthickness'),
                                             bd=normal.get('bd'),
                                             fg=normal.get('fg'),
                                             wrap=tkinter.WORD,
                                             spacing1=0.3,
                                             font='MENLO 20',
                                             relief=normal.get('relief'))
                ck_display[str(x)].insert(tkinter.END, "", 'title')
            elif x == 2:
                ck_display['title'+str(x)].configure(bg=normal.get('background'),
                                                     bd=normal.get('bd'),
                                                     fg=normal.get('fg'),
                                                     wrap=tkinter.WORD,
                                                     spacing1=0.3,
                                                     font='MENLO 30',
                                                     relief=normal.get('relief'))
                ck_display['title'+str(x)].insert(tkinter.END, "Electronics\n\n", 'title')
                ck_display[str(x)].configure(bg=normal.get('background'),
                                             highlightbackground=normal.get('highlightbackground'),
                                             highlightthickness=normal.get('highlightthickness'),
                                             bd=normal.get('bd'),
                                             fg='magenta',
                                             wrap=tkinter.WORD,
                                             spacing1=0.3,
                                             font='MENLO 20',
                                             relief=normal.get('relief'))
                ck_display[str(x)].insert(tkinter.END, "", 'title')
            elif x == 3:
                ck_display['title'+str(x)].configure(bg=normal.get('background'),
                                                     bd=normal.get('bd'),
                                                     fg=normal.get('fg'),
                                                     wrap=tkinter.WORD,
                                                     spacing1=0.3,
                                                     font='MENLO 30',
                                                     relief=normal.get('relief'))
                ck_display['title'+str(x)].insert(tkinter.END, "Conditionals\n\n", 'title')
                ck_display[str(x)].configure(bg=normal.get('background'),
                                             highlightbackground=normal.get('highlightbackground'),
                                             highlightthickness=normal.get('highlightthickness'),
                                             bd=normal.get('bd'),
                                             fg='yellow',
                                             wrap=tkinter.WORD,
                                             spacing1=0.3,
                                             font='MENLO 20',
                                             relief=normal.get('relief'))
                ck_display[str(x)].insert(tkinter.END, "", 'title')
            elif x == 4:
                ck_display['title'+str(x)].configure(bg=normal.get('background'),
                                                     bd=normal.get('bd'),
                                                     fg=normal.get('fg'),
                                                     wrap=tkinter.WORD,
                                                     spacing1=0.3,
                                                     font='MENLO 30',
                                                     relief=normal.get('relief'))
                ck_display['title'+str(x)].insert(tkinter.END, "Loops \n\n", 'title')
                ck_display[str(x)].configure(bg=normal.get('background'),
                                             highlightbackground=normal.get('highlightbackground'),
                                             highlightthickness=normal.get('highlightthickness'),
                                             bd=normal.get('bd'),
                                             fg='cyan',
                                             wrap=tkinter.WORD,
                                             spacing1=0.3,
                                             font='MENLO 20',
                                             relief=normal.get('relief'))
                ck_display[str(x)].insert(tkinter.END, "", 'title')
            elif x == 5:
                ck_display['title'+str(x)].configure(bg=normal.get('background'),
                                                     bd=normal.get('bd'),
                                                     fg=normal.get('fg'),
                                                     wrap=tkinter.WORD,
                                                     spacing1=0.3,
                                                     font='MENLO 30',
                                                     relief=normal.get('relief'))
                ck_display['title'+str(x)].insert(tkinter.END, "Free Code\n\n", 'title')
                ck_display[str(x)].configure(bg=normal.get('background'),
                                             highlightbackground=normal.get('highlightbackground'),
                                             highlightthickness=normal.get('highlightthickness'),
                                             bd=normal.get('bd'),
                                             fg='white',
                                             wrap=tkinter.WORD,
                                             spacing1=0.3,
                                             font='MENLO 20',
                                             relief=normal.get('relief'))
                ck_display[str(x)].insert(tkinter.END, "", 'title')


            codedump[str(x)] = Thread(target=displayCode, args=(str(x)))
            codedump[str(x)].start()

        tkinter.mainloop()
        closeDisplay(display)

def stopThreads():
    """
    stop the thread handling the udp socket
    """
    global listen, root

    listen = False
    root.destroy()

def closeDisplay(display):
    """
    close the GUI window
    TODO: optimize...
    """
    if display == '1':
        s[display].sendto(bytes("Bye Bye CK", "utf-8"), ('localhost', 1111))
    elif display == '2':
        s[display].sendto(bytes("Bye Bye CK", "utf-8"), ('localhost', 2222))
        s['1'].sendto(bytes("Bye Bye CK", "utf-8"), ('localhost', 1111))
    elif display == '3':
        s[display].sendto(bytes("Bye Bye CK", "utf-8"), ('localhost', 3333))
        s['1'].sendto(bytes("Bye Bye CK", "utf-8"), ('localhost', 1111))
        s['2'].sendto(bytes("Bye Bye CK", "utf-8"), ('localhost', 2222))
    elif display == '4':
        s[display].sendto(bytes("Bye Bye CK", "utf-8"), ('localhost', 4444))
        s['1'].sendto(bytes("Bye Bye CK", "utf-8"), ('localhost', 1111))
        s['2'].sendto(bytes("Bye Bye CK", "utf-8"), ('localhost', 2222))
        s['3'].sendto(bytes("Bye Bye CK", "utf-8"), ('localhost', 3333))
    elif display == '5':
        s[display].sendto(bytes("Bye Bye CK", "utf-8"), ('localhost', 5555))
        s['1'].sendto(bytes("Bye Bye CK", "utf-8"), ('localhost', 1111))
        s['2'].sendto(bytes("Bye Bye CK", "utf-8"), ('localhost', 2222))
        s['3'].sendto(bytes("Bye Bye CK", "utf-8"), ('localhost', 3333))
        s['4'].sendto(bytes("Bye Bye CK", "utf-8"), ('localhost', 4444))

    print('\nBye Bye from the CodeKlavier display server...')
    sys.exit(0)

def showUsage():
    print('\nusage example:',
                      'python3 CK_socket -td 3\n', 't, --top: puts the window ALWAYS on top of others')

def start_flash(display):
    """
    Start a flash to the specific display

    :param int display: the display to flash to
    """
    ck_display[str(display)].configure(relief=tkinter.RAISED, bd=0, highlightbackground='cyan', highlightthickness=8)

def end_flash(display):
    """
    End a flash of display

    :param int display: the display to flash to
    """
    time.sleep(0.3)
    ck_display[str(display)].configure(relief=tkinter.SUNKEN, bd=5, highlightbackground='white', highlightthickness=2)

def displayCode(display):
    """
    Funtion to listen for incoming UDP stream.
    Handeld by parallel threads

    :param display string: the display target (1-4)
    :param syntax_color string: the tag to use for coloring the syntax (snippet, mid, hi, low, primitive, loops)
    """
    global ck_display, listen

    while listen:
        try:
            data, addr = s[display].recvfrom(1024)
            dump = data.decode()
            tagmatch = re.findall('.*:', dump)
            try:
                tag = tagmatch[0][0:-1]
            except IndexError:
                tag = ''
            if 'KILL:' in tagmatch:
                ckcode = re.sub('\nKILL:', '', dump).replace('\n', '')
                ck_display[str(display)].configure(bg=ckcode)
            elif display == '1':
                #print(str(data, 'utf-8'))
                if len(tagmatch) > 0:
                    ckcode = re.sub(''+tag+':', '', dump)
                    try:
                        if tag == 'delete':
                            ck_display[display].delete("%s-1c" % tkinter.INSERT, tkinter.INSERT)
                        elif tag == 'clear':
                            ck_display[display].delete('1.0', tkinter.END)
                        elif tag == 'boom':
                            # activating BOOM
                            ck_display[display].insert(tkinter.END, ckcode, tag)
                            ck_display[display].see(tkinter.END)
                        else:
                            # show a quick flash when evaluating a command
                            if tag in  ('snippet', 'hi', 'low', ''):
                                start_flash(display)
                                end_flash(display)
                            ck_display[display].insert(tkinter.END, ckcode, tag)
                            ck_display[display].see(tkinter.END)
                    except RuntimeError as err:
                        break
            elif display == '2':
                if len(tagmatch) > 0:
                    ckcode = re.sub(''+tag+':', '', dump)
                    try:
                        if tag == 'boom':
                            # activating BOOM
                            ck_display[display].insert(tkinter.END, ckcode, tag)
                            ck_display[display].see(tkinter.END)
                        else:
                            if tag in ('snippet', 'hi', 'low', ''):
                                start_flash(display)
                                end_flash(display)
                            ck_display[display].insert(tkinter.END, ckcode, tag)
                            ck_display[display].see(tkinter.END)
                    except RuntimeError as err:
                        break
            elif display == '3':
                if len(tagmatch) > 0:
                    ckcode = re.sub(''+tag+':', '', dump)
                    try:
                        if tag == 'result' or tag == 'error':
                            ck_display[display].delete(1.0, tkinter.END)
                            ck_display[display].insert(tkinter.END, ckcode, tag)
                        else:
                            if tag in ('primitive') or 'flash:' in ckcode:
                                start_flash(display)
                                end_flash(display)
                                ckcode = ckcode.replace('flash:', '')
                            ck_display[display].insert(tkinter.END, ckcode, tag)
                            ck_display[display].see(tkinter.END)
                    except RuntimeError as err:
                        break
            elif display == '4':
                if len(tagmatch) > 0:
                    ckcode = re.sub(''+tag+':', '', dump)
                    try:
                        if tag == 'result' or tag == 'error':
                            ck_display[display].delete(1.0, tkinter.END)
                            ck_display[display].insert(tkinter.END, ckcode, tag)
                        else:
                            if 'flash:' in ckcode:
                                start_flash(display)
                                end_flash(display)
                                ck_display[display].insert(tkinter.END, ckcode.replace('flash:', ''), 'conditional')                            
                            else:
                                ck_display[display].insert(tkinter.END, ckcode, tag)
                            ck_display[display].see(tkinter.END)
                    except RuntimeError as err:
                        break
            elif display == '5': #this is the codespace
                if len(tagmatch) > 0:
                    ckcode = re.sub(''+tag+':', '', dump)
                    try:
                        if tag == 'delete':
                            ck_display[display].delete("%s-1c" % tkinter.INSERT, tkinter.INSERT)
                        elif tag == 'evaluate':
                            start_flash(display)
                            end_flash(display)
                        else:
                            ck_display[display].insert(tkinter.END, ckcode, tag)
                            ck_display[display].see(tkinter.END)
                    except RuntimeError as err:
                        break
        except OSError as err:
            print(err)
            break

    #time.sleep(0.01)

if __name__ == '__main__':
    try:
        main()

        # show usage
        if int(display) == 0:
            showUsage()


    except KeyboardInterrupt:
        stopThreads()
        closeDisplay(display)
