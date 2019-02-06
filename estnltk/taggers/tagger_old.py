from abc import ABC, abstractmethod, abstractproperty
from typing import List


class TaggerOld(ABC):
    """
    Abstract base class for taggers.
    """

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def layer_name(self) -> str:
        pass

    @property
    @abstractmethod
    def attributes(self) -> List:
        pass

    @property
    @abstractmethod
    def depends_on(self) -> List:
        pass

    @property
    @abstractmethod
    def configuration(self) -> dict:
        pass

    @abstractmethod
    def tag(self, text: 'Text', return_layer: bool=False, status: dict={}):
        """
        return_layer: bool, default False
            If True, tagger returns a layer. 
            If False, tagger annotates the text object with the layer and
            returns None.
        status: dict, default {}
            This can be used to store metadata on layer creation.
        """
        pass

    def parameters(self):
        record = {'name': self.__class__.__name__,
                  'layer': self.layer_name,
                  'attributes': self.attributes,
                  'depends_on': self.depends_on,
                  'configuration': [p + '=' + str(self.configuration[p]) for p in sorted(self.configuration)]
                  }
        return record

    def _repr_html_(self):
        import pandas
        pandas.set_option('display.max_colwidth', -1)
        table = pandas.DataFrame.from_records([self.parameters()], columns=['name', 'layer', 'attributes', 'depends_on'])
        table = table.to_html(index=False)
        table = ('<h4>TaggerOld</h4>', self.description, table)

        if self.configuration:
            # Get configuration items in fixed order
            conf = [(k,str(v)) for k,v in sorted(self.configuration.items(), \
                                                      key=lambda x : x[0])]
            row_names = [item[0] for item in conf]
            conf_vals = [(item[1],) for item in conf]
            conf_table = pandas.DataFrame.from_records(conf_vals, index=row_names)
            conf_table = conf_table.to_html(header=False)
            conf_table = ('<h4>Configuration</h4>', conf_table)
        else:
            conf_table = ('No configuration parameters.',)

        return '\n'.join(table + conf_table)

    def __repr__(self):
        conf_str = ""
        if self.configuration:
            conf = [str(k)+'='+str(v) for k,v in sorted(self.configuration.items(), \
                                                        key=lambda x : x[0])]
            conf_str = ', '.join(conf)
        return self.__class__.__name__+"("+conf_str+")"