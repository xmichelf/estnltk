

'''
This script is intended for combinig values from xml_synset and xml_relation tables into
complete relations table 'relation_complete.db'
'''

import sqlite3
from lxml import etree

xml_sset_db = 'xml_synset.db'
xml_relation_db = 'xml_relation.db'
xml_rel_db = 'relation_complete.db'

join_str = '''CREATE TABLE synset_relations AS
            SELECT
                start_index.id AS start_vertex,
                start_index.source_sense AS start_synset, xml_relation.start_estwn,
                end_index.id AS end_vertex,
                end_index.source_sense AS end_synset, xml_relation.end_estwn,
                xml_relation.relation AS relation 
            FROM xml_relation
            LEFT JOIN
            (
                SELECT DISTINCT id, estwn_id, source_sense FROM xml_synset
            ) AS start_index
            ON xml_relation.start_estwn = start_index.estwn_id
            LEFT JOIN
            (
                SELECT DISTINCT id, estwn_id, source_sense FROM xml_synset
            ) AS end_index
            ON xml_relation.end_estwn = end_index.estwn_id
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

def sql_table(databaseLoc):

    sql_create_synset_table = ''' CREATE TABLE IF NOT EXISTS synset_rel(

                                        start_id TEXT NOT NULL,
                                        start_estwn TEXT NOT NULL,
                                        end_estwn TEXT NOT NULL,
                                        end_id TEXT NOT NULL,
                                        relation TEXT NOT NULL
                                                    ); '''
    conn = create_connection(databaseLoc)
    if conn is not None:
        create_table(conn,sql_create_synset_table)
    else:
        print("Error! cannot create db conn.")

conn_rel = create_connection(xml_rel_db)
crsr_rel   = conn_rel.cursor()
    
crsr_rel.execute("ATTACH DATABASE 'xml_synset.db' AS xml_synset")
crsr_rel.execute("ATTACH DATABASE 'xml_relation.db' AS xml_relation")

with conn_rel:
    crsr_rel.execute(join_str)
