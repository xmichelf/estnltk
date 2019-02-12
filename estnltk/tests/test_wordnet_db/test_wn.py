'''
Comparison of wordnet relations with https://teksaurus.keeleressursid.ee relations.
'''
from estnltk.wordnet import Wordnet
from estnltk.wordnet import Synset

wn = Wordnet(version='74')

source_literal = [ 'patustus', 'päevalillekollane', 'õigusetu', 'puhiseja', 'pageja', 'miktsioonuriin',  'Millsi test', 'liigutustundlikkus', 'limaskestabarjäär', 'tuššima']

source_pos = {}
source_sense = {}

source_pos['patustus'] = 'n'
source_sense['patustus'] = 1

source_pos['päevalillekollane'] = 'a'
source_sense['päevalillekollane'] = 1

source_pos['õigusetu'] = {}
source_sense['õigusetu'] = {} 

source_pos['puhiseja'] =  'n' 
source_sense['puhiseja'] = 1

source_pos['pageja'] = 'n'
source_sense['pageja'] = 1

source_pos['miktsioonuriin'] = 'n'
source_sense['miktsioonuriin'] = 1

source_pos['Millsi test'] = 'n'
source_sense['Millsi test'] = 1

source_pos['liigutustundlikkus'] = 'n'
source_sense['liigutustundlikkus'] = 1

source_pos['limaskestabarjäär'] = 'n'
source_sense['limaskestabarjäär'] = 1

source_pos['tuššima'] = 'v'
source_sense['tuššima'] = 1


target_relations = {}
for relation in source_literal:
    target_relations[relation] = {}

target_relations['patustus']['hyponym'] = {'käitumisakt'}
target_relations['patustus']['involved'] =  {'patutegu'}
target_relations['patustus']['hypernym'] = {'väärdumine'}
target_relations['päevalillekollane']['hypernym'] = {'kollane'}
target_relations['õigusetu'][] = {}
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


def test_relations():
    for source_node in source_relation:
        source = wn.get_synset(source_pos[source_node], source_sense[source_node], source_node)
        source_name = source.name[:-4]
        relations = source.get_related_synset() 
        for relation in relations:
            if relation[0].name is None:
                assert None in target_relations[source_name][None]
                continue
            rel_name = relation[0].name[0:-4]
            assert rel_name in target_relations[source_name]


source_nodes = ['õigusetu', 'väikettevõtja', 'bombard']
target_depth = {}
for key in source_nodes:
    target_depth[key] = {}

target_depth['väikettevõtja'][1] = {'ettevõtja', 'väikettevõte'}
target_depth['väikettevõtja'][2] = {'bisnismen', 'käitis'}
target_depth['väikettevõtja'][3] = {'inimene', 'asutus'}
target_depth['väikettevõtja'][4] = {'elusolend', 'sotsiaalne_grupp'}
target_depth['väikettevõtja'][5] = {'olend', 'grupp'}
target_depth['väikettevõtja'][6] = {'olev', 'miski'}
target_depth['bombard'][1] = {'kahur'}
target_depth['bombard'][2] = {'mehhanism', 'tulirelv'}
target_depth['bombard'][3] = {'funktsioneerimine', 'riistapuu', 'laskerelv'}
target_depth['bombard'][4] = {'töö', 'vahend', 'relv'}
target_depth['bombard'][5] = {'tegevus', 'asi', 'riistapuu', 'tegevus'}
target_depth['bombard'][6] = {'objekt', 'vahend'}
target_depth['bombard'][7] = {'olev', 'asi'}
target_depth['bombard'][8] = {'objekt'}
target_depth['bombard'][9] = {'olev'}

target_depth['õigusetu'][1] = {}

#id 815
source_pos['õigusetu'] = 'a'
source_sense['õigusetu'] = 1

#id 104
source_pos['väikettevõtja'] = 'n'
source_sense['väikettevõtja'] = 1

#id 1969
source_pos['bombard'] = 'n'
source_sense['bombard'] = 1


def test_root_hypernyms():

    #root_hypernyms test
    for source_node in source_nodes:
        source = wn.get_synset(source_pos[source_node], source_sense[source_node], source_node)
        assert source_pos[source_node] == source.pos
        assert source_sense[source_node] == source.sense

        for depth in source.root_hypernyms(depth_threshold=float('inf'), return_depths=True):
            threshold = depth[1]

            for relation in source.root_hypernyms(depth_threshold=threshold, return_depths=True):
                synset_word = relation[0].name[:-4]
                depth_2 = relation[1]
                source_word = source.name[:-4]
                assert synset_word in target_depth[source_word][depth]


def test_closure():
    #closure test
    for source_node in source_nodes:
        source = wn.get_synset(source_pos[source_node], source_sense[source_node], source_node)
        for depth in source.closure(relation='hypernym', depth_threshold=float('inf'), return_depths=True):
            threshold = depth[1]

            for relation in source.closure(relation='hypernym', depth_threshold=threshold, return_depths=True):
                synset_word = relation[0].name[:-4]
                depth_2 = relation[1]
                source_word = source.name[:-4]
                assert synset_word in target_depth[source_word][depth_2]
