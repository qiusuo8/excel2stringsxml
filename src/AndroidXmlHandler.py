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
            v = node.nodeValue.strip()
            if v != None and v != '':
                value = v
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
    def writeToFile(keys, baseValues, values, directory, isBase):
        if not os.path.exists(directory):
            os.makedirs(directory)

        xmlPath = os.path.join(directory, 'strings.xml')
        Log.info("Creating android xml file:" + xmlPath)

        doc = minidom.Document()
        resourcesNode = doc.createElement('resources')
        if isBase:
            resourcesNode.setAttribute('xmlns:tools', 'http://schemas.android.com/tools')
            resourcesNode.setAttribute('tools:ignore', 'MissingTranslation')
        doc.appendChild(resourcesNode)

        for x in range(len(keys)):
            key = keys[x]
            if key is None or key == '':
                continue
            key = keys[x].strip()

            if key == Contant.KEY_DEV_COMMENT:
                comment = doc.createComment(baseValues[x].strip().decode('utf-8'))
                resourcesNode.appendChild(comment)
                continue

            if values[x] is None or values[x].strip() == '':
                # Log.error("Key:" + keys[x] + "\'s value is None. Index:" + str(x))
                continue

            stringEle = doc.createElement('string')
            stringEle.setAttribute('name', key)
            resourcesNode.appendChild(stringEle)    
            textNodeParent = stringEle   

            value = values[x].strip()
            result = re.split(Contant.ELEMENT_TAG_DEVIDER, value, maxsplit=1)
            if len(result) == 2 and result[0] == 'u':
                value = result[1]
                uEle = doc.createElement('u')
                stringEle.appendChild(uEle)
                textNodeParent = uEle

            value = re.sub(r'(%\d\$)(@)', r'\1s', value)
            textNode = doc.createTextNode(value.decode('utf-8'))
            textNodeParent.appendChild(textNode)

        filestream = open(xmlPath, "wb")
        filestream.write(doc.toprettyxml(encoding='utf-8'))
        filestream.close()

    @staticmethod
    def getKeyValueDictByPath(path):
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
    def getKeysAndValuesByPath(path):
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
