#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import string
import errno
from config import RAND_DIR_LENGTH, BUFFER_SIZE, MAX_FILE_SIZE
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


def write_put(file_path):
    ''' Write file for PUT request '''
    try:
        with open(file_path, 'wb') as f:
            while True:
                chunk = request.stream.read(BUFFER_SIZE)
                if chunk:
                    f.write(chunk)
                else:
                    break
    except:
        logger.error('Failed to save file {}'.format(file_path), exc_info=True)
        raise


def write_post(file_path, file_obj):
    ''' Write file to POST method '''
    try:
        file_obj.save(file_path, BUFFER_SIZE)
    except:
        logger.error('Failed to save file {}'.format(file_path, exc_info=True))
        raise


def validate_data(filename):
    ''' Check if request contains data and filter file type '''
    file_size = int(request.headers.get('Content-Length', 0))
    if file_size > MAX_FILE_SIZE:
        abort(413)
    if file_size == 0:
        abort(400, 'No data received')
