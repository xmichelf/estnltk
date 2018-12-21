


import sqlite3

entry_db ='xml_lexical_entry.db'
synset_db ='xml_synset.db'

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

conn_wn_entry = create_connection('../../data/estwn_kb74/wordnet_entry-1.db')
crsr_wn_entry = conn_wn_entry.cursor()

conn_wn_entry.execute("ATTACH DATABASE 'xml_synset.db' AS xml_synset ")
conn_wn_entry.execute("ATTACH DATABASE 'xml_lexical_entry.db' AS xml_lexical_entry")

with conn_wn_entry:
    crsr_wn_entry.execute('''CREATE TABLE wordnet_entry AS SELECT id, source_sense AS synset_name, xml_synset.estwn_id,pos,sense,written_form AS literal FROM xml_lexical_entry 
                                        JOIN xml_synset 
                                        ON xml_synset.estwn_id = xml_lexical_entry.estwn_id ''')

