import sqlite3
from wordnet import Wordnet


'''
tee wordnet.py fail milles on Wordnet klass, mille _init_ meetod teeb kaks SQLight andmebaasi ühendust

üks wordnet_relations jaoks ja teine wordnet_entries jaoks

sul on juba olemas kaks funktsiooni mida sellel klassil vaja läheb

lisaks on sul vaja defineerida kõik wn.py olevad meetodid, mis ei alga alakriipsuga

lisaks on sul vaja defineerida _del_ funktsioon, mis paneb SQLight ühendused kinni
'''

def _get_key_from_id(id, cursor):
    '''
    Returns synset word string "literal.pos.sense".
    '''
    
    cursor.execute('''SELECT literal, pos, sense FROM wordnet_entry WHERE id = '{}' LIMIT 1'''.format(id))
    data = cursor.fetchall()[0]
    literal = data[0]
    pos = data[1]
    sense = "%02d"%data[2]
    
    return '.'.join([literal,pos,sense])

class SynsetException(Exception):
    pass

class Synset:
    """Represents a WordNet synset.
    Attributes
    ----------
    wordnet: wordnet version
    name : str
      Synset  string identifier in the form `lemma.pos.sense_id`.
    id : int
      Synset integer identifier.
    pos : str
      Synset's part-of-speech.
    estwn_id: eurown.Synset
      Underlying Synset object. Not intended to access directly.
    """
    
    def __init__(self, wordnet, id):
       
        #invalid entry.
        if not isinstance(id, int):
            self.wordnet = None 
            self.id = None
            self.estwn_id = None
            self.pos = None
            self.sense = None
            self.literal = None
            self.name = None
            return

        self.wordnet = wordnet
        self.id = id
        self.wordnet.cur.execute("SELECT estwn_id, pos, sense, literal FROM wordnet_entry WHERE id = {} LIMIT 1".format(id))
        self.estwn_id, self.pos, self.sense, self.literal = self.wordnet.cur.fetchone()
        self.name = '{}.{}.{}'.format(self.literal, self.pos, self.sense)
        

    def __eq__(self,other):
        
        return self.wordnet == other.wordnet and self.id != None and self.id == other.id
    
    
    def get_related_synset(self, relation=None):
        '''Returns all relation names and start_vertex if relation not specified, else returns start_vertex of specified relation.
        Parameters
        ----------
        synset_id : int
        relation  : str
        '''     

        #TODO:if relation not '', '', ' ', '.',';".... # if is str and "_ # else return []"
        if relation.isalnum():
            if self.wordnet == None:
                return []

            if relation == None:
                self.wordnet.cur.execute('''SELECT end_vertex,relation FROM wordnet_relation WHERE start_vertex = '{}' '''.format(self.id))
                return [(Synset(self.wordnet, row[0]), row[1]) for row in self.wordnet.cur.fetchall()]
            else:
                self.wordnet.cur.execute('''SELECT end_vertex FROM wordnet_relation WHERE start_vertex = '{}' AND relation = '{}' '''.format(self.id, relation))
                return [Synset(self.wordnet, row[0]) for row in self.wordnet.cur.fetchall()]
        else:
            return []

    
    def get_synset(self, synset_id):

        return Synset(self.wordnet, synset_id)        

    def closure(self, relation, depth=float('inf')):   
        
        """Finds all the ancestors of the synset using provided relation.
        Parameters
        ----------
          relation : str
        Name of the relation which is recursively used to fetch the ancestors.
        Returns
        -------
          list of Synsets
        Returns the ancestors of the synset via given relations.
        """

        path = [self]
        unvisited_relation = [(sset, 1) for sset in self.get_related_synset(relation)]

        while len(unvisited_relation) > 1:
            relation_depth = unvisited_relation.pop()
            if relation_depth[1] > depth:
                continue
            parents = relation_depth[0].get_related_synset(relation)

            if not parents:
                yield relation_depth[0]
            else:
                unvisited_relation.extend( [(parent, relation_depth[1]+1) for parent in parents] )
    
    def hypernyms(self):
        """Retrieves all the hypernyms.
        
        Returns
        -------
          list of Synsets
        Synsets which are linked via hypernymy relation.
        
        """

        return self.get_related_synset("hypernym")

    def hyponyms(self):
        """Retrieves all the hyponyms.
        
        Returns
        -------
          list of Synsets
        Synsets which are linked via hyponymy relation.
        
        """
        
        return self.get_related_synset("hyponym")
    
    def holonyms(self):
        """Retrieves all the holonyms.
        
        Returns
        -------
          list of Synsets
        Synsets which are linked via holonymy relation.
        
        """
        return self.get_related_synset("holonym")

    def meronyms(self):
        """Retrieves all the meronyms.
        
        Returns
        -------
          list of Synsets
        Synsets which are linked via meronymy relation.
        
        """
        return self.get_related_synset("meronym")

    def member_holonyms(self):
        """Retrieves all the member holoynms.
        
        Returns
        -------
          list of Synsets
        Synsets which are "wholes" of what the synset represents.
        
        """
        return self.get_related_synset("holo_member")

    def root_hypernyms(self):

        """Retrieves all the root hypernyms.
        
        Returns
        -------
          list of Synsets
        Roots via hypernymy relation.
        
        """

        path = [self]
        while path:
            current_node = path.pop()
            parents = current_node.hypernyms()
            
            if not parents:
                yield current_node
            else:
                path.extend(parents)
    
    def get_variants(self):
        """Returns variants/lemmas of the synset.
        
        Returns
        -------
          list of eurown.Variants
        Lemmas/variants of the synset.
        
        """
        print("Not implemented.")
      
    def definition(self):
        """Returns the definition of the synset.
        
        Returns
        -------
          str
        Definition of the synset as a new-line separated concatenated string from all its variants' definitions.
        
        """
        return print("not implemented")#'\n'.join([variant.gloss for variant in self.estwn_id.variants if variant.gloss])
      

      #TODO compare 1.4 wn lemma return value with entry.db values.
    def lemmas(self):
        """Returns the synset's lemmas/variants' literal represantions.
        
        Returns
        -------
          list of Lemmas
        List of its variations' literals as Lemma objects.
        
        """
        self.wordnet.cur.execute('''SELECT literal FROM wordnet_entry WHERE id = {} ''' .format(self.id))
        return [row[0] for row in self.wordnet.cur.fetchall()]
