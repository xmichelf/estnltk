'''
Script which uploads all relations, their start and end vertex ID-s with relation to wordnet_relations.db IDs.
Note: this database is for graph.

'''


from estnltk.wordnet import wn
import sqlite3

# save all synsets from wn to synsetList
pos = [wn.ADJ, wn.ADV, wn.VERB, wn.NOUN]
synsetList=[]
for i in pos:
    tmp = wn.all_synsets(i)
    for j in tmp:
        synsetList.append(j)        

sset_db = '../../data/estwn_kb69/wordnet_entries.db'
relation_db = '../../data/estwn_kb69/wordnet_relations.db'

start_vrtx = []
end_vrtx   = []
end_sset   = []
start_sset = []
rel_type = []
#sset_word =[]

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

    sql_create_table = ''' CREATE TABLE IF NOT EXISTS wordnet_relations(

                                        start_vertex INT,
                                        start_synset TEXT,
                                        end_synset TEXT,
                                        end_vertex INT,
                                        relation TEXT
                                                    ); '''
    conn = create_connection(databaseLoc)
    if conn is not None:
        create_table(conn,sql_create_table)
    else:
        print("Error! cannot create db conn.")

def fetch_id(synset_word,cursor):
    cursor.execute('SELECT synset_id FROM wordnet_entries WHERE synset_word = ?',(synset_word,))
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
    Reads synsets from database in order - first to last: 
    synset_id - int, synset_word - str, POS - str, sense - int, literal- str
    '''
    
    conn = create_connection(synset_db)
    cursor = conn.cursor()
    with conn:
        #select all synsets with different indices from table.
        cursor.execute("SELECT DISTINCT synset_word FROM wordnet_entries")
        for row in cursor.fetchall():
            synsetList.append(row[0])

#TODO: upload whole synset string to sset_start and sset_end columns (name.n.0x) 
def synset_name(raw_synset):
    pos = raw_synset.pos
    literal = raw_synset.variants[0].literal
    sense = "%02d"%raw_synset.variants[0].sense
    return '.'.join([literal,pos,sense])

def synset_str(synset_word, cursor):
    cursor.execute('SELECT pos, sense FROM wordnet_entries WHERE synset_word = ?',(synset_word,))
    data = cursor.fetchone()
    if data is not None:
        var = "." + data[0] + "." + str(data[1])
        synset_word += var
    else: return None
    
    return synset_word

def fetch_relations(db_file):
    
    relationList = ["has_hyperonym", "has_hyponym", "has_holonym", "has_meronym", "has_member_holo"]
    relation_str = ["hyperonym", "hyponym", "holonym", "meronym", "member_holonym"]
    conn = create_connection(db_file)
    cursor = conn.cursor()
    
    with conn:
        for sset in synsetList:
            i=0
            sset_word = sset._raw_synset.firstVariant.literal
            end = fetch_id(sset_word,cursor) 
            sset_str = synset_str(sset_word, cursor)
            for rel in relationList:
                rel_sset_list = sset.get_related_synsets(rel)
                if rel_sset_list:                 
                    rel_word = get_literals(rel_sset_list)
                    '''
                    # FIXME: few words from wn are returned in form of single list "[word]" instead of "word".
                    if len(rel_word) == 1:
                        rel_word = rel_word[0]
                    #~~~
                   ''' 
                    start = []
                    if len(rel_word) > 1 and rel_word[0] is not '[':
                        for word in rel_word:
                            rel_type.append(relation_str[i])
                            word_str = synset_str(word,cursor)
                            start_sset.append(word_str)
                            end_sset.append(sset_str)
                            start = fetch_id(word,cursor)
                            #if start is not None:
                            start_vrtx.append(start)
                            #if end is not None:
                            end_vrtx.append(end)
                            #else: end_vrtx.append("None")
                    elif len(rel_word) == 1:
                        rel_type.append(relation_str[i]) 
                        rel_str = synset_str(rel_word[0], cursor)
                        end_sset.append(sset_str)
                        start_sset.append(rel_str)
                        start = fetch_id(rel_word[0],cursor)
                        #if start is not None:
                        start_vrtx.append(start)
                        #if end is not None:
                        end_vrtx.append(end)
                        #else: end_vrtx.append("None")
                i+=1

def upload_relations(db_file):
    
    sqlTables(db_file)
    conn = create_connection(db_file)
    cursor = conn.cursor()
    
    with conn:
        print("Uploading relations to db...")
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
            cursor.execute("INSERT INTO wordnet_relations(start_vertex, start_synset, end_synset, end_vertex, relation)\
                                            VALUES(?,?,?,?,?)",(start_vrtx[i], start_word, end_sset[i], end_vrtx[i],rel_type[i]))
        conn.commit()

fetch_relations(sset_db)
#First holonym @ index 11186,  meronym @ 11184, hyponym @ 123
upload_relations(relation_db)
