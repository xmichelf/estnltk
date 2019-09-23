from collections import OrderedDict
from estnltk.core import abs_path
from estnltk.converters import text_to_dict
from estnltk.converters.conll_importer import conll_to_text
from estnltk.converters.conll_importer import add_layer_from_conll

from estnltk.taggers.text_segmentation.word_tagger import MAKE_AMBIGUOUS as _MAKE_WORDS_AMBIGUOUS

text_dict = {
    'text': 'Iga üheksas kroon tuli salapärastelt isikutelt . '
            'See oli rohkem kui 10 protsenti kogu Hansapanka paigutatud rahast .',
    'meta': {},
    'layers': [{'name': 'syntax',
                'attributes': ('id',
                               'lemma',
                               'upostag',
                               'xpostag',
                               'feats',
                               'head',
                               'deprel',
                               'deps',
                               'misc',
                               'parent_span',
                               'children'),
                'parent': None,
                'enveloping': None,
                'ambiguous': False,
                'serialisation_module': 'syntax_v0',
                'meta': {},
                'spans': [{'base_span': (0, 3),
                           'annotations': [{'id': 1,
                                            'lemma': 'iga',
                                            'upostag': 'P',
                                            'xpostag': 'P',
                                            'feats': OrderedDict([('det', ''), ('sg', ''), ('nom', '')]),
                                            'head': 2,
                                            'deprel': '@NN>',
                                            'deps': None,
                                            'misc': None}]},
                          {'base_span': (4, 11),
                           'annotations': [{'id': 2,
                                            'lemma': 'üheksas',
                                            'upostag': 'N',
                                            'xpostag': 'A',
                                            'feats': OrderedDict([('ord', ''), ('sg', ''), ('nom', ''), ('l', '')]),
                                            'head': 3,
                                            'deprel': '@AN>',
                                            'deps': None,
                                            'misc': None}]},
                          {'base_span': (12, 17),
                           'annotations': [{'id': 3,
                                            'lemma': 'kroon',
                                            'upostag': 'S',
                                            'xpostag': 'S',
                                            'feats': OrderedDict([('sg', ''), ('nom', '')]),
                                            'head': 4,
                                            'deprel': '@SUBJ',
                                            'deps': None,
                                            'misc': None}]},
                          {'base_span': (18, 22),
                           'annotations': [{'id': 4,
                                            'lemma': 'tule',
                                            'upostag': 'V',
                                            'xpostag': 'V',
                                            'feats': OrderedDict([('indic', ''),
                                                                  ('impf', ''),
                                                                  ('ps3', ''),
                                                                  ('sg', '')]),
                                            'head': 0,
                                            'deprel': 'ROOT',
                                            'deps': None,
                                            'misc': None}]},
                          {'base_span': (23, 36),
                           'annotations': [{'id': 5,
                                            'lemma': 'sala_pärane',
                                            'upostag': 'A',
                                            'xpostag': 'A',
                                            'feats': OrderedDict([('pl', ''), ('abl', '')]),
                                            'head': 6,
                                            'deprel': '@AN>',
                                            'deps': None,
                                            'misc': None}]},
                          {'base_span': (37, 46),
                           'annotations': [{'id': 6,
                                            'lemma': 'isik',
                                            'upostag': 'S',
                                            'xpostag': 'S',
                                            'feats': OrderedDict([('pl', ''), ('abl', '')]),
                                            'head': 4,
                                            'deprel': '@ADVL',
                                            'deps': None,
                                            'misc': None}]},
                          {'base_span': (47, 48),
                           'annotations': [{'id': 7,
                                            'lemma': '.',
                                            'upostag': 'Z',
                                            'xpostag': 'Z',
                                            'feats': OrderedDict([('Fst', '')]),
                                            'head': 6,
                                            'deprel': '@Punc',
                                            'deps': None,
                                            'misc': None}]},
                          {'base_span': (49, 52),
                           'annotations': [{'id': 1,
                                            'lemma': 'see',
                                            'upostag': 'P',
                                            'xpostag': 'P',
                                            'feats': OrderedDict([('dem', ''), ('sg', ''), ('nom', '')]),
                                            'head': 2,
                                            'deprel': '@SUBJ',
                                            'deps': None,
                                            'misc': None}]},
                          {'base_span': (53, 56),
                           'annotations': [{'id': 2,
                                            'lemma': 'ole',
                                            'upostag': 'V',
                                            'xpostag': 'V',
                                            'feats': OrderedDict([('indic', ''),
                                                                  ('impf', ''),
                                                                  ('ps3', ''),
                                                                  ('sg', '')]),
                                            'head': 0,
                                            'deprel': 'ROOT',
                                            'deps': None,
                                            'misc': None}]},
                          {'base_span': (57, 63),
                           'annotations': [{'id': 3,
                                            'lemma': 'rohkem',
                                            'upostag': 'D',
                                            'xpostag': 'D',
                                            'feats': None,
                                            'head': 2,
                                            'deprel': '@OBJ',
                                            'deps': None,
                                            'misc': None}]},
                          {'base_span': (64, 67),
                           'annotations': [{'id': 4,
                                            'lemma': 'kui',
                                            'upostag': 'J',
                                            'xpostag': 'Jc',
                                            'feats': None,
                                            'head': 5,
                                            'deprel': '@J',
                                            'deps': None,
                                            'misc': None}]},
                          {'base_span': (68, 70),
                           'annotations': [{'id': 5,
                                            'lemma': '10',
                                            'upostag': 'N',
                                            'xpostag': 'N',
                                            'feats': OrderedDict([('card', ''), ('sg', ''), ('nom', '')]),
                                            'head': 3,
                                            'deprel': '@ADVL',
                                            'deps': None,
                                            'misc': None}]},
                          {'base_span': (71, 80),
                           'annotations': [{'id': 6,
                                            'lemma': 'protsent',
                                            'upostag': 'S',
                                            'xpostag': 'S',
                                            'feats': OrderedDict([('sg', ''), ('part', '')]),
                                            'head': 5,
                                            'deprel': '@<Q',
                                            'deps': None,
                                            'misc': None}]},
                          {'base_span': (81, 85),
                           'annotations': [{'id': 7,
                                            'lemma': 'kogu',
                                            'upostag': 'A',
                                            'xpostag': 'A',
                                            'feats': None,
                                            'head': 10,
                                            'deprel': '@AN>',
                                            'deps': None,
                                            'misc': None}]},
                          {'base_span': (86, 96),
                           'annotations': [{'id': 8,
                                            'lemma': 'Hansa_pank',
                                            'upostag': 'S',
                                            'xpostag': 'H',
                                            'feats': OrderedDict([('sg', ''), ('adit', '')]),
                                            'head': 9,
                                            'deprel': '@ADVL',
                                            'deps': None,
                                            'misc': None}]},
                          {'base_span': (97, 107),
                           'annotations': [{'id': 9,
                                            'lemma': 'paiguta=tud',
                                            'upostag': 'A',
                                            'xpostag': 'A',
                                            'feats': OrderedDict([('partic', '')]),
                                            'head': 10,
                                            'deprel': '@AN>',
                                            'deps': None,
                                            'misc': None}]},
                          {'base_span': (108, 114),
                           'annotations': [{'id': 10,
                                            'lemma': 'raha',
                                            'upostag': 'S',
                                            'xpostag': 'S',
                                            'feats': OrderedDict([('sg', ''), ('el', '')]),
                                            'head': 5,
                                            'deprel': '@ADVL',
                                            'deps': None,
                                            'misc': None}]},
                          {'base_span': (115, 116),
                           'annotations': [{'id': 11,
                                            'lemma': '.',
                                            'upostag': 'Z',
                                            'xpostag': 'Z',
                                            'feats': OrderedDict([('Fst', '')]),
                                            'head': 10,
                                            'deprel': '@Punc',
                                            'deps': None,
                                            'misc': None}]}]},
               {'name': 'words',
                'attributes': (),
                'parent': None,
                'enveloping': None,
                'ambiguous': _MAKE_WORDS_AMBIGUOUS,
                'serialisation_module': None,
                'meta': {},
                'spans': [{'base_span': (0, 3), 'annotations': [{}]},
                          {'base_span': (4, 11), 'annotations': [{}]},
                          {'base_span': (12, 17), 'annotations': [{}]},
                          {'base_span': (18, 22), 'annotations': [{}]},
                          {'base_span': (23, 36), 'annotations': [{}]},
                          {'base_span': (37, 46), 'annotations': [{}]},
                          {'base_span': (47, 48), 'annotations': [{}]},
                          {'base_span': (49, 52), 'annotations': [{}]},
                          {'base_span': (53, 56), 'annotations': [{}]},
                          {'base_span': (57, 63), 'annotations': [{}]},
                          {'base_span': (64, 67), 'annotations': [{}]},
                          {'base_span': (68, 70), 'annotations': [{}]},
                          {'base_span': (71, 80), 'annotations': [{}]},
                          {'base_span': (81, 85), 'annotations': [{}]},
                          {'base_span': (86, 96), 'annotations': [{}]},
                          {'base_span': (97, 107), 'annotations': [{}]},
                          {'base_span': (108, 114), 'annotations': [{}]},
                          {'base_span': (115, 116), 'annotations': [{}]}]},
               {'name': 'sentences',
                'attributes': (),
                'parent': None,
                'enveloping': 'words',
                'ambiguous': False,
                'serialisation_module': None,
                'meta': {},
                'spans': [{'base_span': ((0, 3),
                                         (4, 11),
                                         (12, 17),
                                         (18, 22),
                                         (23, 36),
                                         (37, 46),
                                         (47, 48)),
                           'annotations': [{}]},
                          {'base_span': ((49, 52),
                                         (53, 56),
                                         (57, 63),
                                         (64, 67),
                                         (68, 70),
                                         (71, 80),
                                         (81, 85),
                                         (86, 96),
                                         (97, 107),
                                         (108, 114),
                                         (115, 116)),
                           'annotations': [{}]}]}]}


def test_conll_importers():
    file = abs_path('tests/test_converters/test_conll.conll')
    text = conll_to_text(file, syntax_layer='syntax')

    assert text_to_dict(text) == text_dict

    del text.syntax
    assert 'syntax' not in text.layers

    add_layer_from_conll(file, text, 'syntax')

    assert text_to_dict(text) == text_dict
