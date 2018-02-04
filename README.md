
# CodeKlavier
Live coding with the piano as interface.
An open source project by Felipe Ignacio Noriega and Anne Veinberg.

CodeKlavier development started in April 2017 and currently has two prototypes: "hello world" and Motippets. A performance on these prototypes was presented at SHA2017 and can be viewed here https://www.youtube.com/embed/efU7trVAPvA?start=1213. More information about the specific prototypes can be found in their respective directories. Please note that Motippets is currently in active development and is in the develop branch.

<div class='dream'>
<div>The dream: </div><div>An intuitive programming language with the piano as interface.</div></div>
<div class='dream'>
<div>The starting-to-be-graspable dream:</div><div>A programming language for the piano as interface</div></div>
<div class='dream'>
<div>The long term goal:</div><div>a live coding music-domain programming language for the piano as interface</div></div>
<div class='dream'>
<div>The mid term goal:</div><div>strategy-specific releases of mini-language approaches for live coding through the piano</div></div>
<div class='dream'>
<div>The short term goal:</div><div>research-release-evaluation cycles of prototypes which tackle specific aspects of the system</div></div>

## codeklavier-python
This is the Python directory of CodeKlavier. This project was initially started in Node.js but has been refactored into Python 3.0.

## Equipment
1. An acoustic-MIDI piano such as a Yamaha Disklavier, any piano fitted with a silent system or an acoustic intrument in combination with a MOOG piano bar. If an acoustic-MIDI piano is not available, any 88-key MIDI keyboard will suffice providing this instrument is of suitable sensitivity for the pianist.

2. MIDI interface (incase this is not present in the piano)

3. Sound system 

## Libraries
Install with pip3

1. python-rtmidi
2. pynput
3. sphinx

Run ``pip3 install -r requirements.txt`` to install the required libraries.

## SuperCollider

Please install [SuperCollider](http://supercollider.github.io)

__For this developement branch add the CodeKlavier directory to your sys.path so the CK modules are recognized__

in your ~/.bash_profile or equivalente add the following lines:

`# Modules for the CodeKlavier
PYTHONPATH="/Users/narcodeb/Development/Repos/codeklavier-python/CodeKlavier:$PYTHONPATH"
export PYTHONPATH`

## Test run
After installing the libraries, plug in your midi device and run the miditest by ``python3 miditest.py``. After you complete the setup and configuration, you will see the midi messages on the screen. After that: try playing a ``hello world`` piece. Move into the ``hello world`` directory and run ``python3 hello_world.py``.
