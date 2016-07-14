#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import string
import errno
from config import RAND_DIR_LENGTH, MAX_FILE_SIZE
from random import SystemRandom as SR
from flask import request, abort
from upload.logs import logger


def mkdir(path):
    ''' Create directory '''
    logger.info('Creating directory {}'.format(path))
    try:
        os.mkdir(path)
        logger.info('{} created!'.format(path))
    except IOError as io_exc:
        logger.error('{}'.format(io_exc), exc_info=True)
        raise
    except OSError as os_exc:
        if os_exc.errno == errno.EEXIST and os.access(path, os.W_OK):
            logger.warn('{} already exists'.format(path))
        else:
            logger.error('Failed to create dir {}'.format(path), exc_info=True)
            raise


def rand_dir():
    ''' Generate random string to be url path '''
    return ''.join(SR().choice(string.ascii_letters + string.digits)
                   for _ in range(RAND_DIR_LENGTH))


def write_stream(file_path):
    '''
    Write file by accessing to stream
    http://flask.pocoo.org/docs/0.11/api/#flask.Request.stream
    '''
    try:
        with open(file_path, 'wb') as f:
            buf_max = 1024 * 500
            buf = 1024 * 16
            while True:
                chunk = request.stream.read(buf)
                if chunk:
                    f.write(chunk)
                    if buf < buf_max:
                        buf = buf * 2
                else:
                    break
    except:
        logger.error('Failed to save file {}'.format(file_path), exc_info=True)
        raise


def write_form(file_path, file_obj):
    '''
    Write file by accessing to 'save'
    https://github.com/pallets/werkzeug/blob/master/werkzeug/datastructures.py#L2635
    '''
    try:
        file_obj.save(file_path)
    except:
        logger.error('Failed to save file {}'.format(file_path, exc_info=True))
        raise


def validate_filesize():
    ''' Check if request contains data and filter file type '''
    if request.headers.get('Content-Length'):
        file_size = int(request.headers.get('Content-Length'))
    else:
        file_size = None
    if file_size > MAX_FILE_SIZE:
        abort(413)
    if not file_size:
        abort(400, 'No data received')
