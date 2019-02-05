'''
Comparison of wordnet relations with https://teksaurus.keeleressursid.ee relations.
'''

from estnltk.wordnet import Wordnet
from estnltk.wordnet import Synset

source_relation = [ 'patustus', 'päevalillekollane', 'õigusetu', 'puhiseja', 'pageja', 'miktsioonuriin',  'Millsi test', 'liigutustundlikkus', 'limaskestabarjäär', 'tuššima']
target_relations = {}
for relation in source_relation:
    target_relations[relation] = {}
target_relations['patustus']['hyponym'] = {'käitumisakt'}
target_relations['patustus']['involved'] =  {'patutegu'}
target_relations['patustus']['hypernym'] = {'väärdumine'}
target_relations['päevalillekollane']['hypernym'] = {'kollane'}
target_relations['õigusetu']['None'] = {'None'}
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
                assert 'None' in target_relations[source_name]['None']
                continue
            rel_name = relation[0].name[0:-4]
            rel_type = relation[1]
            assert rel_name in target_relations[source_name][rel_type]