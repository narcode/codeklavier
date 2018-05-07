# Motippets

The Motippets prototype is able to parse selected melodic/harmonic motifs and map these to music making code snippets. Once a snippet is present, up to three of its variables can be manipulated through a tremolo recognition function. This function calculates the interval of the tremolo in real-time and sets this value to the associated variable. The keyboard is divided into three distinct ranges and we use mini-motifs to direct the system as to which variable is being manipulated at any given moment.This setup enables the pianist to code and manipulate snippets in parallel- a feature made possible by the use of the piano keyboard as a coding interface. 

Furthermore, in Motippets  the performer is able to set up both ongoing and momentary conditionals. These conditionals test aspects of the pianist’s playing such as the number of notes played over a particular time period or the range within which the pianist IS or IS NOT playing. If a test is passed, an event occurs. All of the values and outcomes of these conditionals are set up by the pianist during the performance. 

The performer is relatively free to play anything on the piano but must ensure that the coding motifs are integrated into the performance. The structure is not set and should be reactionary to the interaction of the coded algorithms.You can watch a video of one version of Motippets [here](https://youtu.be/nzsW1w38JEc)
 

## Run
Make sure you have installed supercollider and the required libraries before you
start motipets. Then run: ``python3 motippets.py``.

## Customise
This prototype is musically customisable by adjusting the motifs used to trigger the snippets in the motifs class and/or adjusting the printed snippets in the default.ini
