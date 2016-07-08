#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import string
import errno
try:
    from config import RAND_DIR_LENGTH, BUFFER_SIZE, MAX_FILE_SIZE
except ImportError:
    RAND_DIR_LENGTH = 6
    BUFFER_SIZE = 1024 * 16
    MAX_FILE_SIZE = 1024 * 1024 * 10
from random import SystemRandom as SR
from flask import request, abort
from upload.logs import logger


def mkdir(path):
    ''' Create directory '''
    logger.info('Creating directory {}'.format(path))
    if os.path.isdir(path) and not os.access(path, os.W_OK):
        logger.error('{} exists but not accessible'.format(path),
                     exc_info=True)
        raise OSError('{} exists but not accessible'.format(path))
    try:
        os.mkdir(path)
        logger.info('{} created!'.format(path))
    except IOError as io_exc:
        logger.error('{}'.format(io_exc), exc_info=True)
        raise
    except OSError as os_exc:
        if os_exc.errno == errno.EEXIST:
            logger.warn('{} already exists'.format(path))
        else:
            raise
    except:
        raise


def rand_dir():
    ''' Generate random string to be url path '''
    return ''.join(SR().choice(string.ascii_letters + string.digits)
                   for _ in range(RAND_DIR_LENGTH))


def _write_put(file_path):
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


def _write_post(file_path, file_obj):
    ''' Write file to POST method '''
    try:
        file_obj.save(file_path, BUFFER_SIZE)
    except:
        logger.error('Failed to save file {}'.format(file_path, exc_info=True))
        raise


def save(file_path, file_obj=None):
    ''' Write file_obj to file_path depend on method '''
    logger.info('Saving file to {}'.format(file_path))
    if file_obj:
        _write_post(file_path, file_obj)
    else:
        _write_put(file_path)
    logger.info('{} saved!'.format(file_path))


def validate_data(filename):
    ''' Check if request contains data and filter file type '''
    file_size = int(request.headers.get('Content-Length', 0))
    if file_size > MAX_FILE_SIZE:
        abort(413)
    if file_size == 0:
        abort(400, 'No data received')
