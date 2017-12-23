#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from constants import Log, Contant
from xml.dom import minidom, Node
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def _elementKeyValue(elementNode):
    key = elementNode.getAttribute('name').strip()
    value = ''
    for node in elementNode.childNodes:
        if node.nodeType == Node.TEXT_NODE:
            value = node.nodeValue.strip()
        elif node.nodeType == Node.ELEMENT_NODE:
            k, v = _elementKeyValue(node)
            value = node.nodeName + Contant.ELEMENT_TAG_DEVIDER + v
        else:
            Log.error('not text node in %s: %s %d %s' % (key, node.nodeName, node.nodeType, node.nodeValue))
    return key, value

def _stringElementKeyValue(elementNode):
    if elementNode.nodeName != 'string':
        return ('', ''), False

    key, value = _elementKeyValue(elementNode)
    if key == '' or value == '':
        return ('', ''), False
    return (key, value), True

class AndroidXmlHandler:
    @staticmethod
    def writeToFile(keys, values,directory,additional):
        if not os.path.exists(directory):
            os.makedirs(directory)

        Log.info("Creating android file:" + directory + "/strings.xml")

        fo = open(directory + "/strings.xml", "wb")

        stringEncoding = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<resources>\n"
        fo.write(stringEncoding)

        for x in range(len(keys)):
            if values[x] is None or values[x] == '' :
                Log.error("Key:" + keys[x] + "\'s value is None. Index:" + str(x + 1))
                continue

            key = keys[x].strip()
            value = re.sub(r'(%\d\$)(@)', r'\1s', values[x])
            content = "   <string name=\"" + key + "\">" + value + "</string>\n"
            fo.write(content)

        if additional is not None:
            fo.write(additional)

        fo.write("</resources>")
        fo.close()

    @staticmethod
    def getDict(path):
        if path is None:
            Log.error('file path is None')
            return
        Log.info('parse %s' % path)

        languageDict = {}
        doc = minidom.parse(path)
        root = doc.documentElement
        nodeList = root.getElementsByTagName('string')

        for node in nodeList:
            if node.nodeType == Node.ELEMENT_NODE:
                retValue, ok = _stringElementKeyValue(node)
                if ok:
                    languageDict[retValue[0]] = retValue[1]
            else:
                Log.error('not support node: %s %d %s' % (node.nodeName, node.nodeType, node.nodeValue))

        return languageDict

    @staticmethod
    def getStandardKeysAndValues(path):
        if path is None:
            Log.error('file path is None')
            return
        Log.info('parse %s' % path)

        keys = []
        values = []
        doc = minidom.parse(path)
        root = doc.documentElement

        for node in root.childNodes:
            if node.nodeType == Node.TEXT_NODE:
                pass
            elif node.nodeType == Node.COMMENT_NODE:
                keys.append(Contant.KEY_DEV_COMMENT)
                values.append(node.nodeValue)
            elif node.nodeType == Node.ELEMENT_NODE:
                retValue, ok = _stringElementKeyValue(node)
                if ok:
                    keys.append(retValue[0])
                    values.append(retValue[1])
            else:
                Log.error('not support node: %s %d %s' % (node.nodeName, node.nodeType, node.nodeValue))

        return keys, values
