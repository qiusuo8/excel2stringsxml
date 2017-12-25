#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
from ExcelReader import ExcelReader
from AndroidXmlHandler import AndroidXmlHandler
from iOSStringsHandler import iOSStringsHandler
from constants import Log
import os

def _addParser():
    parser = OptionParser()
    parser.add_option("-x", "--xls",
                      dest="xls",
                      default="",
                      help="xls file path",
                      metavar="xls")
    parser.add_option("-s", "--targetFolder",
                      dest="targetFolder",
                      default="",
                      help="generate strings and xml in this folder",
                      metavar="targetFolder")
    (options, args) = parser.parse_args()
    Log.info("options: %s, args: %s" % (options, args))
    return options

def startConvert(xlsPath, targetFolder):
    if xlsPath is not None:
        if targetFolder is None:
            Log.error("targetFolder is None！use -h for help.")
            return

        Log.info("read xls file from" + xlsPath)
        reader = ExcelReader(xlsPath)
        table = reader.getTableByIndex(0)
        convertExcelTableToStringsXml(table, targetFolder)
        Log.info("Finished,go to see it -> " + targetFolder)
    else:
        Log.error("file path is None！use -h for help.")

def convertExcelTableToStringsXml(table, targetFolder):
    countryCodeList = table.row_values(0)

    keyNameList = table.col_values(0)
    del keyNameList[0]

    baseIndex = countryCodeList.index('en')
    baseValueList = table.col_values(baseIndex)
    del baseValueList[0]

    for i in range(1, len(countryCodeList)):
        countryCode = countryCodeList[i]
        values = table.col_values(i)
        del values[0]
        # iOS
        iOSStringsHandler.writeToFile(keyNameList, baseValueList, values, os.path.join(targetFolder, 'ios', countryCode + '.lproj'))

        #Android
        if countryCode == "zh-Hans":
            countryCode = "zh-rCN"
        countryCodeFolder = 'values-' + countryCode
        if countryCode == 'en':
            countryCodeFolder = 'values'
        path = os.path.join(targetFolder, 'android', countryCodeFolder)
        AndroidXmlHandler.writeToFile(keyNameList, baseValueList, values, path, countryCode == 'en')

def main():
    options = _addParser()
    startConvert(options.xls, options.targetFolder)

if __name__=='__main__':
    main()