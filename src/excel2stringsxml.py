#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
from ExcelReader import ExcelReader
from AndroidXmlHandler import AndroidXmlHandler
from iOSStringsHandler import iOSStringsHandler
from constants import Log

def addParser():
    parser = OptionParser()
    parser.add_option("-f", "--filePath",
                      help="original.xls File Path.",
                      metavar="filePath")
    parser.add_option("-t", "--targetFloderPath",
                      help="Target Floder Path.",
                      metavar="targetFloderPath")
    parser.add_option("-i", "--iOSAdditional",
                      help="iOS additional info.",
                      metavar = "iOSAdditional")
    parser.add_option("-a", "--androidAdditional",
                      help="android additional info.",
                      metavar="androidAdditional")
    (options, args) = parser.parse_args()
    Log.info("options: %s, args: %s" % (options, args))
    return options


def startConvert(filePath, targetFloderPath, iOSAdditional, androidAdditional):
    if filePath is not None:
        if targetFloderPath is None:
            Log.error("targetFloderPath is None！use -h for help.")
            return

        # xls
        Log.info("read xls file from"+filePath)
        reader = ExcelReader(filePath)

        # iOS & Android
        table = reader.getTableByIndex(0)
        convertiOSAndAndroidFile(table,targetFloderPath,iOSAdditional,androidAdditional)

        Log.info("Finished,go to see it -> "+targetFloderPath)

    else:
        Log.error("file path is None！use -h for help.")


def convertiOSAndAndroidFile(table,targetFloderPath,iOSAdditional,androidAdditional):
    firstRow = table.row_values(0)

    keys = table.col_values(0)
    del keys[0]

    for index in range(len(firstRow)):
        if index > 0:
            languageName = firstRow[index]
            values = table.col_values(index)
            del values[0]
            # iOS
            iOSStringsHandler.writeToFile(keys,values,targetFloderPath + "/ios/"+languageName+".lproj/",iOSAdditional)

            # Android
            if languageName == "zh-Hans":
                languageName = "zh-rCN"

            path = targetFloderPath + "/android/values-"+languageName+"/"
            if languageName == 'en':
                path = targetFloderPath + "/android/values/"
            AndroidXmlHandler.writeToFile(keys,values,path,androidAdditional)

def main():
    options = addParser()
    startConvert(options.filePath, options.targetFloderPath, options.iOSAdditional, options.androidAdditional)

if __name__=='__main__':
    main()