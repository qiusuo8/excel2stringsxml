#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, codecs, re
from xml.dom import minidom, Node
from optparse import OptionParser
from constants import Log

def _addParser():
    parser = OptionParser()
    parser.add_option("-x", "--xmlpath",
                      dest="xmlpath",
                      default="",
                      help="xml file path",
                      metavar="xmlpath")
    parser.add_option("-s", "--stringspath",
                      dest="stringspath",
                      default="",
                      help="strings file path",
                      metavar="stringspath")
    (options, args) = parser.parse_args()
    Log.info("options: %s, args: %s" % (options, args))
    return options

def parseXMLToCheckKeyUniqueAt(filepath):
    if filepath is None or filepath == '':
        print('filepath is empty')
        return
    Log.info('parse %s' % filepath)

    doc = minidom.parse(filepath)
    root = doc.documentElement
    nodeList = root.getElementsByTagName('string')

    keyDict = dict()

    for node in nodeList:
        if node.nodeType == Node.ELEMENT_NODE:
            key = node.getAttribute('name').strip()
            count = keyDict.get(key, 0)
            keyDict[key] = count + 1
    
    for k, v in keyDict.iteritems():
        if v > 1:
            Log.error('%s appear %d!!!' % (k, v))

def parseStringsToCheckKeyUniqueAt(filepath):
    if filepath is None:
        Log.error('file path is None')
        return
    Log.info('parse %s' % filepath)

    keyDict = {}
    file = codecs.open(filepath, mode='r', encoding='utf-8')
    while True:
        lines = file.readlines(sizehint=1000)
        if not lines:
            break

        for line in lines:
            retvalue = re.split(r'"[ ]*=[ ]*"', line, maxsplit=1)
            if len(retvalue) > 1:
                k = retvalue[0].lstrip()[1:]
                count = keyDict.get(k, 0)
                keyDict[k] = count + 1

    for k, v in keyDict.iteritems():
        if v > 1:
            Log.error('%s appear %d!!!' % (k, v))


def main():
    option = _addParser()
    parseXMLToCheckKeyUniqueAt(option.xmlpath)
    parseStringsToCheckKeyUniqueAt(option.stringspath)

if __name__ == '__main__':
    main()