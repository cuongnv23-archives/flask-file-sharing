#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

BASE_DIR = os.path.curdir
# directory store files. Default '/tmp/uploads'
UPLOAD_DIR = '/tmp/uploads'
# length of uri in random format. Default '6'
RAND_DIR_LENGTH = 6
# max file size. Default '10MB'
MAX_FILE_SIZE = 1024 * 1024 * 10
# buffer memory to save file. Default '16KB'
BUFFER_SIZE = 1024 * 16
# log level(CRITICAL, ERROR, WARNING, INFO, DEBUG). Default 'INFO'
LOG_LEVEL = 'INFO'
# log file. Default '/tmp/upload.log'
LOG_FILE = '/tmp/upload.log'
