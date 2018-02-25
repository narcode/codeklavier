// CodeKlavier Environment

~stop = Environment[
  'now' -> {|self|
"stopping".postln;
SkipJack.stop("pedalwatch");
~hello.stop;
~hello2.stop;
~hello3.stop;
~ost.stop;
~ost1.stop;
~ost2.stop;
~down=0;~down1=0;~down2=0;
~op=0;~op1=0;~op2=0;
}
];

~stop.know = true;