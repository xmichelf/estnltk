'''
Script which uploads all relations, their start and end vertex ID-s with relation to all_synsets.db IDs.
Note: this database is for graph.

'''


import estnltk
from estnltk.wordnet import wn
import sqlite3


ssetC = wn.Synset
file_db       = 'wordnet/data/all_synsets.db'
graph_db ='wordnet/data/relations_graph_db'

pos = [wn.ADJ, wn.ADV, wn.VERB, wn.NOUN]
synsetsDb = []
start_vrtx = []
end_vrtx   = []
relation_list =[]

for i in pos:
    tmp = wn.all_synsets(i)
    for j in tmp:
        synsetsDb.append(j)

def relation_test(cursor, synset, relation_str,end_vtx_id):
    
    if synset:
        if len(synset) > 1:
            #print(relation_str)
            for sset in synset:                
                tmp=str(sset)
                sset_name = tmp[9:-8]
                pos       = tmp[-7:-6]
                sense     = tmp[-5:-3]
                '''
                print(tmp)
                print(sset_name)
                print(pos)
                print(sense)
                '''
                cursor.execute('SELECT synset_id FROM synset_table WHERE synset_word = ? AND POS = ? AND sense = ?',(sset_name,pos,sense))
                row=cursor.fetchall()
                #print(row[0][0])
                start_vrtx.append(row[0][0])
                end_vrtx.append(end_vtx_id)
                relation_list.append(relation_str)
        if len(synset) == 1:
            tmp=str(synset)
            sset_name = tmp[10:-9]
            pos       = tmp[-8:-7]
            sense     = tmp[-6:-4]
            cursor.execute('SELECT synset_id FROM synset_table WHERE synset_word = ? AND POS = ? AND sense = ?',(sset_name,pos,sense))
            row=cursor.fetchall()
            '''
            print(relation_str)
            print(row)
            print(synset)
            print(pos)
            print(sense)
            '''
            start_vrtx.append(row[0][0])
            end_vrtx.append(end_vtx_id)
            relation_list.append(relation_str)


def upload_hypernyms(file_db):

    conn = sqlite3.connect(file_db)
    cursor=conn.cursor()
    with conn:
        for i in range(len(synsetsDb)):
            #print("i: ", i)
            #print(synsetsDb[i])
            hypernym = ssetC.hypernyms(synsetsDb[i])
            hyponym  = ssetC.hyponyms(synsetsDb[i])
            holonym  = ssetC.holonyms(synsetsDb[i])
            meronym  = ssetC.meronyms(synsetsDb[i])
            relation_test(cursor,hypernym, "hypernym", i)
            relation_test(cursor,hyponym, "hyponym",  i)
            relation_test(cursor,holonym, "holonym", i)
            relation_test(cursor,meronym, "meronym", i)
                


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

    sql_create_synset_table = ''' CREATE TABLE IF NOT EXISTS relations_graph(

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

def upload_graph_data(graph_db):

    sqlTables(graph_db)
    conn = create_connection(graph_db)
    cursor=conn.cursor()
    with conn:
        for i in range(len(relation_list)):
            start = start_vrtx[i]
            end   = end_vrtx[i]
            tmp = str(synsetsDb[start])
            start_sset = tmp[9:-8]
            tmp   = str(synsetsDb[end])
            end_sset = tmp[9:-8]
            cursor.execute("INSERT INTO relations_graph(start_vertex, start_synset, end_synset, end_vertex, relation) VALUES(?,?,?,?,?)"\
                                                                ,(start, start_sset, end_sset, end, relation_list[i]))
            conn.commit()

upload_hypernyms(file_db)
upload_graph_data(graph_db)
