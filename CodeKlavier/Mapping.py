import time
from pynput.keyboard import Key, Controller

class Mapping_HelloWorld:

    def __init__(self):
        print("Using the Hello World mapping")
        self.__keyboard = Controller()

    def evaluateSC(self):
        with self.__keyboard.pressed(Key.shift):
            self.__keyboard.press(Key.enter)
            self.__keyboard.release(Key.shift)

    def stopSC(self, midinumber):
        if midinumber == 66:
            self.__keyboard.press(Key.cmd)
            self.__keyboard.type('.')
            self.__keyboard.release(Key.cmd)

    def mapping(self, midinumber):
        # chars and nums
        if midinumber == 69:
            self.__keyboard.type('h')
        elif midinumber == 74:
            self.__keyboard.type('l')
        elif midinumber == 63:
            self.__keyboard.type('e')
        elif midinumber == 80:
            self.__keyboard.type('o')
        elif midinumber == 68:
            self.__keyboard.type('o')
        elif midinumber == 81:
            self.__keyboard.type('r')
        elif midinumber == 88:
            self.__keyboard.type('w')
        elif midinumber == 64:
            self.__keyboard.type('d')
        elif midinumber ==48:
            self.__keyboard.type('t')
        elif midinumber == 47:
            self.__keyboard.type('s')
        elif midinumber == 37:
            self.__keyboard.type('a')
        elif midinumber == 41:
            self.__keyboard.type('n')
        elif midinumber == 42:
            self.__keyboard.type('i')
        elif midinumber == 44:
            self.__keyboard.type('o')
        elif midinumber == 45:
            self.__keyboard.type('p')
        elif midinumber == 59:
            self.__keyboard.type('0')
        elif midinumber == 60:
            self.__keyboard.type('1')
        elif midinumber == 61:
            self.__keyboard.type('2')
        elif midinumber == 62:
            self.__keyboard.type('3')
        elif midinumber == 89:
            self.__keyboard.type('4')
        elif midinumber == 90:
            self.__keyboard.type('5')
        elif midinumber == 91:
            self.__keyboard.type('6')
        elif midinumber == 92:
            self.__keyboard.type('7')
        elif midinumber == 93:
            self.__keyboard.type('8')
        elif midinumber == 94:
            self.__keyboard.type('9')
        elif midinumber == 104:
            self.__keyboard.type('k'),
       # special keys
        elif midinumber == 56:
            self.__keyboard.press(Key.space)
            self.__keyboard.release(Key.space),
        elif midinumber == 32:
            self.__keyboard.press(Key.enter)
            self.__keyboard.release(Key.enter)
            self.evaluateSC(),
        elif midinumber == 50:
            self.__keyboard.type('~'),
        elif midinumber == 51:
            self.__keyboard.type('+'),
        elif midinumber == 54:
            self.__keyboard.type('-'),
        elif midinumber == 49:
            self.__keyboard.type('='),
        elif midinumber == 103:
            self.__keyboard.type('?'),
        elif midinumber == 105:
            self.__keyboard.type('.!'),
        elif midinumber == 95:
            self.__keyboard.press(Key.backspace)
            self.__keyboard.release(Key.backspace),
      # supercollider commands:
        elif midinumber == 33:
            self.evaluateSC(),
        elif midinumber == 22:
            self.__keyboard.type('.tempo'),
        elif midinumber == 21:
            self.__keyboard.type('.play'),
        elif midinumber == 102:
            self.__keyboard.type('TempoClock.default')

