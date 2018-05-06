# Hybrid Prototype
The hybrid prototype allows for easy transition from the "hello world" prototype to the Motippets prototype without stopping any of the running code. Check the README.md in the HelloWorld and Motippets directory for more information about what these prototypes can do.

The hybrid prototype comes with a 5 column display for the printed text, the first of which is for "hello world" and 2-5 are for Motippets.

Column 1 - "hello world"
Column 2 - Mot. Snippet 1
Column 3 - Mot. Snippet 2
Column 4 - Mot. Conditionals text
Column 5 - Mot. Conditionals running loops


## Run
Make sure you in the right directory and have installed SuperCollider and the required libraries as mentioned in the general [Read Me document](https://github.com/narcode/codeklavier-python/blob/master/README.md)

To run hybrid codeklavier: ``python3 codeklavier.py -p hybrid``
To run display: Make sure you are in the Codeklavier folder of the codeklavier directory and then use ``python3 CK_socket.py -d5``

## Using the hybrid
Switching between the two prototypes is done by pressing the top Bb on the piano. All sound processes and the ongoing conditionals will continue running so the change will only impact the input mode for the piano. 

Be sure to evaluate the SuperCollider files that correspond with your desired code output extension
