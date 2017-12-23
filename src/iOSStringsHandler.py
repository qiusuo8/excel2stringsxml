#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from constants import Log
import codecs
import re

class iOSStringsHandler:

    @staticmethod
    def writeToFile(keys,values,directory,additional):
        if not os.path.exists(directory):
            os.makedirs(directory)

        Log.info("Creating iOS file:" + directory+"Localizable.strings")

        fo = open(directory+"Language.strings", "wb")

        for x in range(len(keys)):
            if values[x] is None or values[x] == '':
                Log.error("Key:" + keys[x] + "\'s value is None. Index:" + str(x + 1))
                continue

            key = keys[x].strip()
            value = values[x]
            content = "\"" + key + "\" " + "= " + "\"" + value + "\";\n"
            fo.write(content);

        if additional is not None:
            fo.write(additional)

        fo.close()

    @staticmethod
    def getKeyValueDictByPath(path):
        if path is None:
            Log.error('file path is None')
            return
        Log.info('parse %s' % path)

        keyvalue = {}
        file = codecs.open(path, mode='r', encoding='utf-8')
        while True:
            lines = file.readlines(sizehint=1000)
            if not lines:
                break

            for line in lines:
                retvalue = re.split(r'"[ ]*=[ ]*"', line, maxsplit=1)
                if len(retvalue) > 1:
                    k = retvalue[0].lstrip()[1:]
                    v = retvalue[1].rstrip().rstrip(' ;')[:-1]
                    keyvalue[k] = v

        return keyvalue

    @staticmethod
    def getKeysAndValuesByPath(path):
        if path is None:
            Log.error('file path is None')
            return
        Log.info('parse %s' % path)

        keys = []
        values = []
        file = codecs.open(path, mode='r', encoding='utf-8')
        while True:
            lines = file.readlines(sizehint=1000)
            if not lines:
                break

            for line in lines:
                retvalue = re.split(r'"[ ]*=[ ]*"', line, maxsplit=1)
                if len(retvalue) > 1:
                    keys.append(retvalue[0].lstrip()[1:])
                    values.append(retvalue[1].rstrip().rstrip(' ;')[:-1])

        return keys,values