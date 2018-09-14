'''
Module which uploads all synsets and respective literals(lemmas) to 'all_synsets.db' database.

'''
from estnltk.wordnet import wn
import sqlite3

lastId = 39579 # last id in synset database for uploading data from this point.
pos = [wn.ADJ, wn.ADV, wn.VERB, wn.NOUN]
synsetList=[]
for i in pos:
    tmp = wn.all_synsets(i)
    for j in tmp:
        synsetList.append(j)     

synset_database_db = 'wordnet/data/all_synsets.db'
'''
for i in synsetList:
    ssetStr.append(str(i))

for i in range(len(ssetStr)):
    synsetName.append(ssetStr[i][9:-8])
    synsetSense.append(ssetStr[i][-5:-3])
    synsetPos.append(ssetStr[i][-7:-6])
'''

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
        print("\n\tConnection error: [%s]" % e)

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
        print("\n\tConnection error while creating table: [%s]" % e)

def sqlTables(databaseLoc):

    sql_create_synset_table = ''' CREATE TABLE IF NOT EXISTS synset_table(

                                        synset_id   integer NOT NULL,
                                        synset_word text,
                                        POS         text NOT NULL,
                                        sense       integer NOT NULL,
                                        literal     text
                                                    ); '''
    conn = create_connection(databaseLoc)
    if conn is not None:
        create_table(conn,sql_create_synset_table)
    else:
        print("\n\tError! cannot create db conn.")

def database_create(synset_database_db, lastId):
    #sqlTables(synset_database_db)
    conn = create_connection(synset_database_db)
    cursor=conn.cursor()
    j=0
    k=lastId
    with conn:
        literals = []
        for sset in synsetList[lastId:]:
            rsset = sset._raw_synset    
            sset_word = rsset.variants[0].literal
            sset_sense = rsset.variants[0].sense
            sset_pos   = rsset.pos
            for name in rsset.variants:
                sset_literal = []
                if name.literal == sset_word:
                    if len(rsset.variants) == 1:
                        sset_literal = None
                    else:
                        continue
                else: sset_literal = name.literal

                cursor.execute("INSERT INTO synset_table(synset_id, synset_word, POS, sense,literal) VALUES(?,?,?,?,?)"\
                                                            ,(k, sset_word,sset_pos, sset_sense, sset_literal) ) 
                conn.commit()
            k+=1
    
    conn.close()
    
database_create(synset_database_db,lastId)