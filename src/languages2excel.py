#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from optparse import OptionParser
from iOSStringsHandler import iOSStringsHandler
from AndroidXmlHandler import AndroidXmlHandler
import sys
from constants import Log
current_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(current_path)[0]
sys.path.append(root_path)
import pyExcelerator

def _addParser():
    parser = OptionParser()
    parser.add_option("-s", "--sourceFolder",
                      dest="sourceFolder",
                      default="",
                      help="strings or xml in this folder",
                      metavar="sourceFolder")
    parser.add_option("-x", "--xlsFolder",
                      dest="xlsFolder",
                      default="",
                      help="generate xls in this folder",
                      metavar="xlsFolder")
    parser.add_option("-t", "--type",
                      dest="apptype",
                      help="ios or android",
                      metavar="type")
    (options, args) = parser.parse_args()
    return options

def _getCountryCode(foldername, apptype):
    code = ''
    if apptype == 'ios':
        code = foldername.split('.')[0]
    else:
        dirSplit = foldername.split('values-')
        if len(dirSplit) > 1:
            code = dirSplit[1]
        else:
            code = 'en'
    return code

def _getStandardKeyValuesListFrom(languageFolder, apptype):
    if apptype == 'ios':
        path = os.path.join(languageFolder, "en.lproj", 'Language.strings')
        return iOSStringsHandler.getKeysAndValuesByPath(path)
    else:
        path = os.path.join(languageFolder, "values", 'strings.xml')
        return AndroidXmlHandler.getKeysAndValuesByPath(path)

def _getKeyValuesDictFrom(stringsFolder, apptype):
    if apptype == 'ios':
        path = os.path.join(stringsFolder, 'Language.strings')
        return iOSStringsHandler.getKeyValueDictByPath(path)
    else:
        path = os.path.join(stringsFolder, 'strings.xml')
        return AndroidXmlHandler.getKeyValueDictByPath(path)

def startConvert(sourceFolder, xlsFolder, apptype):
    if sourceFolder is not None:
        if xlsFolder is not None:
            workbook = pyExcelerator.Workbook()
            ws = workbook.add_sheet('Localizable.strings')

            # init keyName and standard language value (en)
            stKeys, stValues = _getStandardKeyValuesListFrom(sourceFolder, apptype)
            if len(stKeys) <= 0:
                Log.error('The language files is empty')
                return

            ws.write(0, 0, 'keyName')
            ws.write(0, 1, 'en')
            for row in range(len(stKeys)):
                ws.write(row+1, 0, stKeys[row])
                ws.write(row+1, 1, stValues[row])

            # append other language value
            index = 2
            for parent, dirnames, filenames in os.walk(sourceFolder):
                for dirname in dirnames:
                    conturyCode = _getCountryCode(dirname, apptype)
                    if conturyCode == 'en':
                        continue

                    ws.write(0, index, conturyCode)
                    otherLanguage = _getKeyValuesDictFrom(os.path.join(sourceFolder, dirname), apptype)
                    for row in range(len(stKeys)):
                        if stKeys[row] in otherLanguage:
                            ws.write(row+1, index, otherLanguage[stKeys[row]])
                    index += 1

            filePath = os.path.join(xlsFolder, "Localizable.xls")
            workbook.save(filePath)
            Log.info("Convert successfully! you can see xls file in %s" % (filePath))
        else:
            Log.error("xls folder path can not be empty! try -h for help.")
    else:
        Log.error("strings or xml files filder can not be empty! try -h for help.")


def main():
    options = _addParser()
    startConvert(options.sourceFolder, options.xlsFolder, options.apptype)

if __name__=='__main__':
    main()