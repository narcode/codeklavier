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

    #all are lists
    identity_midi = config['lambda'].get('identity_midi').split(',')
    evaluate_function = config['lambda'].get('evaluate_function').split(',')
    select_first = config['lambda'].get('select_first_midi').split(',')
    select_second = config['lambda'].get('select_second_midi').split(',')
    successor = config['lambda'].get('successor_midi').split(',')
    predecessor = config['lambda'].get('predecessor_midi').split(',')
    add_midi = config['lambda'].get('add_midi').split(',')
    subtract_midi = config['lambda'].get('subtract_midi').split(',')
    mult_midi = config['lambda'].get('mult_midi').split(',')
    division_midi = config['lambda'].get('division_midi').split(',')
    equal_than_midi = config['lambda'].get('equality_midi').split(',')
    greater_than_midi = config['lambda'].get('greater_than_midi').split(',')
    less_than_midi = config['lambda'].get('less_than_midi').split(',')

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
motifs_lambda['eval'] = list(map(int, evaluate_function))
motifs_lambda['zero'] = list(map(int, identity_midi))
motifs_lambda['true'] = list(map(int, select_first))
motifs_lambda['false'] = list(map(int, select_second))
motifs_lambda['successor'] = list(map(int, successor))
motifs_lambda['predecessor'] = list(map(int, predecessor))
motifs_lambda['addition'] = list(map(int, add_midi))
motifs_lambda['subtraction'] = list(map(int, subtract_midi))
motifs_lambda['multiplication'] = list(map(int, mult_midi))
motifs_lambda['division'] = list(map(int, division_midi))
motifs_lambda['equal'] = list(map(int, equal_than_midi))
motifs_lambda['greater'] = list(map(int, greater_than_midi))
motifs_lambda['less'] = list(map(int, less_than_midi))


