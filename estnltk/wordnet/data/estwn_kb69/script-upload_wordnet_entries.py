'''
Module which uploads all synsets and respective literals(lemmas) to 'wordnet_synset.db' database.

'''
from estnltk.wordnet import wn
import sqlite3

synset_db = 'wordnet_entries.db'

pos = [wn.ADJ, wn.ADV, wn.VERB, wn.NOUN]
synsetList=[]
for i in pos:
    tmp = wn.all_synsets(i)
    for j in tmp:
        synsetList.append(j)

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

    sql_create_table = ''' CREATE TABLE IF NOT EXISTS wordnet_entries(

                                        synset_id   integer NOT NULL,
                                        synset_word text,
                                        pos         text NOT NULL,
                                        sense       integer NOT NULL,
                                        literal     text
                                                    ); '''
    conn = create_connection(databaseLoc)
    if conn is not None:
        create_table(conn,sql_create_table)
    else:
        print("\n\tError! cannot create db conn.")

def upload_synsets(synset_db):

    sqlTables(synset_db)
    conn = create_connection(synset_db)
    cursor=conn.cursor()
    j=0
    k=lastId
    with conn:
        print("uploading data to db..")
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
                        sset_literal = name.literal
                    else:
                        continue
                else: sset_literal = name.literal

                cursor.execute("INSERT INTO wordnet_entries(synset_id, synset_word, pos, sense,literal) VALUES(?,?,?,?,?)"\
                                                            ,(k, sset_word,sset_pos, sset_sense, sset_literal) ) 
            k+=1
        conn.commit()
            

upload_synsets(synset_db)