class Mapping_HelloWorld_NKK:

    def __init__(self):
        # print("Using the Hello World mapping (NKK)")
        self.__keyboard = Controller()

    def evaluateSC(self, what):
        if what == 'play':
            with self.__keyboard.pressed(Key.cmd):
                self.__keyboard.press(Key.right)
                self.__keyboard.release(Key.right)
            time.sleep(0.01)
            self.__keyboard.type('.play')
            with self.__keyboard.pressed(Key.shift):
                self.__keyboard.press(Key.enter)
                self.__keyboard.release(Key.enter)
            time.sleep(0.01)
            self.__keyboard.press(Key.enter)
            self.__keyboard.release(Key.enter)
        elif what == 'stop':
            with self.__keyboard.pressed(Key.cmd):
                self.__keyboard.press(Key.right)
                self.__keyboard.release(Key.right)
            time.sleep(0.01)
            self.__keyboard.type('.stop')
            with self.__keyboard.pressed(Key.shift):
                self.__keyboard.press(Key.enter)
                self.__keyboard.release(Key.enter)
            time.sleep(0.01)
            self.__keyboard.press(Key.enter)
            self.__keyboard.release(Key.enter)
        elif what == 'alt_eval':
            with self.__keyboard.pressed(Key.cmd):
                self.__keyboard.type('e')
                self.__keyboard.release(Key.cmd)
        elif what == 'eval':
            with self.__keyboard.pressed(Key.shift):
                self.__keyboard.press(Key.enter)
                self.__keyboard.release(Key.enter)
            time.sleep(0.01)
            self.__keyboard.press(Key.enter)
            self.__keyboard.release(Key.enter)

    def stopSC(self, midinumber):
        if midinumber == 66:
            self.__keyboard.press(Key.cmd)
            self.__keyboard.type('.')
            self.__keyboard.release(Key.cmd)

    def enter(self):
        self.__keyboard.press(Key.enter)
        self.__keyboard.release(Key.enter)

    def delete(self):
        self.__keyboard.press(Key.backspace)
        self.__keyboard.release(Key.backspace)

    def mapping(self, midinumber):
        # chars and nums
        if midinumber == 87:
            self.__keyboard.type('h')
        elif midinumber == 92:
            self.__keyboard.type('l')
        elif midinumber == 90:
            self.__keyboard.type('e')
        elif midinumber == 94:
            self.__keyboard.type('o')
        elif midinumber == 95:
            self.__keyboard.type('p')
        elif midinumber == 91:
            self.__keyboard.type('n')
        elif midinumber == 89:
            self.__keyboard.type('r')
        elif midinumber == 84:
            self.__keyboard.type('t')
        elif midinumber == 83:
            self.__keyboard.type('s')
        elif midinumber == 80:
            self.__keyboard.type('o')
        elif midinumber == 102:
            self.__keyboard.type('a')
        elif midinumber == 104:
            self.__keyboard.type('f')
        elif midinumber == 106:
            self.__keyboard.type('x')
        elif midinumber == 88:
            self.__keyboard.type('d')
        elif midinumber == 89:
            self.__keyboard.type('r')
        elif midinumber == 103:
            self.__keyboard.type('-')
        elif midinumber == 105:
            self.__keyboard.type('+')
        elif midinumber == 107:
            self.delete()
       # special keys
        elif midinumber == 85:
            self.__keyboard.type('~')
        elif midinumber == 101:
            self.__keyboard.type('=')
        elif midinumber == 98:
            self.evaluateSC('stop')
        elif midinumber == 99:
            self.__keyboard.type('.tempo')
        elif midinumber == 97:
            self.evaluateSC('play')
        elif midinumber == 108:
            self.evaluateSC('eval')
       # numbers keys
        elif midinumber == 77:
            self.__keyboard.type('1')
        elif midinumber == 79:
            self.__keyboard.type('2')
        elif midinumber == 81:
            self.__keyboard.type('3')
#        elif midinumber == 66:
#            self.stopSC()

