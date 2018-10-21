
# coding: utf-8

# In[1]:


from estnltk.wordnet import wn
import sqlite3

pos = [wn.ADJ, wn.ADV, wn.VERB, wn.NOUN]
synsetList=[]


# In[2]:


# save all synsets from wn to synsetList
for i in pos:
    tmp = wn.all_synsets(i)
    for j in tmp:
        synsetList.append(j)        


# In[3]:


sset_db = 'wordnet/data/all_synsets.db'
relation_db = 'wordnet/data/all_relations.db'


# In[4]:


end_vrtx = []
start_vrtx = []
start_sset = []
end_sset = []
rel_type = []


# In[5]:


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


# In[122]:


def synset_str(synset_word, cursor):
    
    cursor.execute('SELECT POS, sense FROM synset_table WHERE synset_word = ?',(synset_word,))
    data = cursor.fetchone()
    var = "." + data[0] + "." + str(data[1])
    synset_word += var
    
    return synset_word
    


# In[123]:


def fetch_id(synset_word,cursor):
    
    cursor.execute('SELECT synset_id FROM synset_table WHERE synset_word = ?',(synset_word,))
    data = cursor.fetchone()

    return data[0]


# In[124]:


conn = create_connection(sset_db)
cursor = conn.cursor()
word = "kuu"
with conn:
    sset_id= fetch_id(word, cursor)
    word = synset_str(word, cursor)

print(word)


# In[53]:


def get_literals(synset_list):
    lit_word = []
    for sset in synset_list:
        for word in sset._raw_synset.variants:
            lit_word.append(word.literal)
    
    return lit_word


# In[8]:


def fetch_synsets(synset_db):
    '''
    Reads synsets from database in order first to last: synset_id - int, synset_word - str, POS - str, sense - int, literal- str
    '''
    
    conn = create_connection(synset_db)
    cursor = conn.cursor()
    with conn:
        #select all synsets with different indices from table.
        cursor.execute("SELECT DISTINCT synset_word FROM synset_table")
        for row in cursor.fetchall():
            synsetList.append(row[0])
    


# In[9]:


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
                            start_sset.append(synset_str(word,cursor))
                            end_sset.append(synset_str(sset_word, cursor))
                            #print(word)
                            start = fetch_id(word,cursor)
                            if start is not None:
                                     start_vrtx.append(start[0])
                            if end is not None:
                                     end_vrtx.append(end[0])                                
                    elif len(rel_word) == 1:
                        end_sset.append(synset_str(sset_word, cursor))
                        start_sset.append(synset_str(rel_word, cursor))
                        start = fetch_id(rel_word[0],cursor)
                        #print(start)
                        if start is not None:
                            start_vrtx.append(start[0])
                        if end is not None:
                            end_vrtx.append(end[0])
                i+=1
                    


# In[10]:


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


# In[11]:


def synset_name(raw_synset):
    pos = raw_synset.pos
    literal = raw_synset.variants[0].literal
    sense = "%02d"%raw_synset.variants[0].sense
    return '.'.join([literal,pos,sense])


# In[54]:


sset = synsetList[0]
sset_string = synset_name(sset._raw_synset)
print(sset_string)
print(sset._raw_synset.pos)
#sset_li = get_literals(synsetList[0])


# In[ ]:


i=0
start_sset[0]
for word in start_sset:
    print(word[0])
    if word[0] == '[':
        print(word)
        print(i)
    i+=1


# In[ ]:


#synsetList = []
#fetch_synsets(sset_db)


# In[ ]:


start_vrtx = []
end_vrtx   = []
end_sset   = []
start_sset = []
rel_type = []

fetch_relations(sset_db)


# In[ ]:


#First holonym @ index 11186,  meronym @ 11184, hyponym @ 123
upload_relations(relation_db)


# In[ ]:


print(len(start_vrtx))
len(end_vrtx)


# In[ ]:


def synset_name(raw_synset):
    pos = raw_synset.pos
    literal = raw_synset.variants[0].literal
    sense = "%02d"%raw_synset.variants[0].sense
    return '.'.join([literal,pos,sense])


# In[ ]:


hyperList = []
for sset in synsetList:
    if sset.get_related_synsets("has_hyperonym"):
        var = sset.get_related_synsets("has_hyperonym")[0]
        print(var)
        rsset = var._raw_synset
        name = rsset.variants[0].literal
        print(name)
        
        #print("synset: ", sset)
        #print("hyperonym: ", sset.get_related_synsets("has_hyperonym")[0])


# In[ ]:


'''cycle for relations - hyponym,hypernym, etc.'''   
for sset in synsetList:
        rsset = sset._raw_synset
        #print(sset)
        for relation_candidate in rsset.internalLinks:
            linked_synset = wn.synset(wn._get_key_from_raw_synset(relation_candidate.target_concept))
            relation_candidate.target_concept = linked_synset._raw_synset
            #print(relation_candidate.target_concept)
            #print(linked_synset)
            #print(relation_candidate.name)            
            '''
            sset_literal    =relation_candidate.target_concept.variants[0].literal
            sset_sense      =relation_candidate.target_concept.variants[0].sense
            sset_pos        =rsset.pos
            #[nimi.literal for nimi in rsset.variants ]
            '''

