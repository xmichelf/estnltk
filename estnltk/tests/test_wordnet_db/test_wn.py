'''
Comparison of wordnet relations with https://teksaurus.keeleressursid.ee relations.
'''

from estnltk.wordnet import Wordnet

wn = Wordnet(version='74')

source_pos = {'patustamine': 'n',
              'päevalillekollane': 'a',
              'õigusetu': 'a', # id 815
              'puhiseja': 'n',
              'pageja': 'n',
              'miktsioonuriin': 'n',
              'Millsi test': 'n',
              'liigutustundlikkus': 'n',
              'limaskestabarjäär': 'n',
              'tuššima': 'v',
              'väikettevõtja' : 'n', #id 104
              'bombard': 'n', #id 1969
              'kiin': 'n' #id 2943
             }

source_sense = {'patustamine': 1,
                'päevalillekollane': 1,
                'õigusetu': 1,
                'puhiseja': 1,
                'pageja': 1,
                'miktsioonuriin': 1,
                'Millsi test': 1,
                'liigutustundlikkus': 1,
                'limaskestabarjäär': 1,
                'tuššima': 1,
                'väikettevõtja' : 1,
                'bombard': 1,
                'kiin':3  
                }



def test_relations():
    source_relation = [ 'patustamine', 'päevalillekollane', 'õigusetu', 'puhiseja', 'pageja', 'miktsioonuriin',  'Millsi test', 'liigutustundlikkus', 'limaskestabarjäär', 'tuššima']

    target_relations = {}
    for relation in source_relation:
        target_relations[relation] = {}
    target_relations['patustamine']['hypernym'] = {'käitumine'}
    target_relations['patustamine']['involved'] =  {'patt'}
    target_relations['patustamine']['hyponym'] = {'väärdumine'}
    target_relations['päevalillekollane']['hypernym'] = {'kollane'}
    target_relations['õigusetu']['null'] = {None}
    target_relations['puhiseja']['agent'] = {'puhkima'}
    target_relations['pageja']['similar'] = {'reduline'}
    target_relations['pageja']['agent'] = {'põgenema','redu'}
    target_relations['pageja']['hyponym'] = {'putkaja'}
    target_relations['miktsioonuriin']['hypernym'] = {'kusi'}
    target_relations['Millsi test']['involved_patient'] = {'tennisisti_küünarliiges'}
    target_relations['Millsi test']['hypernym'] = {'kats'}
    target_relations['liigutustundlikkus']['hypernym'] = {'sensitiivsus'}
    target_relations['limaskestabarjäär']['hypernym'] = {'omadus'}
    target_relations['tuššima']['hypernym'] = {'joonistama'}

    for source_node in source_relation:
        source = wn.get_synset(source_node, source_pos[source_node], source_sense[source_node])
        if source is None:
            continue
        source_name = source.name[:-4]
        relations = source.get_related_synset() 
        for relation in relations:
            rel_type = relation[1]
            if rel_type == 'null':
                assert None in target_relations[source_name][rel_type]
                continue
            rel_name = relation[0].name[0:-4]
            assert rel_name in target_relations[source_name][rel_type]


def test_root_hypernyms():
    source_nodes = ['õigusetu', 'väikettevõtja', 'bombard']
    target_depth = {}

    for key in source_nodes:
        target_depth[key] = {}
        
    #emtpy relation    
    target_depth['õigusetu'][1] = {}

    #hypernym
    target_depth['väikettevõtja'][1] = {'ettevõtja', 'väikeettevõte'}
    target_depth['väikettevõtja'][2] = {'bisnismen', 'käitis'}
    target_depth['väikettevõtja'][3] = {'inimene', 'asutus'}
    target_depth['väikettevõtja'][4] = {'elusolend', 'sotsiaalne_grupp'}
    target_depth['väikettevõtja'][5] = {'olend', 'grupp'}
    target_depth['väikettevõtja'][6] = {'olev', 'miski'}

    #outbrancing hypernym
    target_depth['bombard'][1] = {'kahur'}
    target_depth['bombard'][2] = {'mehhanism', 'tulirelv'}
    target_depth['bombard'][3] = {'funktsioneerimine', 'riistapuu', 'laskerelv'}
    target_depth['bombard'][4] = {'töö', 'vahend', 'relv'}
    target_depth['bombard'][5] = {'tegevus', 'asi', 'riistapuu', 'tegevus'}
    target_depth['bombard'][6] = {'tegevus', 'objekt', 'vahend'}
    target_depth['bombard'][7] = {'tegevus', 'olev', 'asi'}
    target_depth['bombard'][8] = {'tegevus', 'olev', 'objekt'}
    target_depth['bombard'][9] = {'tegevus', 'olev'}

    #root_hypernyms test
    for source_node in source_nodes:
        source = wn.get_synset(source_node, source_pos[source_node], source_sense[source_node])
        if source is None:
            continue
        source_word = source.name[:-4]
        for depth in range(1, len(target_depth[source_word])+1):
            result = list(source.root_hypernyms(depth_threshold=depth, return_depths=False))
            for sset in result:
                source_word = source.name[:-4]
                assert sset.name[:-4] in target_depth[source_word][depth]


def test_closure():
    source_nodes = ['õigusetu', 'väikettevõtja', 'bombard', 'kiin']
    target_depth = {}

    for key in source_nodes:
        target_depth[key] = {}
        
    #emtpy relation    
    target_depth['õigusetu'][1] = {}

    #hypernym
    target_depth['väikettevõtja'][1] = {'ettevõtja', 'väikeettevõte'}
    target_depth['väikettevõtja'][2] = {'bisnismen', 'käitis'}
    target_depth['väikettevõtja'][3] = {'inimene', 'asutus'}
    target_depth['väikettevõtja'][4] = {'elusolend', 'sotsiaalne_grupp'}
    target_depth['väikettevõtja'][5] = {'olend', 'grupp'}
    target_depth['väikettevõtja'][6] = {'olev', 'miski'}

    #outbrancing hypernym
    target_depth['bombard'][1] = {'kahur'}
    target_depth['bombard'][2] = {'mehhanism', 'tulirelv'}
    target_depth['bombard'][3] = {'funktsioneerimine', 'riistapuu', 'laskerelv'}
    target_depth['bombard'][4] = {'töö', 'vahend', 'relv'}
    target_depth['bombard'][5] = {'tegevus', 'asi', 'riistapuu', 'tegevus'}
    target_depth['bombard'][6] = {'tegevus', 'objekt', 'vahend'}
    target_depth['bombard'][7] = {'tegevus', 'olev', 'asi'}
    target_depth['bombard'][8] = {'tegevus', 'olev', 'objekt'}
    target_depth['bombard'][9] = {'tegevus', 'olev'}
    # test with hyponym relation as well.
    target_depth['kiin'] = {}
    target_depth['kiin'][1] = {'ninakiin', 'nahakiin', 'maokiin'}
    target_depth['kiin'][2] = {'lamba-ninakiin', 'põhjapõdra-nahakiin', 'veise-nahakiin', 'maokiin'}
    #closure test
    relation_type='hypernym'
    for source_node in source_nodes:
        source = wn.get_synset(source_node, source_pos[source_node], source_sense[source_node])
        if source is None:
            continue
        if source.name[:-4] == 'kiin':
            relation_type = 'hyponym'

        source_word = source.name[:-4]
        for depth in range(1, len(target_depth[source_word])+1):
            results = list(source.closure(relation=relation_type, depth_threshold=depth, return_depths=False))
            for result in results:
                source_word = source.name[:-4]
                assert result.name[:-4] in target_depth[source_word][depth]