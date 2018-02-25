/*

-> toy piano sampler by narcode. April 2017 <-

Thanks to Anne Veinberg for Recording this

*/

{
// load the custom toy piano samples
b = ();
g = Group.new(s, \addToHead);
~pathsamples = thisProcess.nowExecutingPath.dirname;
s.sync;
29.do{|i|
  ~num = 36 + i;
  b[i] = Buffer.read(s, ~pathsamples++"/TPSamples/"++~num++".wav");
};
s.sync;

~srcid =  nil; // annerob: 1151127154 felipe 1429867122 anne -1869464304

// sampler node:
MIDIdef.noteOn(\toypiano, {arg ...args;
  var midinote = args[1]-56;
  // args.postln;
  midinote.postln;
if (midinote < 64 && midinote >= 0) {
  Ndef(midinote.asSymbol, {PlayBuf.ar(2, b[midinote], loop:0) * EnvGen.kr(Env.perc(0.01, 1.5))}).play(6, group: g);
  Ndef((midinote.asString++"d0").asSymbol, {PlayBuf.ar(2, b[midinote], loop:0) * EnvGen.kr(Env.perc(0.01, 1.5))}).play(0);
    }
}, chan: 0, srcID: ~srcid); // 1151127154


// channel 1:
  MIDIdef.noteOn(\toypiano1, {arg ...args;
    var midinote = args[1]-56;
    /*args.postln;*/
    midinote.postln;
  if (midinote < 64 && midinote >= 0) {
    Ndef(midinote.asSymbol, {PlayBuf.ar(2, b[midinote], loop:0) * EnvGen.kr(Env.perc(0.01, 1.5))}).play(20, group: g);
    Ndef((midinote.asString++"d1").asSymbol, {PlayBuf.ar(2, b[midinote], loop:0) * EnvGen.kr(Env.perc(0.01, 1.5))}).play(0);
      }
    }, chan: 1, srcID: ~srcid); // 1151127154


    // channel 2:
      MIDIdef.noteOn(\toypiano2, {arg ...args;
        var midinote = args[1]-56;
        var duplicate = midinote.asString++"d";
        /*args.postln;*/
        midinote.postln;

      if (midinote < 64 && midinote >= 0) {
        Ndef(midinote.asSymbol, {PlayBuf.ar(2, b[midinote], loop:0) * EnvGen.kr(Env.perc(0.01, 1.5))}).play(4, group: g);
        Ndef(duplicate.asSymbol, {PlayBuf.ar(2, b[midinote], loop:0) * EnvGen.kr(Env.perc(0.01, 1.5))}).play(0);
          }
        }, chan: 2, srcID: ~srcid); // 1151127154

        // channel 3:
          MIDIdef.noteOn(\toypiano3, {arg ...args;
            var midinote = args[1]-56;
            /*args.postln;*/
            midinote.postln;

          if (midinote < 64 && midinote >= 0) {
            Ndef(midinote.asSymbol, {PlayBuf.ar(2, b[midinote], loop:0) * EnvGen.kr(Env.perc(0.01, 1.5))}).play(0);
              }
            }, chan: 3, srcID: ~srcid); // 1151127154


s.sync;
"Toy piano sampler ready!".postln;
s.sync;
// fx:
~gtail = Group.new(s, \addToTail);
Ndef(\fx, {|del=1, amp=0.001| CombN.ar(SoundIn.ar(0), 0.2, del.reciprocal, 4)*amp}).play(0, group: ~gtail);
s.sync;
Ndef(\fx1, {|del=1, amp=0.001| CombN.ar(SoundIn.ar(0), 0.2, del.reciprocal, 1)*amp}).play(1, group: ~gtail);
s.sync;
Ndef(\fx2, {|del=2, amp=0.001, rate=1| GVerb.ar(FreqShift.ar(SoundIn.ar(0), LFTri.kr(rate.reciprocal).range(8000, 100)), 62, del)*amp}).play(0,2, group: ~gtail);
s.sync;
"fx ready!".postln;
}.fork;
