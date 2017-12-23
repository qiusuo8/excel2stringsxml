#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from optparse import OptionParser
from AndroidXmlHandler import AndroidXmlHandler
from iOSStringsHandler import  iOSStringsHandler

def addParser():
    parser = OptionParser()
    parser.add_option("-f", "--filePath",
                      help="Localizable.strings File Path.",
                      metavar="filePath")
    parser.add_option("-t", "--targetFilePath",
                      help="Target File (strings.xml) Path.",
                      metavar="targetFilePath")
    parser.add_option("-a", "--androidAdditional",
                      help="android additional info.",
                      metavar="androidAdditional")
    (options, args) = parser.parse_args()
    return options


def startConvert(options):
    filePath = options.filePath
    targetFilePath = options.targetFilePath
    androidAdditional = options.androidAdditional

    if filePath is not None:
        print "Read Localizable.strings file from %s" % (filePath)

        (keys, values) = iOSStringsHandler.getKeysAndValues(filePath)

        print "Read Localizable.strings finish"

        if targetFilePath is not None:
            AndroidXmlHandler.writeToFile(keys,values,targetFilePath,androidAdditional)

            print "Convert successfully! you can see strings.xml in %s" % (targetFilePath)

        else:
            print "Target file path can not be empty! try -h for help."

    else:
        print "File path can not be empty! try -h for help."


def main():
    options = addParser()
    startConvert(options)

if __name__=='__main__':
    main()