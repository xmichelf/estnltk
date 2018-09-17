'''
Script which uploads all relations, their start and end vertex ID-s with relation to all_relations.db IDs.
Note: this database is for graph.

'''



# coding: utf-8

from estnltk.wordnet import wn
import sqlite3

pos = [wn.ADJ, wn.ADV, wn.VERB, wn.NOUN]
synsetList=[]


# save all synsets from wn to synsetList
#TODO: when all synsets are in database, then fetch from db. Fetch_relations function has to be reworked in this case.
for i in pos:
    tmp = wn.all_synsets(i)
    for j in tmp:
        synsetList.append(j)        


sset_db = 'wordnet/data/all_synsets.db'
relation_db = 'wordnet/data/all_relations.db'

start_vrtx = []
end_vrtx   = []
end_sset   = []
start_sset = []
rel_type = []


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print("Connection error: [%s]" % e)

    return None

def create_table(conn, create_table_sql ):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print("Connection error while creating table: [%s]" % e)

def sqlTables(databaseLoc):

    sql_create_synset_table = ''' CREATE TABLE IF NOT EXISTS graph_table(

                                        start_vertex INT NOT NULL,
                                        start_synset TEXT NOT NULL,
                                        end_synset TEXT NOT NULL,
                                        end_vertex INT NOT NULL,
                                        relation TEXT NOT NULL
                                                    ); '''
    conn = create_connection(databaseLoc)
    if conn is not None:
        create_table(conn,sql_create_synset_table)
    else:
        print("Error! cannot create db conn.")


def fetch_id(synset_word,cursor):
    cursor.execute('SELECT synset_id FROM synset_table WHERE synset_word = ?',(synset_word,))
    sset_id = cursor.fetchone()
    
    return sset_id


def get_literals(synset_list):
    lit_word = []
    for sset in synset_list:
        for word in sset._raw_synset.variants:
            lit_word.append(word.literal)
    
    return lit_word


def fetch_synsets(synset_db):
    '''
    Reads synsets from database in order first to last: 
    synset_id - int, synset_word - str, POS - str, sense - int, literal- str
    '''
    
    conn = create_connection(synset_db)
    cursor = conn.cursor()
    with conn:
        #select all synsets with different indices from table.
        cursor.execute("SELECT DISTINCT synset_word FROM synset_table")
        for row in cursor.fetchall():
            synsetList.append(row[0])
    


def fetch_relations(db_file):
    
    relationList = ["has_hyperonym", "has_hyponym", "has_holonym", "has_meronym"]
    relation_str = ["hyperonym", "hyponym", "holonym", "meronym"]
    conn = create_connection(db_file)
    cursor = conn.cursor()
    
    with conn:
        for sset in synsetList:
            i=0
            sset_word = sset._raw_synset.firstVariant.literal
            end = fetch_id(sset_word,cursor) 
            for rel in relationList:
                rel_sset_list = sset.get_related_synsets(rel)
                if rel_sset_list:
                    rel_type.append(relation_str[i])                  
                    rel_word = get_literals(rel_sset_list)
                    start = []
                    if len(rel_word) > 1:
                        for word in rel_word:
                            start_sset.append(word)
                            end_sset.append(sset_word)
                            rel_type.append(relation_str[i])
                            #print(word)
                            start = (fetch_id(word,cursor))
                            if start is not None:
                                     start_vrtx.append(start[0])
                            if end is not None:
                                     end_vrtx.append(end[0])                                
                    elif len(rel_word) == 1:
                        end_sset.append(sset_word)
                        start_sset.append(rel_word)
                        start = fetch_id(rel_word[0],cursor)
                        rel_type.append(relation_str[i])
                        #print(start)
                        if start is not None:
                            start_vrtx.append(start[0])
                        if end is not None:
                            end_vrtx.append(end[0])
                i+=1
                    


def upload_relations(db_file):
    
    sqlTables(db_file)
    conn = create_connection(db_file)
    cursor = conn.cursor()
    
    with conn:
        for i in range(len(start_vrtx)):
            start_id   = start_vrtx[i]
            #FIXME
            if len(start_sset[i]) == 1:
                start_word = start_sset[i][0]
            else:
                start_word = str(start_sset[i])
            #~~~
            end_word   = str(end_sset[i])
            end_id     = end_vrtx[i]
            relation   = rel_type[i]
            cursor.execute("INSERT INTO graph_table(start_vertex, start_synset, end_synset, end_vertex, relation) VALUES(?,?,?,?,?)"                                                            ,(start_id, start_word, end_word, end_id,relation))
            conn.commit()

fetch_relations(sset_db)
#First holonym @ index 11186,  meronym @ 11184, hyponym @ 123
upload_relations(relation_db)



