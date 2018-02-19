# CodeKlavier
### Live coding with the piano as interface.

An open source project by Felipe Ignacio Noriega and Anne Veinberg. Supported By **Stimuleringsfonds Creatieve Industrie** for its developement and
**FondsPodiumKunsten NL** for public presentations

CodeKlavier development started in April 2017 and currently has two prototypes (newest on top):
+  *Motippets* (coding via pianistic gestures/motifs)
+ *hello world* (proof of concept prototype, with 1-1 mapping of piano keys to alphanumeric characters)

More information about the specific prototypes can be found in their respective directories.


A performance on these prototypes was presented at SHA2017 and can be viewed here:<br>
[#sha2017 presentation](https://www.youtube.com/embed/efU7trVAPvA?start=1213) <br>

<div class='dream'>
<div><strong>The dream:</strong></div><div>🐍🎹 An intuitive programming language with the piano as interface.</div></div>
<div class='dream'>
<div><strong>The starting-to-be-graspable dream:</strong></div><div>👩🏼‍💻 A programming language for the piano as interface</div></div>
<div class='dream'>
<div><strong>The long term goal:</strong></div><div>🎼🎧 a live coding music-domain programming language for the piano as interface</div></div>
<div class='dream'>
<div><strong>The mid term goal:</strong></div><div>💾📌 strategy-specific releases of mini-language approaches for live coding through the piano</div></div>
<div class='dream'>
<div><strong>The short term goal:</strong></div><div>📆📈 research-release-evaluation cycles of prototypes which tackle specific aspects of the system</div></div>


## Equipment
1. An acoustic-MIDI piano such as a Yamaha Disklavier, any piano fitted with a silent system or an acoustic intrument in combination with a MOOG piano bar. If an acoustic-MIDI piano is not available, any 88-key MIDI keyboard will suffice providing this instrument is of suitable sensitivity for the pianist.

2. MIDI interface (in case this is not present in the piano)

## Libraries
Install with pip3

1. python-rtmidi
2. pynput
3. sphinx

Run ``pip3 install -r requirements.txt`` to install the required libraries.

## SuperCollider

Please install the latest release of [SuperCollider](http://supercollider.github.io)

## Test run
After installing the libraries, plug in your midi device and run the miditest by ``python3 miditest.py``. After you complete the setup and configuration, you will see the midi messages on the screen. After that: try playing a ``hello world`` piece. Move into the ``hello world`` directory and run ``python3 hello_world.py``.

# This project is possible thanks to the Stimuleringsfonds Creatieve Industrie
