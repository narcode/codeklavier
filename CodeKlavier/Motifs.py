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
motifs_ar = {}


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
    
    if len(config['ar']) > 1:
        dot = config['ar'].get('dot').split(',')
        create = config['ar'].get('create').split(',')
        clear_rule = config['ar'].get('clear').split(',')
        select = config['ar'].get('select').split(',')
        generation = config['ar'].get('generation').split(',')
        nextt = config['ar'].get('nextt').split(',')
        transform = config['ar'].get('transform').split(',')
        shape = config['ar'].get('shape').split(',')
        store_collection = config['ar'].get('store_collection').split(',')
        transp_even = config['ar'].get('transpositon_even').split(',')
        transp_odd = config['ar'].get('transposition_odd').split(',')
        

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

# AR module
if len(config['ar']) > 1:
    motifs_ar['dot'] = list(map(int, dot))
    motifs_ar['create'] = list(map(int, create))
    motifs_ar['clear_rule'] = list(map(int, clear_rule))
    motifs_ar['generation'] = list(map(int, generation))
    motifs_ar['select'] = list(map(int, select))
    motifs_ar['next'] = list(map(int, nextt))
    motifs_ar['transform'] = list(map(int, transform))
    motifs_ar['shape'] = list(map(int, shape))
    motifs_ar['store_collection'] = list(map(int, store_collection))
    motifs_ar['transp_even'] = list(map(int, transp_even))
    motifs_ar['transp_odd'] = list(map(int, transp_odd))

