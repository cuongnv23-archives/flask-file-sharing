#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import sys


try:
    UPLOAD_DIR = config.UPLOAD_DIR
    LOG_FILE = config.LOG_FILE
    BUFFER_SIZE = config.BUFFER_SIZE
    LOG_LEVEL = config.LOG_LEVEL
    MAX_FILE_SIZE = config.MAX_FILE_SIZE
    RAND_DIR_LENGTH = config.RAND_DIR_LENGTH
except AttributeError as e:
    if 'UPLOAD_DIR' in e.message:
        print "UPLOAD_DIR is not set."
        sys.exit(1)
    if 'LOG_FILE' in e.message:
        print "LOG_FILE is not set."
        sys.exit(1)
    if 'BUFFER_SIZE' in e.message:
        BUFFER_SIZE = 1024 * 16
    if 'LOG_LEVEL' in e.message:
        LOG_LEVEL = 'INFO'
    if 'RAND_DIR_LENGTH' in e.message:
        RAND_DIR_LENGTH = 6
    if 'MAX_FILE_SIZE' in e.message:
        print "MAX_FILE_SIZE is not set."
        sys.exit(1)
