// midi mappings:
s.waitForBoot({
	"starting MIDI...".postln;
	MIDIIn.connectAll;
s.sync;
MIDIClient.init;
s.sync;
MIDIIn.connectAll;
s.sync;
m = MIDIOut.newByName("IAC Driver", "Bus 1");
s.sync;
// hello world \\
(
"setting variables adn ostinatos...".postln;
~pitch = 0;~pitch1 = 0;~pitch2 = 0; ~pulsepitch = 0;
// adjust the quant;
~quant=1/4;
s.sync;
// ostinatos:
~ost=Pdef(\ostinato1, {Pbind(\dur, Pseq([Pfuncn({1/h}, 1), Pfuncn({1/e},1), Pfuncn({1/l},1)], inf), \ctranspose, Pfunc{~pitch},
\midinote, Pseq(["ab3".namemidi, "B3".namemidi, "C4".namemidi, "gb3".namemidi, "f3".namemidi, "db3".namemidi, "C4".namemidi], inf),
\type, \midi, \midiout, m)});
~ost.quant=~quant;
~ost1=Pdef(\ostinato2, {Pbind(\dur, Pseq([Pfuncn({1/o}, 1), Pfuncn({1/w},1), Pfuncn({1/r},1)], inf), \ctranspose, Pfunc{~pitch1},
\midinote, Pseq(["ab3".namemidi, "B3".namemidi, "C4".namemidi, "gb3".namemidi, "f3".namemidi, "db3".namemidi, "C4".namemidi], inf),
\type, \midi, \midiout, m)});
~ost1.quant=~quant;
~ost2=Pdef(\ostinato3, {Pbind(\dur, Pseq([Pfuncn({1/d}, 1), Pfuncn({1/a},1), Pfuncn({1/n},1)], inf), \ctranspose, Pfunc{~pitch2},
\midinote, Pseq(["ab3".namemidi, "B3".namemidi, "C4".namemidi, "gb3".namemidi, "f3".namemidi, "db3".namemidi, "C4".namemidi], inf),
\type, \midi, \midiout, m)});
~ost2quant=~quant;
s.sync;
// random ostinatos

~rand=Tdef(\randostinato, {
var rit = (1/2).rrand(4).round(0.5);
var rit2 = (1/2).rrand(4).round(0.5);
var rit3 = (1/2).rrand(4).round(0.5);
var randrit = [Pfuncn({1/(h*rit)}, 1), Pfuncn({1/(e*rit2)},1), Pfuncn({1/(l*rit3)},1)];
var randpitch = ["ab3".namemidi, "B3".namemidi, "C4".namemidi, "gb3".namemidi, "f3".namemidi, "db3".namemidi].scramble;
	Pdef(\ostinato1, {Pbind(\dur, Pseq(randrit, inf);, \ctranspose, Pfunc{~pitch},
\midinote, Pseq(randpitch, inf),
\type, \midi, \midiout, m)})});
s.sync;
// hello pulse
~hello=Pdef(\hello, {Pbind(\dur, Pseq([2], inf), \ctranspose, Pfunc{~h1o}, \midinote, Pseq(["a2".namemidi], inf), \type, \midi, \midiout, m)});
~hello.quant=~quant;
~hello2=Pdef(\hello2, {Pbind(\dur, Pseq([2], inf), \ctranspose, Pfunc{~h2o}, \midinote, Pseq(["a2".namemidi], inf), \type, \midi, \midiout, m)});
~hello2.quant=~quant;
~hello3=Pdef(\hello3, {Pbind(\dur, Pseq([2], inf), \ctranspose, Pfunc{~h3o}, \midinote, Pseq(["a2".namemidi], inf), \type, \midi, \midiout, m)});
~hello3.quant=~quant;
s.sync;
~hello2.quant=~quant;
~h1o=~h2o=~h3o=0;
s.sync;
h=e=l=o=w=d=a=r=n=1;
~p = 1; // ????
s.sync;
~reset = Tdef(\reset, {1.do{h=e=l=o=w=d=a=r=n=1; t.tempo=1;
	~h1o=~h2o=~h30=0;
	~ost=Pdef(\ostinato1, {Pbind(\dur, Pseq([Pfuncn({1/h}, 1), Pfuncn({1/e},1), Pfuncn({1/l},1)], inf), \ctranspose, Pfunc{~pitch},
	\midinote, Pseq(["ab3".namemidi, "B3".namemidi, "C4".namemidi, "gb3".namemidi, "f3".namemidi, "db3".namemidi, "C4".namemidi], inf),
	\type, \midi, \midiout, m)});
	~ost1=Pdef(\ostinato2, {Pbind(\dur, Pseq([Pfuncn({1/o}, 1), Pfuncn({1/w},1), Pfuncn({1/r},1)], inf), \ctranspose, Pfunc{~pitch1},
	\midinote, Pseq(["ab3".namemidi, "B3".namemidi, "C4".namemidi, "gb3".namemidi, "f3".namemidi, "db3".namemidi, "C4".namemidi], inf),
	\type, \midi, \midiout, m)});
	~ost2=Pdef(\ostinato3, {Pbind(\dur, Pseq([Pfuncn({1/d}, 1), Pfuncn({1/a},1), Pfuncn({1/n},1)], inf), \ctranspose, Pfunc{~pitch2},
	\midinote, Pseq(["ab3".namemidi, "B3".namemidi, "C4".namemidi, "gb3".namemidi, "f3".namemidi, "db3".namemidi, "C4".namemidi], inf),
	\type, \midi, \midiout, m)});
		}
	});
	s.sync;
);
(
	"starting routine for re-pitching with piano pedal...".postln;
	/// re-pitching:
SkipJack({
	/*var key = "narcode".scramble;
Tdef(key.asSymbol, {*/
	1.do {

	if (~op == 1) {
		/*("op ---> running").postln;*/

		MIDIdef.cc(\pedalpitch, {arg ...args;
			if (args[1] == 64) {
				~pitch = args[0].linlin(0, 127, 0, 12).round(1);
				("ostinato1 ***" + ~pitch + " semitones up").postln;
			}
		});
	};

	if (~op == 0) {
		/*("op ----> stopped").postln;*/
MIDIdef.cc(\pedalpitch).free;
	};

	if (~op1 == 1) {
		MIDIdef.cc(\pedalpitchop1, {arg ...args;
			if (args[1] == 64) {
				~pitch1 = args[0].linlin(0, 127, 0, 12).round(1);
			  ("ostinato2 ***" + ~pitch1 + " semitones up").postln;
			}
		});
	};

	if (~op1 == 0) {
MIDIdef.cc(\pedalpitchop1).free;
	};

	if (~op2 == 1) {
		MIDIdef.cc(\pedalpitchop2, {arg ...args;
			if (args[1] == 64) {
				~pitch2 = args[0].linlin(0, 127, 0, 12).round(1);
				("ostinato3 *** " + ~pitch2 + " semitones up").postln;
			}
		});
	};

	if (~op2 == 0) {
MIDIdef.cc(\pedalpitchop2).free;
	};

	if (~down == 1) {
		("down ---> running").postln;
		MIDIdef.cc(\pedalpitchd, {arg ...args;
			if (args[1] == 64) {
				~pitch = args[0].linlin(0, 127, 0, -7).round(1);
				("ostinato1 ***" + ~pitch + " semitones down").postln;
			}
		});
	};

	if (~down == 0) {
		/*("down ----> stopped").postln;*/

MIDIdef.cc(\pedalpitchd).free;
	};

	if (~down1 == 1) {
		MIDIdef.cc(\pedalpitchd1, {arg ...args;
			if (args[1] == 64) {
				~pitch1 = args[0].linlin(0, 127, 0, -7).round(1);
			  ("ostinato2 ***" + ~pitch1 + " semitones down").postln;
			}
		});
	};

	if (~down1 == 0) {
MIDIdef.cc(\pedalpitchd1).free;
	};

	if (~down2 == 1) {
		MIDIdef.cc(\pedalpitchd2, {arg ...args;
			if (args[1] == 64) {
				~pitch2 = args[0].linlin(0, 127, 0, -7).round(1);
				("ostinato3 ***" + ~pitch2 + " semitones down").postln;
			}
		});
	};

	if (~down2 == 0) {
MIDIdef.cc(\pedalpitchd2).free;
	};
}; }, 1, name: "pedalwatch");
);
s.sync;
"CodeKlavier is ready and listening...".postln;
}.fork;
);

/// if you want to stop the pedal watcher:
/*SkipJack.stop("pedalwatch");*/
