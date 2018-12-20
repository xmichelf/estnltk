'''
This script creates three databases from xml database. - xml_synset.db ,xml_lexical_entry.db, xml_relation.db.

Author: Jaan Kalder
date: 15.12.18
'''


from lxml import etree
import sqlite3

xml_entry_db = 'xml_lexical_entry-2.db'
xml_sset_db = 'xml_synset-2.db'
xml_rel_db = 'xml_relation-2.db'

tree = etree.parse("../../source_data/estwn_kb74/estwn-et-2.0.0.beta.xml")

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


def entryTable(databaseLoc):

    sql_create_synset_table = ''' CREATE TABLE IF NOT EXISTS xml_lexical_entry(
                                        
                                        estwn_id TEXT,
                                        synset,
                                        written_form TEXT,
                                        pos TEXT ,
                                        sense INT 
                                                    ); '''
    conn = create_connection(databaseLoc)
    if conn is not None:
        create_table(conn,sql_create_synset_table)
    else:
        print("Error! cannot create db conn.")        

def synsetTable(databaseLoc):

    sql_create_synset_table = ''' CREATE TABLE IF NOT EXISTS xml_synset(
                                        
                                        id INT NOT NULL,
                                        estwn_id TEXT NOT NULL,
                                        source_sense TEXT NOT NULL
                                                    ); '''
    conn = create_connection(databaseLoc)
    if conn is not None:
        create_table(conn,sql_create_synset_table)
    else:
        print("Error! cannot create db conn.")  
        
def rel_table(databaseLoc):

    sql_create_synset_table = ''' CREATE TABLE IF NOT EXISTS xml_relation(

                                        start_estwn TEXT NOT NULL,
                                        end_estwn TEXT NOT NULL,
                                        relation TEXT NOT NULL
                                                    ); '''
    conn = create_connection(databaseLoc)
    if conn is not None:
        create_table(conn,sql_create_synset_table)
    else:
        print("Error! cannot create db conn.")

def fetch_entry():
    synsets = tree.xpath('/LexicalResource/Lexicon/LexicalEntry')
    j=0
    for sset in synsets:
        if len(sset)>1:
            for i in range(1, len(sset)):
                #status_list.append(sset[i].attrib['status'])
                sset_list.append(sset[i].attrib['id'])
                pos_list.append(sset[0].attrib['partOfSpeech'])
                lemma_list.append(sset[0].attrib['writtenForm'])
                estwnId_list.append(sset[i].attrib['synset'])
                sense = sset[i].attrib['id']
                sense_list.append(sense[-1:])           
        else:
            try:
                pos_list.append(sset[0].attrib['partOfSpeech'])
                lemma_list.append(sset[0].attrib['writtenForm'])
                word = sset[0].attrib['writtenForm']
                
                if " " in word:
                    var = word.replace(" ", "_")
                    word = var
                sset_list.append( "s-" + word + "-" + sset[0].attrib['partOfSpeech'] )
                
                estwnId_list.append('null')
                sense = sset.attrib['id']
                sense_list.append(sense[-1:])
                status_list.append("null")
            except:
                #print("pass @",j)
                pass
        j+=1


def fetch_synset(entry_xml_db):
    '''
     Appends to list estwn-id and sourceSense from xml database.
    '''
    synsets = tree.xpath('/LexicalResource/Lexicon/Synset')
    
    conn = create_connection(entry_xml_db)
    cursor = conn.cursor()
    with conn:
        i=0
        j=0
        for sset in synsets:
            estwnId_list.append(sset.attrib['id'])
            try:
                var   = sset[0].attrib['sourceSense']
                sset_word.append(var[2:-3])

            except:
                cursor.execute("SELECT written_form FROM xml_lexical_entry WHERE estwn_id = ?", (sset.attrib['id'],))
                row = cursor.fetchone()
                sset_word.append(row[0])

def fetch_relation():

    synsetList  = tree.xpath('/LexicalResource/Lexicon/Synset')
    for sset in synsetList: 
        end = sset.attrib['id']        
        if len(sset) > 1:
            for subset in sset[1:]:
                try:
                    start_estwn.append(subset.attrib['target'])
                    rel_type.append(subset.attrib['relType'])
                    end_estwn.append(end)
                except: pass
            
        else:
            end_estwn.append(end)
            try:
                start_estwn.append( sset[0].attrib['target'] )
                rel_type.append( sset[0].attrib['relType'] )            
            except:
                start_estwn.append("null")
                rel_type.append("null")
                pass




