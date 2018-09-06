
'''
Module which uploads all synsets to 'all_synsets.db' database.

'''

from estnltk.wordnet import wn
import sqlite3

synset_database_db = 'estnltk/wordnet/data/all_synsets_new.db'
pos = [wn.ADJ, wn.ADV, wn.VERB, wn.NOUN]
synsetList =[]
for i in pos:
    tmp = wn.all_synsets(i)
    for j in tmp:
        synsetList.append(j)

print(len(synsetList))


synsetPos   = []
synsetName  = []
synsetSense =[]

ssetStr = []

for i in synsetList:
    ssetStr.append(str(i))

for i in range(len(ssetStr)):
    synsetName.append(ssetStr[i][9:-8])
    synsetSense.append(ssetStr[i][-5:-3])
    synsetPos.append(ssetStr[i][-7:-6])

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

    sql_create_synset_table = ''' CREATE TABLE IF NOT EXISTS synset_table(

                                        synset_id INT NOT NULL,
                                        synset_word TEXT NOT NULL,
                                        literal     TEXT NOT NULL
                                        POS         CHAR NOT NULL,
                                        sense       INT NOT NULL
                                                    ); '''
    conn = create_connection(databaseLoc)
    if conn is not None:
        create_table(conn,sql_create_synset_table)
    else:
        print("Error! cannot create db conn.")

def database_create(synset_database_db):
    sqlTables(synset_database_db)
    conn = create_connection(synset_database_db)
    cursor=conn.cursor()
    i=j=0
    with conn:
        literals = []
        for sset in synsetList:
            rsset = sset._raw_synset
            for relation_candidate in rsset.internalLinks:

                sset_literal    =relation_candidate.target_concept.variants[0].literal
                sset_sense      =relation_candidate.target_concept.variants[0].sense
                sset_pos        =rsset.pos
                #[nimi.literal for nimi in rsset.variants ]
                for name in rsset.variants:
                    if len(name.literal) == 1:
                        literal = None
                    elif name == rsset.variants[0]:
                        literal = None
                    else: sset_literal = name
                    print("lit. > 1 !")
                    
                    cursor.execute("INSERT INTO synset_table(synset_id, synset_word, literal, POS, sense) VALUES(?,?,?,?)",(i, sset_word, literal,pos, sense) ) 
                    conn.commit()
            i+=1
    
    conn.close()

database_create(synset_database_db)

