# -*- coding: utf-8 -*-
#from estnltk.wiki.iterParser import totalTime

__author__ = 'Andres'

#incremental XML parsing
import re
from xml.etree.ElementTree import iterparse

from infoBox import infoBoxParser
from sections import sectionsParser
from references import referencesFinder,refsParser
from categoryParser import categoryParser
import time
from jsonWriter import jsonWriter
from cleaner import clean

totalwriter = 0
totalComp = 0
totalTime = 0

# Matches bold/italic
bold_italic = re.compile(r"'''''(.*?)'''''")
bold = re.compile(r"'''(.*?)'''")
italic_quote = re.compile(r"''\"([^\"]*?)\"''")
italic = re.compile(r"''(.*?)''")
quote_quote = re.compile(r'""([^"]*?)""')

# Matches space
spaces = re.compile(r' {2,}')

# Matches dots
dots = re.compile(r'\.{4,}')


def parse_and_remove(filename, path):
    path_parts = path.split('/')
    doc = iterparse(filename, ('start', 'end'))
    # Skip the root element
    #next(doc)

    tag_stack = []
    elem_stack = []
    for event, elem in doc:
        if event == 'start' in elem.tag:
            tag_stack.append(elem.tag)
            elem_stack.append(elem)
        elif event == 'end':
            eletag = elem.tag
            elemtext = elem.text
            yield eletag, elemtext

            if tag_stack == path_parts:
                yield elem
                elem_stack[-2].remove(elem)
            try:
                tag_stack.pop()
                elem_stack.pop()
            except IndexError:
                pass



data = parse_and_remove('G:\WikiDumper\etwiki-latest-pages-articles.xml', "wikimedia/wikimedia" )
linkBegin = "http://et.wikipedia.org/wiki/"
#G:\WikiDumper\etwiki-latest-pages-articles.xml

ib = re.compile(r'(?!\<ref>)\{\{[^\}]+?\n ?\|.+?=')
pageObj = {}
count = 0
errata = []
for tag, text in data:
    tag, text = str(tag), str(text)


    if 'title' in tag:
        pageObj['title'] = text
        pageObj['url'] = linkBegin+text.replace(' ', '_')
        print('-----------')
        print(pageObj['title'])
        #print(pageObj['url'])
    if 'timestamp' in tag:
        pageObj['timestamp'] = text
        #print(pageObj['timestamp'])

 #   def refsParser(refsDict):
 #       for k, v in refsDict.items():
 #           pass



    if 'text' in tag:
        #if '#REDIRECT' or '#suuna' in text:
        #print('REDIRECT')
        #    continue
        compStart = time.time()
        #TOdO: remove junk from text
        m = re.search(ib, text)

        if m:
            mg  = m.group()
            text, pageObj['infobox'] = infoBoxParser(text)
            #print(pageObj['infobox'])
        #try:
        ##pprint(referencesFinder(text))
        #Finds and marks nicely all the references in the article, returns a tag:reference dictionary
        text, refsDict = referencesFinder(text)
        refsDict = refsParser(refsDict)
        #SectionParser is where all the work with links, images etc gets done
        text, catList = categoryParser(text)
        text = clean(text)
        pageObj['categories'] = catList
        sectionobj = (sectionsParser(text, pageObj['title'], refsDict))

        pageObj['sections'] = sectionobj
        #print(pageObj['sections'])
        #except AttributeError:

         #   count += 1
         #   errata.append(pageObj['title'])
         #   print('Error: ', count)

        # Pageobj done convert to json. write to disk.

        #Precious time

        thisComp = time.time() - compStart
        totalComp += thisComp
        #print('Progtime : ',thisComp , totalComp)
        timestart = time.time()
        jsonWriter(pageObj, 'G:\Json\\')
        thisWrite = time.time()-timestart
        totalwriter += thisWrite
        #print('Writetime: ' , thisWrite ,totalwriter)


        pageObj = {}
        totalTime +=thisComp + thisWrite
        print('Totaltime: ' , totalTime)
#TODO.  pudi-padi, special pages


"""
Go through dictionary
def myprint(d):
  for k, v in d.iteritems():
    if isinstance(v, dict):
      myprint(v)
    else:
      print "{0} : {1}".format(k, v)
"""