class Mapping_Motippets:

    def __init__(self):
        print("Using the mapping for Motippets")
        self.__keyboard = Controller()

    def evaluateSC(self, what):
        if what == 'play':
            with self.__keyboard.pressed(Key.cmd):
                self.__keyboard.press(Key.right)
                self.__keyboard.release(Key.right)
            time.sleep(0.01)
            self.__keyboard.type('.play')
            with self.__keyboard.pressed(Key.shift):
                self.__keyboard.press(Key.enter)
                self.__keyboard.release(Key.enter)
            time.sleep(0.01)
            self.__keyboard.press(Key.enter)
            self.__keyboard.release(Key.enter)
        elif what == 'stop':
            with self.__keyboard.pressed(Key.cmd):
                self.__keyboard.press(Key.right)
                self.__keyboard.release(Key.right)
            time.sleep(0.01)
            self.__keyboard.type('.stop')
            with self.__keyboard.pressed(Key.shift):
                self.__keyboard.press(Key.enter)
                self.__keyboard.release(Key.enter)
            time.sleep(0.01)
            self.__keyboard.press(Key.enter)
            self.__keyboard.release(Key.enter)
        elif what == 'alt_eval':
            with self.__keyboard.pressed(Key.cmd):
                self.__keyboard.type('e')
                self.__keyboard.release(Key.cmd)
        elif what == 'eval':
            with self.__keyboard.pressed(Key.shift):
                self.__keyboard.press(Key.enter)
                self.__keyboard.release(Key.enter)
            time.sleep(0.2)
            self.__keyboard.press(Key.enter)
            self.__keyboard.release(Key.enter)

    def enter(self):
        self.__keyboard.press(Key.enter)
        self.__keyboard.release(Key.enter)

    def delete(self):
        self.__keyboard.press(Key.backspace)
        self.__keyboard.release(Key.backspace)

    def mapping(self, midinumber):
        # out of trouble with pedal:
        # TODO: check with Anne
        if midinumber == 66:
            self.evaluateSC('eval')

    def snippets(self, num):
        if num == 1:
            self.__keyboard.type('~snippet1 = Tdef(\\1, {|ev| loop{ Ndef(~name.next, {|pitch=400,fx=88| SinOsc.ar(456*LFTri.kr(fx).range(100, pitch)) * EnvGen.kr(Env.perc) * ~amp1}).play(0,2);(1/ev.rit).wait;}}).play(quant:0);')
            self.evaluateSC('eval')
        elif num == 2:
            self.__keyboard.type('~snippet2 = Ndef(\\acc, {|note=500, amp=0.1, cut=200, bw=0.5, fx=0.1| BPF.ar(Resonz.ar(SinOsc.ar([note.lag(1), note.lag(2)*3/2, note*2, note.lag(1.5)*4/3]), (note*LFTri.kr(fx).range(1/2, 8))+80, bw), 600, 0.8) * amp.lag(0.5)}).play(0,2);')
            self.evaluateSC('eval')            
    
    def miniSnippets(self, snippet_num, pianosection):
        if snippet_num == 1 and pianosection == 'hi':
            self.__keyboard.type('[\\pulse, \\pulse2, \\pulse3, \\pulse4, \\pulse5, \\pulse6].do{|i| Ndef(i).map(\\fx, Ndef(\\krm3));}')
            self.evaluateSC('eval')
        if snippet_num == 1 and pianosection == 'hi with unmap':
            self.__keyboard.type('[\\pulse, \\pulse2, \\pulse3, \\pulse4, \\pulse5, \\pulse6].do{|i| Ndef(i).map(\\fx, Ndef(\\krm3));}')
            self.evaluateSC('eval')
            #unmap other motif
            self.__keyboard.type('Ndef(\\acc).set(\\fx, ~tremoloH.linlin(1, 16, 0, 15));')
            self.evaluateSC('eval')             
        if snippet_num == 1 and pianosection == 'mid':
            self.__keyboard.type('[\\pulse, \\pulse2, \\pulse3, \\pulse4, \\pulse5, \\pulse6].do{|i| Ndef(i).map(\\pitch, Ndef(\\krm1));}')
            self.evaluateSC('eval')
        if snippet_num == 1 and pianosection == 'mid with unmap':
            self.__keyboard.type('[\\pulse, \\pulse2, \\pulse3, \\pulse4, \\pulse5, \\pulse6].do{|i| Ndef(i).map(\\pitch, Ndef(\\krm1));}')
            self.evaluateSC('eval')
            #unmap
            self.__keyboard.type('Ndef(\\acc).set(\\note, ~tremoloM.linlin(1, 16, 180, 800));')
            self.evaluateSC('eval')
        if snippet_num == 1 and pianosection == 'low':
            self.__keyboard.type('~map_rhythm = true;')
            self.evaluateSC('eval')
        if snippet_num == 1 and pianosection == 'low with unmap':
            self.__keyboard.type('~map_rhythm = true;')
            self.evaluateSC('eval')
            #unmap
            self.__keyboard.type('Ndef(\\acc).set(\\amp, ~tremoloL.linlin(1, 16, 0, 1.5));')
            self.evaluateSC('eval') 
            
        # for snippet 2:
        if snippet_num == 2 and pianosection == 'hi':
            self.__keyboard.type('Ndef(\\acc).map(\\fx, Ndef(\\krm2_3));')
            self.evaluateSC('eval')
        if snippet_num == 2 and pianosection == 'hi with unmap':
            self.__keyboard.type('Ndef(\\acc).map(\\fx, Ndef(\\krm2_3)');
            self.evaluateSC('eval')
            #unmap other motif
            self.__keyboard.type('[\\pulse, \\pulse2, \\pulse3, \\pulse4, \\pulse5, \\pulse6].do{|i| Ndef(i).set(\\fx, ~tremoloH.linlin(1, 16, 1, 88));}')
            self.evaluateSC('eval')               
        if snippet_num == 2 and pianosection == 'mid':
            self.__keyboard.type('Ndef(\\acc).map(\\note, Ndef(\\krm2_1));')
            self.evaluateSC('eval')
        if snippet_num == 2 and pianosection == 'mid with unmap':
            self.__keyboard.type('Ndef(\\acc).map(\\note, Ndef(\\krm2_1));')
            self.evaluateSC('eval') 
            #unmap
            self.__keyboard.type('[\\pulse, \\pulse2, \\pulse3, \\pulse4, \\pulse5, \\pulse6].do{|i| Ndef(i).set(\\pitch, ~tremoloM.linlin(1, 16, 200, 3000));}')
            self.evaluateSC('eval')
        if snippet_num == 2 and pianosection == 'low':
            self.__keyboard.type('Ndef(\\acc).map(\\amp, Ndef(\\krm2_2));')
            self.evaluateSC('eval') 
        if snippet_num == 2 and pianosection == 'low with unmap':
            self.__keyboard.type('Ndef(\\acc).map(\\amp, Ndef(\\krm2_2));')
            self.evaluateSC('eval')
            #unmap
            self.__keyboard.type('~map_rhythm = false;')
            self.evaluateSC('eval')            
            
            
            
    def tremolo(self, pianoregister, value):
        if pianoregister == 'hi':
            self.__keyboard.type('~tremoloH = ' + str(value))
        elif pianoregister == 'mid':
            self.__keyboard.type('~tremoloM = ' + str(value))
        elif pianoregister == 'low':
            self.__keyboard.type('~tremoloL = ' + str(value))               
        self.evaluateSC('eval')
        