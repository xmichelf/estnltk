'''
Comparison of wordnet relations with https://teksaurus.keeleressursid.ee relations.
'''

from estnltk import wordnet
from estnltk.wordnet import Synset

source_relation = [ 'patustus', 'päevalillekollane', 'õigusetu', 'puhiseja', 'pageja', 'miktsioonuriin',  'Millsi test', 'liigutustundlikkus', 'limaskestabarjäär', 'tuššima']
target_relations = {}
for relation in source_relation:
    target_relations[relation] = {}
target_relations['patustus']['hyponym'] = {'käitumisakt'}
target_relations['patustus']['involved'] =  {'patutegu'}
target_relations['patustus']['hypernym'] = {'väärdumine'}
target_relations['päevalillekollane']['hypernym'] = {'kollane'}
target_relations['õigusetu'][None] = {None}
target_relations['puhiseja']['agent'] = {'puhklema'}
target_relations['pageja']['similar'] = {'reduline'}
target_relations['pageja']['agent'] = {'pakku minema','redu'}
target_relations['pageja']['hyponym'] = {'putkaja'}
target_relations['miktsioonuriin']['hypernym'] = {'piss'}
target_relations['Millsi test']['involved_patient'] = {'tennisisti küünarliiges'}
target_relations['Millsi test']['hypernym'] = {'kats'}
target_relations['liigutustundlikkus']['hypernym'] = {'tundehellus'}
target_relations['limaskestabarjäär']['hypernym'] = {'atribuut'}
target_relations['tuššima']['hypernym'] = {'joonistama'}


wn = Wordnet(version='74')

def test_relations():
    for source_node in source_relation:
        id = wn.get_synset(source_node)[0]
        source_name = Synset(wn, id).name[:-4]
        relations = Synset(wn, id).get_related_synset() 
        for relation in relations:
            if relation[0].name is None:
                assert None in target_relations[source_name][None]
                continue
            rel_name = relation[0].name[0:-4]
            rel_type = relation[1]
            assert rel_name in target_relations[source_name][rel_type]

source_nodes = ['õigusetu', 'väikettevõtja']
iteration_relations = {}
for key in source_nodes:
    iteration_relations[key] = {}
    iteration_depth[key] = {}

iteration_relations['õigusetu'][None] = {None}
iteration_relations['väikettevõtja']['hypernym'] = {'olev', 'miski'} # olev  - 6

iteration_depth['õigusetu']['depth'] = {None}
iteration_depth['väikettevõtja']['depth'] = {6}


def test_root_hypernyms():

    #root_hypernyms test
    for source_node in source_nodes:
        id = wn.get_synset(source_node)[0]
        roots = Synset(wn,id).root_hypernyms(depth_threshold=float('inf'), return_depths=True)
        for relation in roots:
            synset = relation[0]
            depth = relation[1]
            if synset is None: #if depth is 0, ie. no relations
                assert None in iteration_relations[source_node][None] 
            else:
                assert synset.name[:-4] in iteration_relations[source_node]['hypernym']
                assert depth in iteration_depth[source_node]['depth']


def test_closure():
    #closure test
    for source_node in source_nodes:
        id = wn.get_synset(source_node)[0]
        roots = Synset(wn, id).root_hypernyms(relation=None, depth_threshold=float('inf'), return_depths=True)
        for relation in roots:
            synset = relation[0]
            depth = relation[1]
            if synset is None:
                assert None in iteration_relations[source_node][None]
            else:
                assert synset.name[:-4] in iteration_relations[source_node]['hypernym']
                assert depth in iteration_depth[source_node]['depth']

