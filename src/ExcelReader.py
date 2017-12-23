#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

current_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(current_path)[0]
sys.path.append(root_path)

import xlrd

class ExcelReader:
    'xls file util'

    def __init__(self,filePath):
        self.filePath = filePath
        # get all sheets
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.data = xlrd.open_workbook(filePath)

    def getAllTables(self):
        return self.data.sheets()

    def getTableByIndex(self,index):
        if index >= 0 and index < len(self.data.sheets()):
            return self.data.sheets()[index]
        else:
            print("ExcelReader error -- getTable:index")

    def getTableByName(self,name):
        return self.data.sheet_by_name(name)