def upload_entries(db_file):
    entryTable(db_file)
    conn = create_connection(db_file)
    cursor = conn.cursor()
    with conn:
        for i in range(len(sset_list)):
            #ssetId = fetch_ssetId(estwnId_list[i])
            cursor.execute("INSERT INTO xml_lexical_entry(estwn_id,synset, written_form, pos, sense) VALUES(?,?,?,?,?)"                                                        ,(estwnId_list[i],sset_list[i], lemma_list[i], pos_list[i], sense_list[i]))
        conn.commit()




def upload_synsets(synset_db):

    synsetTable(synset_db)
    conn = create_connection(synset_db)
    cursor = conn.cursor()
    with conn:
        for i in range(len(estwnId_list)):
            cursor.execute("INSERT INTO xml_synset(id, estwn_id, source_sense) VALUES (?,?,?)"                                                ,(i,estwnId_list[i],sset_word[i]))


def upload_relations(db_file):
    
    rel_table(db_file)
    conn = create_connection(db_file)
    cursor = conn.cursor()
    with conn:
        for i in range(len(end_estwn)):    
            cursor.execute("INSERT INTO xml_relation(start_estwn, end_estwn, relation) VALUES(?,?,?)"                                                            ,(start_estwn[i], end_estwn[i],rel_type[i]))
        conn.commit()

estwnId_list=[]
pos_list = []
lemma_list = []
sset_list=[]
sense_list=[]
#uploads xml_entry.db
fetch_entry()
upload_entries(xml_entry_db)

estwnId_list = []
sset_word = []
#uploads xml_synset.db
fetch_synset(xml_entry_db)
upload_synsets(xml_sset_db)

start_estwn = []
end_estwn   = []
rel_type    = []
#uploads xml_lexical_entry.db
fetch_relation()
upload_relations(xml_rel_db)

#yet unnecesary functions.
'''
def fetch_lemma(estwn_id):
    '''
    
    '''
    xml_conn = create_connection(xml_db)
    cursor = xml_conn.cursor()
    with xml_conn:
        #select all synsets with different indices from table.
        cursor.execute("SELECT DISTINCT written_form FROM xml_lexical_entry WHERE estwn_id = ?", (estwn_id,))
        row = cursor.fetchone()
        #print(row[0])
        if row is not None:
            return row[0]




def fetch_ssetId(estwn_id):
    
    lemma = fetch_lemma(estwn_id)
    
    db_conn = create_connection(sset_db)
    cursor = db_conn.cursor()
    with db_conn:
        cursor.execute("SELECT DISTINCT synset_id FROM synset_table WHERE synset_word = ?", (lemma,))
        row = cursor.fetchone()
        if row is not None:
            #print(row[0])
            return row[0]




def fetch_estwnId(estwnId):
    
    db_conn = create_connection(sset_db)
    cursor = db_conn.cursor()
    with db_conn:
        cursor.execute("SELECT DISTINCT id FROM xml_synsets WHERE estwn_id = ?", (estwnId,))
        row = cursor.fetchone()
        if row is not None:
            #print(row[0])
            return row[0]
        else: return 'null'




ssetId =[]
def addId(entry_db, ssetId):
    
    #Adds id from xml_synsets to xml_lexical_entry db. (If does not exist.)
    
    
    conn = create_connection(entry_db)
    cursor = conn.cursor()
    
    with conn:
        #cursor.execute("ALTER TABLE xml_LexicalEntry ADD COLUMN id")
        cursor.execute("SELECT estwn_id FROM xml_lexical_entry")
        for get in cursor.fetchall():
            data = get[0]
            estwnIdList.append(data)
            ssetId.append(fetch_estwnId(data))   
        i=0
        for data in ssetId:
            #print(data)
            cursor.execute("UPDATE xml_lexical_entry SET id = ? WHERE estwn_id = ?", (data,estwnIdList[i]))
            i+=1
        conn.commit()
'''