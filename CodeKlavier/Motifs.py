"""Motifs in Dictionaries.

Here you can define the name of the motif and the series of midi-notes that
make up that motif.
Way more efficient than an unjustified class.

TODO: re-order to have a config loader before execution of prototypes, etc...
"""

import configparser
import os

currentpath = os.path.dirname(os.path.abspath(__file__))
projectdir = os.path.abspath(os.path.join(currentpath, os.pardir))

config = configparser.ConfigParser()
config.read(projectdir + '/default_setup.ini', encoding='utf8')

motifs = {}
motifs_mel = {} #TODO

mini_motifs = {}
mini_motifs_mel = {}

conditional_motifs = {}
conditional_motifs_mel = {}

conditional_results_motifs = {}
conditional_results_motifs_mel = {}

mottipets_motifs = {}
motifs_lambda = {}


try:
    #chordal:
    for motif in config['chordal main motifs midi']:
        mottipets_motifs[motif] = config['chordal main motifs midi'].get(motif).split(',')
    
    for motif in config['chordal conditional motifs midi']:
        conditional_motifs[motif] = config['chordal conditional motifs midi'].get(motif).split(',')

    for motif in config['chordal conditional results motifs midi']:
        conditional_results_motifs[motif] = config['chordal conditional results motifs midi'].get(motif).split(',')
      
    #melodic:  
    for motif in config['melodic mini motifs']:
        mini_motifs_mel[motif] = config['melodic mini motifs'].get(motif).split(',')
        
    for motif in config['melodic conditional results motifs midi']:
        conditional_results_motifs_mel[motif] = config['melodic conditional results motifs midi'].get(motif).split(',')
    
    #mini_motif_1_mid = config['snippets midi mapping'].get('mini_motif_1_mid').split(',')
    #mini_motif_2_mid = config['snippets midi mapping'].get('mini_motif_2_mid').split(',')
    #mini_motif_3_mid = config['snippets midi mapping'].get('mini_motif_3_mid').split(',')    
    
    #conditional_1 = config['snippets midi mapping'].get('conditional_1').split(',')
    conditional_2 = config['snippets midi mapping'].get('conditional_2').split(',')
    conditional_3 = config['snippets midi mapping'].get('conditional_3').split(',')
    
    #conditional_result_1 = config['snippets midi mapping'].get('conditional_result_1').split(',')
    #conditional_result_2 = config['snippets midi mapping'].get('conditional_result_2').split(',')
    #conditional_result_3 = config['snippets midi mapping'].get('conditional_result_3').split(',')
    #conditional_result_4 = config['snippets midi mapping'].get('conditional_result_4').split(',')
    conditional_result_5 = config['snippets midi mapping'].get('conditional_result_5').split(',')

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
    raise LookupError('Missing key information in the config file.')

# motippets
#motifs['motif_1'] = list(map(int, motif_1))
#motifs['motif_2'] = list(map(int, motif_2))

# chordal:
for motif in mottipets_motifs:
    motifs[motif] = list(map(int, mottipets_motifs[motif]))
    
for motif in conditional_motifs:
    conditional_motifs[motif] = list(map(int, conditional_motifs[motif]))
    
for motif in conditional_results_motifs:
    conditional_results_motifs[motif] = list(map(int, conditional_results_motifs[motif]))      
    
# melodic:  
for motif in mini_motifs_mel:
    mini_motifs_mel[motif] = list(map(int, mini_motifs_mel[motif]))     
    
for motif in conditional_results_motifs_mel:
    #print('parsed motifs:', motif, mini_motifs_mel[motif])
    conditional_results_motifs_mel[motif] = list(map(int, conditional_results_motifs_mel[motif]))      

#mini_motifs['mini_motif_1_mid'] = list(map(int, mini_motif_1_mid))
#mini_motifs['mini_motif_2_mid'] = list(map(int, mini_motif_2_mid))
#mini_motifs['mini_motif_3_mid'] = list(map(int, mini_motif_3_mid))


#conditional_motifs['conditional_1'] = list(map(int, conditional_1))
conditional_motifs['conditional_2'] = list(map(int, conditional_2))
conditional_motifs['conditional_3'] = list(map(int, conditional_3))
#conditional_motifs['conditional_result_1'] = list(map(int, conditional_result_1))
#conditional_motifs['conditional_result_2'] = list(map(int, conditional_result_2))
#conditional_motifs['conditional_result_3'] = list(map(int, conditional_result_3))
#conditional_motifs['conditional_result_4'] = list(map(int, conditional_result_4))
conditional_motifs['conditional_result_5'] = list(map(int, conditional_result_5))

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


