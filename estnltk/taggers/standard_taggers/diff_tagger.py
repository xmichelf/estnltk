from estnltk import EnvelopingSpan
from estnltk import Layer
from estnltk.layer_operations import diff_layer
from estnltk.taggers import Tagger
from estnltk.layer.span_operations import symm_diff_ambiguous_spans


class DiffTagger(Tagger):
    """ Finds differences of input layers.
    """
    conf_param = ['input_layer_name_attribute']

    def __init__(self,
                 layer_a: str,
                 layer_b: str,
                 output_layer: str,
                 output_attributes,
                 input_layer_name_attribute
                 ):
        assert input_layer_name_attribute in output_attributes
        self.input_layers = (layer_a, layer_b)
        self.output_layer = output_layer
        self.output_attributes = output_attributes
        self.input_layer_name_attribute = input_layer_name_attribute

    def _make_layer(self, raw_text, layers, status):
        name_a = self.input_layers[0]
        name_b = self.input_layers[1]
        layer_a = layers[self.input_layers[0]]
        layer_b = layers[self.input_layers[1]]
        assert layer_a.attributes == layer_b.attributes
        assert layer_a.parent == layer_b.parent
        assert layer_a.enveloping == layer_b.enveloping
        assert layer_a.ambiguous == layer_b.ambiguous

        layer = Layer(
            name=self.output_layer,
            attributes=self.output_attributes,
            parent=layer_a.parent,
            enveloping=layer_a.enveloping,
            ambiguous=True
            )
        missing_spans = 0
        extra_spans = 0
        missing_annotations = 0
        extra_annotations = 0
        copy_attributes = [attr for attr in self.output_attributes if attr != self.input_layer_name_attribute]
        if layer_a.ambiguous:
            if layer_a.enveloping:
                for a_spans, b_spans in diff_layer(layer_a, layer_b):
                    if a_spans is None:
                        extra_spans += 1
                        extra_annotations += len(b_spans)
                    if b_spans is None:
                        missing_spans += 1
                        missing_annotations += len(a_spans)
                    if a_spans is not None and b_spans is not None:
                        a_spans, b_spans = symm_diff_ambiguous_spans(a_spans, b_spans)
                        missing_annotations += len(a_spans)
                        extra_annotations += len(b_spans)
                    if a_spans is not None:
                        for a in a_spans:
                            attributes = {attr: getattr(a, attr) for attr in copy_attributes}
                            attributes[self.input_layer_name_attribute] = name_a
                            es = EnvelopingSpan(spans=a.spans, layer=layer, attributes=attributes)
                            layer.add_span(es)
                    if b_spans is not None:
                        for b in b_spans:
                            attributes = {attr: getattr(b, attr) for attr in copy_attributes}
                            attributes[self.input_layer_name_attribute] = name_b
                            es = EnvelopingSpan(spans=b.spans, layer=layer, attributes=attributes)
                            layer.add_span(es)
            elif layer.parent:
                # TODO:
                raise NotImplementedError()
            else:
                # TODO:
                raise NotImplementedError()
        else:
            if layer_a.enveloping:
                for a, b in diff_layer(layer_a, layer_b):
                    if a is not None:
                        attributes = {attr: getattr(a, attr) for attr in copy_attributes}
                        attributes[self.input_layer_name_attribute] = name_a
                        es = EnvelopingSpan(spans=a.spans, layer=layer, attributes=attributes)
                        layer.add_span(es)
                    if b is not None:
                        attributes = {attr: getattr(b, attr) for attr in copy_attributes}
                        attributes[self.input_layer_name_attribute] = name_b
                        es = EnvelopingSpan(spans=b.spans, layer=layer, attributes=attributes)
                        layer.add_span(es)
            elif layer.parent:
                # TODO:
                raise NotImplementedError()
            else:
                # TODO:
                raise NotImplementedError()

        if status is not None:
            status['different spans'] = len(layer)
            status['missing_annotations'] = missing_annotations
            status['missing_spans'] = missing_spans
            status['extra_annotations'] = extra_annotations
            status['extra_spans'] = extra_spans

        return layer
