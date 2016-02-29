.. _layer_operations_tutorial:

=======================================================
Tutorial for processing and creating text object layers
=======================================================

In Estnltk there are layer operations to modify, compare, filter, add and delete layers in the Text object and the
functions that do this are introduced in this tutorial.

All of the functions used on the layers can be used given that a Text object is already created. All of the functions
can be used for working with one Text object. Notice that the layer functions are designed in way that the original
Text object will not be changed automatically.

Keeping layers
==============
To keep the desired layers in a text object, as in the example below::

    from ...text import Text

    from estnltk.layers.operations import keep_layer

    text = Text('Mees, keda seal kohtasime Tartus, oli tuttav ja ta teretas meid.')

    text.tag_all().named_entities

    new_text = keep_layer(text, ['sentences', 'named_entities'])

    pprint(new_text)

The result is:
::

    {'named_entities': [{'end': 32, 'label': 'LOC', 'start': 26}],
     'sentences': [{'end': 64, 'start': 0}],
     'text': 'Mees, keda seal kohtasime Tartus, oli tuttav ja ta teretas meid.'}

The ``keep_layer()`` function is being executed on the Text object and takes a Text object and a list as an input. The
input list represents the layers that will be kept and all the layers that are not in the list will be deleted from the
Text object, with the exception of the ``text`` layer, which will be kept. The function returns the Text object with the
desired layers kept.

Deleting layers
===============
Another way to modify the Text object is to delete specific layers, as in the example below::

    from ...text import Text

    from estnltk.layers.operations import delete_layer

    text = Text('Mees, keda seal kohtasime Tartus, oli tuttav ja ta teretas meid.')

    text.tag_all()

    new_text = delete_layer(text, ['words', 'verb_chains', 'clauses'])

    pprint(new_text)

The result is:
::

    {'dct': '2015-12-11T20:34',
     'named_entities': [{'end': 32, 'label': 'LOC', 'start': 26}],
     'paragraphs': [{'end': 64, 'start': 0}],
     'sentences': [{'end': 64, 'start': 0}],
     'text': 'Mees, keda seal kohtasime Tartus, oli tuttav ja ta teretas meid.',
     'timexes': []}

The ``delete_layer()`` function is being executed on the Text object and takes a Text object and list as an input,
same as the ``keep_layer()`` function. The difference is that the function deletes all the layers in the input list,
with again the exception of the ``text`` layer, which will be kept. The function returns the Text object with the
desired layers deleted.

Creating layers with regex
==========================
To create a layer for one specific word or sentence (``String`` type) pattern you can use the ``new_layer_with_regex()``
function. An example is shown below::

    from ...text import Text

    from pprint import pprint

    from estnltk.layers.operations import new_layer_with_regex

    text = Text('Mees, keda seal kohtasime Tartus, oli tuttav ja ta teretas meid.')

    new_text = new_layer_with_regex(text, 'new_layer', ['ja', 'oli'])

The function ``new_layer_with_regex()`` takes the name of the new layer and the word or sentence pattern as input and
makes a new layer. The result of this function would be::

    pprint(new_text)

The result is:
::

    {'new_layer': [{'end': 47, 'start': 45, 'text': 'ja'},
                   {'end': 37, 'start': 34, 'text': 'oli'}],
     'text': 'Mees, keda seal kohtasime Tartus, oli tuttav ja ta teretas meid.'}

As you can see the function ``new_layer_with_regex()`` made a new layer for two estonian words 'ja' and 'oli'. If you
try to overwrite an already existing layer the function will stop and return the original Text object. If you need
the overwrite the layer you will need to use the ``delete_layer()`` function and after that make the layer again with
the ``new_layer_with_regex()`` function.

Using simple filter to create new layers
========================================
If you need to select a layer with specific restrictions ``apply_simple_filter()`` can be used, in the last there is a
``new_layer`` with two values. To find all the values that start with the number 34 you use the function as follows::

    from ...text import Text

    from pprint import pprint

    from estnltk.layers.operations import apply_simple_filter

    filtered = apply_simple_filter(new_text, layer='new_layer', restriction={'start': 34, 'text':'ja'})

    pprint(filtered)

The result is:
::

    [{'end': 47, 'start': 45, 'text': 'ja'},
     {'end': 37, 'start': 34, 'text': 'oli'}]


By default the function uses an 'OR' option. This means that at least one of the rules in the restriction has to be
met. When adding an 'AND' option, all the rules in the restriction have to be met. The result should be as follows::

    filtered = apply_simple_filter(new_text, layer='new_layer', restriction={'start': 45, 'text':'ja'}, option='AND')

    pprint(filtered)

