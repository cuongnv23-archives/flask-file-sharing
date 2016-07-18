#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask import Flask, request, make_response, \
    send_from_directory, abort, url_for
from werkzeug.utils import secure_filename
from config import UPLOAD_DIR, MAX_FILE_SIZE
from upload import utils
from upload.logs import logger


app = Flask(__name__)
utils.mkdir(UPLOAD_DIR)
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE


@app.errorhandler(400)
def bad_request(err):
    ''' HTTP 400 code '''
    return make_response('{}'.format(err.description), 400)


@app.errorhandler(404)
def not_found(err):
    ''' HTTP 404 code '''
    logger.error('Not found')
    return make_response('Not found', 404)


@app.errorhandler(405)
def not_allowed(err):
    ''' HTTP 405 code '''
    logger.error('Method not allowed')
    return make_response('Method not allowed', 405)


@app.errorhandler(413)
def file_too_large(err):
    ''' HTTP 413 code '''
    file_size = request.content_length / 1024 / 1024
    limit_size = MAX_FILE_SIZE / 1024 / 1024
    logger.error('File too large: {}MB'.format(file_size))
    return make_response('File too large. Limit {}MB'.format(limit_size), 413)


@app.route('/', defaults={'file_name': ''}, methods=['POST', 'PUT'])
@app.route('/<string:file_name>', methods=['POST', 'PUT'])
def upload(file_name):
    ''' Write data '''
    rand_dir = utils.rand_dir()
    store_dir = os.path.join(UPLOAD_DIR, rand_dir)
    file_obj = request.files.get('file')
    if file_obj:
        '''
        curl -X POST|PUT -F file=@myfile
        '''
        # check if file sent is empty or not
        file_obj.seek(0, os.SEEK_END)
        filesize = file_obj.tell()

        if not file_name:
            fname = secure_filename(file_obj.filename)
        else:
            fname = secure_filename(file_name)
        utils.validate_filesize(filesize)
        url_path = '/'.join([rand_dir, fname])
        utils.mkdir(store_dir)
        utils.write_form(os.path.join(store_dir, fname), file_obj)
    elif not file_obj and file_name:
        '''
        curl -X POST|PUT --upload-file myfile
        '''
        filesize = request.content_length
        utils.validate_filesize(filesize)
        fname = secure_filename(file_name)
        url_path = '/'.join([rand_dir, fname])
        utils.mkdir(store_dir)
        utils.write_stream(os.path.join(store_dir, fname))
    else:
        abort(400)
    return url_for("download", path=url_path, _external=True), 201


@app.route('/<path:path>', methods=['GET'])
def download(path):
    ''' Return file from path directory'''
    logger.info('GET {}'.format(path))
    return send_from_directory(UPLOAD_DIR, path)
