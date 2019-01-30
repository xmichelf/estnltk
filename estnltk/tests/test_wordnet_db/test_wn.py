'''
Comparison of wordnet relations with https://teksaurus.keeleressursid.ee relations.
'''
import sys
sys.path.append('../../wordnet')

from wordnet import Wordnet
from synset import Synset

wn = Wordnet(version='74')

web_start_synset = ['käitumisakt', 'patutegu', 'väärdumine', 'kollane', 'None', 'puhklema','reduline','pakku minema',\
                             'redu', 'putkaja', 'piss', 'tennisisti küünarliiges', 'kats', 'tundehellus', 'atribuut', 'joonistama']

web_relation = ['hypernym', 'involved', 'hyponym', 'hypernym', 'None', 'agent', 'similar', 'agent',\
                     'agent', 'hyponym', 'hypernym', 'involved_patient', 'hypernym', 'hypernym', 'hypernym', 'hypernym']

idList=[2,9,815,12,13,14,15,16,17,18]

def test_relations():
    j=0
    for i in idList:
        relations = Synset(wn,i).get_related_synset()
        if relations[0][0].name is None:
            assert 'None' == web_start_synset[j]
            assert 'None' == web_relation[j]
            j+=1
            continue
            
        for relation in relations:
            assert relation[0].name[0:-4] == web_start_synset[j]
            assert relation[1] == web_relation[j]
            j+=1

test_relations()