The result is:
::

    [{'end': 47, 'start': 45, 'text': 'ja'}]

When you want to add a new layer to the old Text object you can still use the ``apply_simple_filter()`` function, as in
the example below::

    new_text['filtered'] = apply_simple_filter(new_text, layer='new_layer', restriction={'start': 34, 'text':'ja'})

    pprint(new_text)

The result is:
::

    {'filtered': [{'end': 47, 'start': 45, 'text': 'ja'},
                  {'end': 37, 'start': 34, 'text': 'oli'}],
     'new_layer': [{'end': 47, 'start': 45, 'text': 'ja'},
                   {'end': 37, 'start': 34, 'text': 'oli'}],
     'text': 'Mees, keda seal kohtasime Tartus, oli tuttav ja ta teretas meid.'}


Comparing layer intersections
=============================
To find overlappings among layer elements you can use the ``compute_layer_intersection()`` function. The function takes
the Text object, the layers and the selected method as input. You can choose between ``exact``, ``union`` or
``intersection`` method to compare the layers. In preparation you need to create the layers for comparison. For this
you can use ``new_layer_with_regex()``, ``apply_simple_filter()`` functions or some other function/way. For an example
a new Text object is made::

    pprint(text)

    {'Tartu': [{'end': 5, 'start': 0, 'text': 'Tartu'},
               {'end': 291, 'start': 286, 'text': 'Tartu'},
               {'end': 415, 'start': 410, 'text': 'Tartu'},
               {'end': 466, 'start': 461, 'text': 'Tartu'}],
     'Tartu 2': [{'end': 415, 'start': 410, 'text': 'Tartu'}],
     'Tartu Tehnoloogia': [{'end': 303,
                            'start': 286,
                            'text': 'Tartu Tehnoloogia'},
                           {'end': 427,
                            'start': 410,
                            'text': 'Tartu Tehnoloogia'}],
     'text': 'Tartu Ulikooli, Tallinna Tehnikaulikooli ja ettevotete koostoos '
             'initsialiseeritud tehnoloogia arenduskeskus Tarkvara TAK pakub '
             'ettevotetele ja teistele partneritele teadus- ja arendustoo ning '
             'alus ja rakendusuuringute teenuseid. Uurimisvaldkondadeks on '
             'andmekaeve ning tarkvaratehnika. Tartu Tehnoloogia ja Rakenduste '
             'Arenduskeskuste programm on Euroopa Regionaalarengu fondist EAS '
             'kaudu rahastatav programm.  Tartu Tehnoloogia ja Rakenduste '
             'Arenduskeskus asub Tartus juba 5 aastat.'}

To find the ``union`` overlap between layers 'Tartu' and 'Tartu Tehnloogia' you can use the function in the example
below::

    text['union'] = compute_layer_intersection(text, 'Tartu', 'Tartu Tehnoloogia', method= 'union')

    text['union']

The result is::

    [{'start': 286, 'end': 303}, {'start': 410, 'end': 427}]

To find the ``intersection`` overlap between layers 'Tartu' and 'Tartu Tehnloogia' you can use the function in the
example below::

     text['intersection'] = compute_layer_intersection(text, 'Tartu', 'Tartu Tehnoloogia', method= 'intersection')

     text['intersection']

And the result is::

    [{'start': 286, 'end': 291}, {'start': 410, 'end': 415}]

As you can see the results of ``union`` and ``intersection`` are different. This is thanks to the different methods
used. For the purpose of demonstrating the ``exact`` method the layer 'Tartu 2', which has one element, was created.
An example for ``exact`` method is below::

    text['exact'] = compute_layer_intersection(text, 'Tartu', 'Tartu 2', method='exact')

    text['exact']

And the result is::

    [{'end': 415, 'start': 410}]

Notice that the tag ``end`` in layers is exclusive, this means that if ``end`` is for example 15, then the 15th
symbol in the element is not included. This is important when using the ``intersection`` method. Example below::

    text['A'] = [{'start' : 1, 'end' : 15}]
    text['B'] = [{'start' : 15, 'end' : 20}]

    text['intersection'] = compute_layer_intersection(text, 'A', 'B', method = 'intersection')

    text['intersection']

The result is empty, because the 15th symbol in the ``A`` layer is exclusive and this means that the two layers do not
have any overlapping between them. And the result::

    []

