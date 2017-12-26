#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from constants import Log, Contant
import codecs
import re

class iOSStringsHandler:

    @staticmethod
    def writeToFile(keys, baseValues, values, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

        stringsPath = os.path.join(directory, 'Language.strings')
        Log.info("Creating iOS strings file:" + stringsPath)
        filestream = open(stringsPath, "wb")

        for x in range(len(keys)):
            key = keys[x].strip()
            if key is None or key == '':
                continue

            if key == Contant.KEY_DEV_COMMENT:
                comment = baseValues[x].strip()
                filestream.write('/*' + comment + '*/\n')
                continue

            if values[x] is None or values[x] == '':
                # Log.error("Key:" + keys[x] + "\'s value is None. Index:" + str(x))
                continue

            value = values[x].strip()
            filestream.write('"' + key + '"' + ' = ' + '"' + value + '";\n')

        filestream.close()

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
                else:          
                    result = re.split(r'/\*.+\*/\n', line, maxsplit=1)
                    if len(result) == 2:
                        keys.append(Contant.KEY_DEV_COMMENT)
                        values.append(line.strip().replace('/*', '').replace('*/', ''))

        return keys,values