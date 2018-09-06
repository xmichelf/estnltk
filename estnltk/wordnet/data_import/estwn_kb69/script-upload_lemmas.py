'''
This script uploads all literals with corresponding id, synsets,pos and sense to database 'literals_db'
'''

from estnltk.wordnet import wn
import os
import sqlite3


literals_db  = 'estnltk/wordnet/data/literals.db'
pos = [wn.ADJ, wn.ADV, wn.VERB, wn.NOUN]

sset_db = []
synsetList = []

ssetWords = []
posList = []
sense = []

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

    sql_create_synset_table = ''' CREATE TABLE IF NOT EXISTS synset_literals(

                                        ID INT NOT NULL,
                                        synset TEXT NOT NULL,
                                        lemma TEXT NOT NULL,
                                        POS TEXT NOT NULL,
                                        sense INT NOT NULL
                                                    ); '''
    conn = create_connection(databaseLoc)
    if conn is not None:
        create_table(conn,sql_create_synset_table)
    else:
        print("Error! cannot create db conn.")

def list2data():
    for i in synsetList:
        ssetWords.append(i[9:-8])
        posList.append(i[-5:-3])
        sense.append(i[-7:-6])

def upload_literals(upload_db):
    
    j=0
    sqlTables(upload_db)
    conn = create_connection(upload_db)
    cursor=conn.cursor()
    with conn:
        for sset in sset_db:      
            rsset=sset._raw_synset
            i=0
            for sset2 in rsset._variants:
                if i == 0:
                    i+=1
                    continue
                cursor.execute("INSERT INTO synset_literals(ID, synset, lemma, POS, sense) VALUES(?,?,?,?,?)",(j, ssetWords[j], str(sset2.literal), posList[j], sense[j]))
                conn.commit()
                i+=1 
            j+=1


#get all synsets to lists
for i in pos:
    tmp = wn.all_synsets(i)
    for j in tmp:
        synsetList.append(str(j)) #sset strings
        sset_db.append(j)         #sset objects
        

list2data() # extract word, sense and pos from synset string

upload_literals(literals_db) # get literals and upload to database



