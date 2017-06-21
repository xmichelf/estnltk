import regex as re
from pandas import DataFrame, read_csv

from estnltk.text import Layer
from estnltk.layer_operations import resolve_conflicts


class RegexTagger:
    """
    Searches matches for regular expressions in the text, solves the possible
    conflicts and creates a new layer of the matches.
    """
    def __init__(self,
                 vocabulary,
                 attributes=[],
                 conflict_resolving_strategy='MAX',
                 overlapped=False,
                 return_layer=False,
                 layer_name='regexes',
                 ):
        """Initialize a new RegexTagger instance.

        Parameters
        ----------
        vocabulary: list of dicts or pandas.DataFrame or csv file name
            regexes and attributes to annotate
        conflict_resolving_strategy: 'ALL', 'MAX', 'MIN' (default: 'MAX')
            Strategy to choose between overlapping events.
        overlapped: bool (Default: False)
            If True, the match of a regular expression may overlap with a match
            of the same regular expression.
        return_layer: bool
            If True, RegexTagger.tag(text) returns a layer. 
            If False, RegexTagger.tag(text) annotates the text object with the
            layer and returns None.
        layer_name: str (Default: 'regexes')
            The name of the new layer.
        """
        self._illegal_keywords = {'start', 'end'}

        # attributes in output layer
        self._attributes = set(attributes)
        # attributes needed by tagger 
        self._internal_attributes = self._attributes|{'_group_', '_priority_'}
        
        self._vocabulary = self._read_expression_vocabulary(vocabulary)
        self._overlapped = overlapped
        self._return_layer = return_layer
        if conflict_resolving_strategy not in ['ALL', 'MIN', 'MAX']:
            raise ValueError("Unknown conflict_resolving_strategy '%s'." % conflict_resolving_strategy)
        self._conflict_resolving_strategy = conflict_resolving_strategy
        self._layer_name = layer_name


    def _read_expression_vocabulary(self, expression_vocabulary):
        if isinstance(expression_vocabulary, list):
            vocabulary = expression_vocabulary
        elif isinstance(expression_vocabulary, DataFrame):
            vocabulary = expression_vocabulary.to_dict('records')
        elif isinstance(expression_vocabulary, str):
            vocabulary = read_csv(expression_vocabulary, na_filter=False, index_col=False).to_dict('records')
        else:
            raise TypeError(str(type(expression_vocabulary)) + " not supported as expression vocabulary")
        records = []
        for record in vocabulary:
            if set(record) & self._illegal_keywords:
                raise KeyError('Illegal keys in expression vocabulary: ' + str(set(record)&self._illegal_keywords))
            if self._internal_attributes-set(record):
                raise KeyError('Missing keys in expression vocabulary: ' + str(self._internal_attributes-set(record)))
            
            _regex_pattern_ = record['_regex_pattern_']
            if isinstance(_regex_pattern_, str):
                _regex_pattern_ = re.compile(_regex_pattern_)

            rec = {'_regex_pattern_': _regex_pattern_,
                   '_group_': record.get('_group_', 0),
                   '_priority_': record.get('_priority_', 0)
                   }
            for key in self._attributes:
                if key not in record:
                    raise KeyError('Missing key in expression vocabulary: ' + key)
                value = record[key]
                if isinstance(value, str) and value.startswith('lambda m:'):
                    value = eval(value)
                rec[key] = value
            records.append(rec)

        return records


    def tag(self, text, status={}):
        """Retrieves list of regex_matches in text.
        Parameters
        ----------
        text: Text
            The estnltk text object to search for matches.
        Returns
        -------
        Layer, if return_layer is True,
        None, otherwise.
        """
        layer = Layer(name=self._layer_name,
                      attributes=self._attributes,
                      )
        records = self._match(text.text)
        layer = layer.from_records(records)
        layer = resolve_conflicts(layer, self._conflict_resolving_strategy, status)
        if self._return_layer:
            return layer
        else:
            text[self._layer_name] = layer

    def _match(self, text):
        matches = []
        for voc in self._vocabulary:
            for matchobj in voc['_regex_pattern_'].finditer(text, overlapped=self._overlapped):
                record = {
                    'start': matchobj.span(voc['_group_'])[0],
                    'end': matchobj.span(voc['_group_'])[1],
                }
                for a in self._internal_attributes:
                    v = voc[a]
                    if callable(v):
                        v = v(matchobj)
                    record[a] = v
                matches.append(record)
        return matches