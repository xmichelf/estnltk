

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
        self.wordnet.cur.execute("SELECT estwn_id, pos, sense, synset_name, literal FROM wordnet_entry WHERE id = ? LIMIT 1",(id,))
        self.estwn_id, self.pos, self.sense, name, self.literal = self.wordnet.cur.fetchone()
        self.name = '{}.{}.{}'.format(name, self.pos, self.sense)
                

    def __eq__(self, other):
        
        return self.wordnet == other.wordnet and self.id != None and self.id == other.id
    
    
    def get_related_synset(self, relation=None):
        '''Returns all relation names and start_vertex if relation not specified, else returns start_vertex of specified relation.
        Parameters
        ----------
        synset_id : int
        relation  : str
        '''     
        if self.wordnet == None:
            return []
        if relation == None:
            self.wordnet.cur.execute('''SELECT start_vertex,relation FROM wordnet_relation WHERE end_vertex = '{}' '''.format(self.id))
            return [(Synset(self.wordnet, row[0]), row[1]) for row in self.wordnet.cur.fetchall()]
        elif relation:
            try:
                relation.isalnum()
            except Exception as e:
                raise SynsetException("Could not query database with: \n\t: {}.".format(e))

            self.wordnet.cur.execute('''SELECT start_vertex FROM wordnet_relation WHERE end_vertex = '{}' AND relation = '{}' '''.format(self.id, relation))
            return [Synset(self.wordnet, row[0]) for row in self.wordnet.cur.fetchall()]
        else:
            return []

    '''
    def get_synset(self, synset_id=None):

        if synset_id is None:
            return Synset(self.wordnet, self.id)
        else:
            return Synset(self.wordnet, synset_id)    
    '''


    def closure(self, relation, depth_threshold=float('inf'), return_depths=False):   
        
        """Finds all the ancestors of the synset using provided relation.

        Parameters
        ----------
        relation : str
            Name of the relation which is recursively used to fetch the ancestors.
            
        depth_treshold : int
            Amount of recursive relations to yield. If left unchanged, then yields all recursive relations.

        return_depths : bool
            'return_depths = True' yields synset and amount of recursions.
            'return_depths = False' yields only synset.
            Default value 'False'.

        Returns
        -------
        Synset recursions of given relation via generator.

        """
        if depth_threshold < 1:
            return 

        node_stack = self.get_related_synset(relation)
        depth_stack = [1]*len(node_stack)

        while len(node_stack):
            node = node_stack.pop()
            depth = depth_stack.pop()
            if depth > depth_threshold:
                continue
            parents = node.get_related_synset(relation)

            if not parents or depth == depth_threshold:
                if return_depths is not False:
                    yield (node, depth)
                else:
                    yield node
            else:
                node_stack.extend(parents)
                depth_stack.extend([depth+1] * len(parents))


    def root_hypernyms(self, depth_threshold=float('inf'), return_depths=False):

        """Retrieves all the root hypernyms.
        
        Returns
        -------
          list of Synsets
        Roots via hypernymy relation.
        
        """
        if depth_threshold < 1:
            return 

        node_stack = self.hypernyms()
        depth_stack = [1]*len(node_stack)

        while len(node_stack):
            node = node_stack.pop()
            depth = depth_stack.pop()
            if depth > depth_threshold:
                continue
            parents = node.hypernyms()
                    
            if not parents or depth == depth_threshold:
                if return_depths is not False:
                    yield (node, depth)
                else:
                    yield node        
            else:
                node_stack.extend(parents)
                depth_stack.extend([depth+1] * len(parents))


    
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
      

    def lemmas(self):
        """Returns the synset's lemmas/variants' literal represantions.
        
        Returns
        -------
          list of Lemmas
        List of its variations' literals as Lemma objects.
        
        """
        self.wordnet.cur.execute('''SELECT literal FROM wordnet_entry WHERE id = {} ''' .format(self.id))
        return [row[0] for row in self.wordnet.cur.fetchall()]
