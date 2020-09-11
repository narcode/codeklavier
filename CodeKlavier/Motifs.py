"""Motifs in Dictionaries.

Here you can define the name of the motif and the series of midi-notes that
make up that motif.
Way more efficient than an unjustified class.

TODO: re-order to have a config loader before execution of prototypes, etc...
"""

import configparser
import os
from CK_config import inifile

config = configparser.ConfigParser()
config.read(inifile, encoding='utf8')

motifs = {}
motifs_mel = {}

mottipets_motifs = {}
mottipets_motifs_mel = {}

mini_motifs = {}
mini_motifs_mel = {}

conditional_motifs = {}
conditional_motifs_mel = {}

conditional_results_motifs = {}
conditional_results_motifs_mel = {}

ckalculator_motifs = {}
motifs_lambda = {}


try:
    #chordal:
    for motif in config['chordal main motifs midi']:
        mottipets_motifs[motif] = config['chordal main motifs midi'].get(motif).split(',')
        
    for motif in config['chordal mini motifs']:
        mini_motifs[motif] = config['chordal mini motifs'].get(motif).split(',')
    
    for motif in config['chordal conditional motifs midi']:
        conditional_motifs[motif] = config['chordal conditional motifs midi'].get(motif).split(',')

    for motif in config['chordal conditional results motifs midi']:
        conditional_results_motifs[motif] = config['chordal conditional results motifs midi'].get(motif).split(',')
      
    #melodic:  
    for motif in config['melodic main motifs midi']:
        mottipets_motifs_mel[motif] = config['melodic main motifs midi'].get(motif).split(',')
        
    for motif in config['melodic mini motifs']:
        mini_motifs_mel[motif] = config['melodic mini motifs'].get(motif).split(',')
    
    for motif in config['melodic conditional motifs midi']:
        conditional_motifs_mel[motif] = config['melodic conditional motifs midi'].get(motif).split(',')
        
    for motif in config['melodic conditional results motifs midi']:
        conditional_results_motifs_mel[motif] = config['melodic conditional results motifs midi'].get(motif).split(',')

    #ckalculator
    for motif in config['lambda']:
        ckalculator_motifs[motif] = config['lambda'].get(motif).split(',')    

except KeyError:
    raise LookupError('Missing sections in the config file or the config file does not exist. Maybe a typo?')

# chordal:
for motif in mottipets_motifs:
    motifs[motif] = list(map(int, mottipets_motifs[motif]))
        
for motif in mini_motifs:
    mini_motifs[motif] = list(map(int, mini_motifs[motif]))     
    
for motif in conditional_motifs:
    conditional_motifs[motif] = list(map(int, conditional_motifs[motif]))
    
for motif in conditional_results_motifs:
    conditional_results_motifs[motif] = list(map(int, conditional_results_motifs[motif]))      
    
# melodic:  
for motif in mottipets_motifs_mel:
    motifs_mel[motif] = list(map(int, mottipets_motifs_mel[motif]))
    
for motif in mini_motifs_mel:
    mini_motifs_mel[motif] = list(map(int, mini_motifs_mel[motif]))     

for motif in conditional_motifs_mel:
    conditional_motifs_mel[motif] = list(map(int, conditional_motifs_mel[motif]))
    
for motif in conditional_results_motifs_mel:
    #print('parsed motifs:', motif, mini_motifs_mel[motif])
    conditional_results_motifs_mel[motif] = list(map(int, conditional_results_motifs_mel[motif]))      

# lambda calculus
for motif in ckalculator_motifs:
    motifs_lambda[motif] = list(map(int, ckalculator_motifs[motif]))


