'''(py35) jaan@mouni:~/Projects/estnltk$ /home/jaan/anaconda3/envs/estnltk/bin/python /home/jaan/Projects/estnltk/estnltk/wordnet/data_import/estwn_kb73/script-all_synsets_upload.py
65517
Connection error while creating table: [near "POS": syntax error]
Traceback (most recent call last):
  File "/home/jaan/Projects/estnltk/estnltk/wordnet/data_import/estwn_kb73/script-all_synsets_upload.py", line 101, in <module>
    database_create(synset_database_db)
  File "/home/jaan/Projects/estnltk/estnltk/wordnet/data_import/estwn_kb73/script-all_synsets_upload.py", line 93, in database_create
    sense = "%02d"%raw_synset.variants[0].sense
NameError: name 'raw_synset' is not defined
'''
#TODO: 2 import scripts in estwn_kb69a
#kontroll: lugeda data txt faili ning lugeda ridade numbrid
#-TODO uurida välja kuidas wn.get_related_synsets tagastab synsetid ok 

#TODO: def synset class which contains igraph vertex. Holding attributes of current wn.py : 199.
'''
def synset(LEMMA, POS):
    select vertex_ID
    where lemma = LEMMA
    or POS = POS
'''

#TODO: wordnet_relation start_vertex not matching wordnet_entries id.