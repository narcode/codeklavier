# "hello world"
A work for Robot Toy Piano and acoustic midi piano performed by a (coder) pianist.

“hello world” is the first prototype of the CodeKlavier created especially to live code the actions of a Robot Toy Piano through playing an acoustic midi piano as interface. The keys are individually mapped to alphanumeric characters and strings to allow the (coder) pianist to execute various code
commands through corresponding motivic material. The system is built on top of Python 3.0 and SuperCollider.

In true live coding spirit, a performance of "hello world" is not subject to a concrete structure and should unfold in its own way with every performance. Feel free to watch Anne Veinberg's [performance](https://youtu.be/ytpB8FB6VTU) of "hello world" and view a [score](https://drive.google.com/file/d/0B6qSeqXuDEKQSWNnSDVOdkJyaGNIVnVhNVlhbDZZLThWSzFz/view?usp=sharing) of the piece. 


## To Run
Make sure you in the right directory and have installed SuperCollider and the required libraries as mentioned in the general [Read Me document](https://github.com/narcode/codeklavier-python/blob/master/README.md). 

For the Robot Toy Piano version, run ``python3 codeklavier.py -p hello_world_rtp``

## Versions and Extensions
As an extension to the original "hello world", for [SHA2017](https://sha2017.org) a version that also incorporates sound processing was created. You can watch the presentation on [youtube](https://youtu.be/efU7trVAPvA).

To run this version use ``python3 codeklavier.py -phello_world_v4.py``

To make your own custom mappings, use the Mapping.py file

In September 2017, a special version of "hello world" was created for the Leiden Night of Art and Science (Leiden Nacht van Kunst en Kennis (NKK)). For this version, audience members were encouraged to try-out the CodeKlavier system and see what <u>they could live code through piano playing. The key mapping was simplified so that non-pianists were also able to have a go and a Python tutorial was created to assist the participant. With the help of the tutorial, this version can theoretically run as an installation without further assistance, although some participants may find this too challenging or require more time to navigate through the system. 
  
A unique feature of the NKK version is that it utilized the tremolo as value function of the [Motippets](https://github.com/narcode/codeklavier/tree/master/mottipets) prototype. In the future, the concept behind this version will form the basis of the CodeKlavierEDU model - an educational CodeKlavier system. If you would like to know more about this version or the future CodeKlavierEDU model, please get in touch.

