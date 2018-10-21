
# coding: utf-8

# In[1]:


from estnltk.wordnet import wn
import sqlite3
import igraph as ig
import plotly.plotly as py
from plotly.graph_objs import *


# In[2]:


sset_db = 'wordnet/data/all_synsets.db'
relation_db = 'wordnet/data/all_relations_strings.db'


# In[3]:


g = ig.Graph()
g.es["relation"] = []
g.vs["synset"] =[]


# In[4]:


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


# In[5]:


def get_ssets(db_file):

    sqlTables(db_file)
    conn = create_connection(db_file)
    cursor = conn.cursor()
    with conn:
        cursor.execute("SELECT DISTINCT synset_word FROM synset_table")
        for row in cursor.fetchall():
            sset_word.append(row[0])


# In[6]:




def get_relations(db_file):
    
    sqlTables(db_file)
    conn = create_connection(db_file)
    cursor = conn.cursor()
    
    with conn:
        cursor.execute("SELECT start_vertex FROM graph_table")
        for row in cursor.fetchall():
            start_vrtx.append(row[0])
        cursor.execute("SELECT end_vertex FROM graph_table")
        for row in cursor.fetchall():
            end_vrtx.append(row[0])
        cursor.execute("SELECT relation FROM graph_table")
        for row in cursor.fetchall():
            relation.append(row[0])


# In[65]:


def add_edges(start_vertex, end_vertex, N):
    '''
    Edges are added between start_vertex[i] and end_vertex
    If end vertex ID changes, it means that there are no more start IDs corresponding to end ID, so
    we take N-1 as end ID and continiue adding start_vertex[i] to end_vertex[N-1], etc.
    '''
    sset_list = [None]*N
    rel_list = [None]*N
    #max_vrt = max(max(start_vertex[N]), max(end_vertex[N]))
    g.add_vertices(N)
    end = int((N/2)-1) # edges indexed from 0
    j=1
    print(end)
    for i in range(N):
        g.add_edge(i, end)        
        sset_list[i] = sset_word[ start_vertex[i] ]
        sset_list[N-(i+1)] = sset_word[ end_vertex[i] ]
        #rel_list[i] = relation[i]
        if end_vertex[i] != end_vertex[i+1]:
            end = N-j
            j+=1            
    g.es["relation"] = relation[:N]#rel_list
    g.vs["synset"] = sset_list
    


# In[9]:


start_vrtx = []
end_vrtx   = []
relation   = []

get_relations(relation_db)


# In[10]:


sset_word = []
get_ssets(sset_db)


# In[35]:


start_vrtx[:10]


# In[66]:


g = ig.Graph()
g.vs["synset"]=[]
g.es["relation"]=[]
amount = 100
add_edges(start_vrtx, end_vrtx, amount)


# In[64]:



layout = g.layout("kk")
visual_style = {}
visual_style["vertex_label"] = g.vs["synset"]
visual_style["edge_label"] = g.es["relation"]
visual_style["vertex_size"] = 5
visual_style["layout"] = layout
visual_style["bbox"] = (1024,1000)
visual_style["margin"] = 10
ig.plot(g, **visual_style)

#ig.plot(g, layout = layout, bbox = (800, 800), margin = 5)
