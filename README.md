# CodeKlavier

### Live coding with the piano as interface.

An open source project by Felipe Ignacio Noriega and Anne Veinberg. 

CodeKlavier development started in April 2017 and currently has five modules (newest on top):
+  [*ARquatic*](https://codeklavier.space/arquatic) (A CodeKlavier Augmented Reality experience!)
+  [*Ckalcuλator*](https://github.com/narcode/codeklavier/tree/master/ckalculator) (Lambda-calculus with the piano!)
+  [*Hybrid*](https://github.com/narcode/codeklavier/blob/master/hybrid/README.md) (switching between the first two prototypes and includes a custom code display via udp sockets)
+  [*Motippets*](https://github.com/narcode/codeklavier/tree/master/motippets) (coding via pianistic gestures/motifs)
+  [*hello world*](https://github.com/narcode/codeklavier/blob/master/hello_world) (proof of concept prototype, with 1-1 mapping of piano keys to alphanumeric characters)

More information about the specific prototypes can be found in their respective directories.


Checkout our [videos page](https://codeklavier.space/videos) to see the Codeklavier in action or visit the [Activities page](https://codeklavier.space/activities) for info on past and future performances.

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
1. An acoustic-MIDI piano such as a  Disklavier, any piano fitted with a silent system or an acoustic intrument in combination with a MOOG piano bar or other MIDI keyscanner. We use a MIDI KeyScanner developed by Andrew McPherson and his team at Queen Mary University of London. If an acoustic-MIDI piano is not available, any 88-key MIDI keyboard will suffice providing this instrument is of suitable sensitivity for the pianist.

2. MIDI interface (if not integrated in the piano)

## Libraries
Install with pip3

1. python-rtmidi
2. pynput
3. sphinx
4. numpy
5. python-osc (if you want to use the AR module and Caffeine Extension)
6. websockets (idem)

Run ``pip3 install -r requirements.txt`` to install the required libraries.

## Modules
__For this version please add the CodeKlavier directory to your sys.path so the CK modules are recognized__

You can run the ``setPythonPath.sh`` every time you start a new shell (type ``. setPythonPath.sh`` - not the **dot-space** before the command), or put the following lines in your ``~/.bash_profile`` or ``~/.bashrc`` or equivalent add the following lines (make sure you have the correct path!):

`# Modules for the CodeKlavier
PYTHONPATH="/path/to/your/codeklavier/project/folder:$PYTHONPATH"
export PYTHONPATH`

As an example, the path to the Codeklavier in my system looks like this:

`
PYTHONPATH="/Users/narcodeb/Development/Repos/codeklavier-python/CodeKlavier:$PYTHONPATH"
`
## Extensions

There are a number of different code output extensions for the CodeKlavier. The loading ini file for these can be found in the CodeKlavier-Extensions repository[https://github.com/codeklavier/codeklavier-extensions]. You will need to download/clone this directory in order to run CodeKlavier.

If you are interested in collaborating on an extension for the CodeKlavier, don't hesitate to get in touch.

Currently, outpute extensions exist for SuperCollider, Mercury, JavaScript, Augmented Reality and Hydra.


## Test run
After installing the libraries, plug in your midi device and run the miditest by ``python3 miditest.py``. After you complete the setup and configuration, you will see the midi messages on the screen. After that run codeklavier.py -p hybrid -i base.ini (be sure to change the directory too match your setup  Try playing an upward  C major 3 note arpeggio starting on middle C. If everything works, your test is complete and you are ready to explore CK!


## Watch
[Codeklavier Videos](http://codeklavier.space/videos)

## Publications
[Publications page](https://codeklavier.space/publications)

## Support
This project was made possible by the Creative Industries Fund NL, our angel sponsor and the festivals and venues that book us for paid concerts. However, our initial funding has come to an end so if you believe in the project and would like to support it, please consider "buying us a coffee". Every little bit counts and we greatly appreciate your support!

[![ko-fi](https://www.ko-fi.com/img/donate_sm.png)](https://ko-fi.com/J3J7PGIE)
