# codeklavier-python
CodeKlavier (experimental Python 3 flavour of CodeKlavier)

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
