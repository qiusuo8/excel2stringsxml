#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

class Contant:
    KEY_DEV_COMMENT = 'dev_comment'
    ELEMENT_TAG_DEVIDER = '@#$&'

class Log:
    'Log util'

    #Log error
    @staticmethod
    def info(msg):
        message = '\033[1;30;50m' + '[INFO]: %s' % msg + '\033[0m'
        print(message)

    #Log error
    @staticmethod
    def error(msg):
        message = '\033[1;31;50m' + '[ERROR]: %s' % msg + '\033[0m'
        print(message)