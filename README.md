# CodeKlavier
### Live coding with the piano as interface.

An open source project by Felipe Ignacio Noriega and Anne Veinberg. Supported By **Stimuleringsfonds Creatieve Industrie NL** and other sponsors.

CodeKlavier development started in April 2017 and currently has four prototypes (newest on top):
+  *Ckalcuλator* (Lambda-calculus with the piano!)
+  *Hybrid* (switching between the two prototypes and includes a custom code display via udp sockets)
+  *Motippets* (coding via pianistic gestures/motifs)
+  *hello world* (proof of concept prototype, with 1-1 mapping of piano keys to alphanumeric characters)

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
1. An acoustic-MIDI piano such as a  Disklavier, any piano fitted with a silent system or an acoustic intrument in combination with a MOOG piano bar or other MIDI keyscanner. If an acoustic-MIDI piano is not available, any 88-key MIDI keyboard will suffice providing this instrument is of suitable sensitivity for the pianist.

2. MIDI interface (if not integrated in the piano)

## Libraries
Install with pip3

1. python-rtmidi
2. pynput
3. sphinx
4. numpy

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

#### Augmented Reality

Standalone AR Extension Developed for the Ckalculator in collaboration with [Patrick Borgeat](https://github.com/cappelnord). Read more about it or watch it in action [Codeklavier/augmentedreality](https://codeklavier.space/augmentedreality)

#### SuperCollider

Use the Codeklavier to code electronic music. This is our default, built-in extension. We will release it as a Quark soon. Please install the latest release of [SuperCollider](http://supercollider.github.io)


## Test run
After installing the libraries, plug in your midi device and run the miditest by ``python3 miditest.py``. After you complete the setup and configuration, you will see the midi messages on the screen. After that: try playing a ``hello world`` piece. Move into the ``hello world`` directory and run ``python3 hello_world.py``.

Be sure to setup the correct port and device ID via ``default_setup.ini``

## Watch
[Codeklavier Videos](http://codeklavier.space/videos)

## Papers
[Coding with a Piano: The first phase of the CodeKlavier's development](https://drive.google.com/file/d/1UIr2JyPqRw833OIkBgDrx2P6VjZcEKf1/view?usp=sharing), International Computer Music Conference 2018

## Support
This project is made possible by the Creative Industries Fonds NL, our angel sponsor and the festivals and venues that book us for paid concerts. However, our funding will soon run out so if you believe in the project and would like to support it, please consider "buying us a coffee". Every little bit counts and we greatly appreciate your support! [![ko-fi](https://www.ko-fi.com/img/donate_sm.png)](https://ko-fi.com/J3J7PGIE)

