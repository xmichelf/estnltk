import estnltk
from collections import defaultdict
import lxml.html as html
import lxml.etree as etree


def remove_comments(element):
    for c in element.xpath('//comment()'):
        p = c.getparent()
        p.remove(c)
    return element


def cleanup_br(element):
    """Replaces <br> tags in the tree with linebreaks
    :param element: html.HtmlElement
    """
    for e in element.xpath('br'):
        try:
            e.tail = '\n' + e.tail
        except TypeError:
            e.tail = '\n'
        e.drop_tree()
    return element


def html_to_estnltk(html_text, drop_tags = ('style', 'head')):
    """
    Returns estnltk.text object with most html tags added as layers.
    Tags with content length 0 are removed unless they have attribute values.
    Linebreaks (<br>) are replaced with newlines (\n).
    Resolves entities to unicode values.

    :param html_text: text of html snippet
    :return: estnltk.Text
    """
    root = html.fragment_fromstring(html_text, create_parent='root')
    root = cleanup_br(root)
    root = remove_comments(root)
    texts = []

    tag_stacks = defaultdict(list)
    tag_spans = defaultdict(list)

    counter = 0
    for event, element in etree.iterwalk(root, events=('start', 'end')):
        if element.tag in drop_tags:
            continue

        if event == 'start':
            tag_stacks[element.tag].append((counter, element.attrib))
            text = element.text
            if text is not None:
                counter += len(text)
                texts.append(text)

        elif event == 'end':
            text = element.tail
            if text is not None:
                texts.append(text)

            start_i, attrib = tag_stacks[element.tag].pop()
            tag_spans[element.tag].append((start_i, counter, attrib))
            if text is not None:
                counter += len(text)


    del tag_spans['root']
    layers = {}
    for k, v in tag_spans.items():
        layers[k] = [{'start': a, 'end': b, 'attrib': attrib} for a, b, attrib in v if ((a != b) or attrib)]

    text = estnltk.Text(''.join(texts))
    text.update(layers)
    return text

