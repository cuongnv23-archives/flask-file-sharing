#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask import Flask, request, make_response, \
    send_from_directory, abort, url_for
from werkzeug.utils import secure_filename
from upload.settings import UPLOAD_DIR, MAX_FILE_SIZE
from upload import utils
from upload.logs import logger


app = Flask(__name__)
utils.mkdir(UPLOAD_DIR)
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE


@app.errorhandler(400)
def bad_request(error):
    ''' HTTP 400 code '''
    return make_response('{}'.format(error.description), 400)


@app.errorhandler(404)
def not_found(error):
    ''' HTTP 404 code '''
    logger.error('File not found')
    return make_response('{}'.format(error.description), 404)


@app.errorhandler(405)
def not_allowed(error):
    ''' HTTP 405 code '''
    logger.error('Method not allowed')
    return make_response('{}'.format(error.description), 405)


@app.errorhandler(413)
def file_too_large(error):
    ''' HTTP 413 code '''
    file_size = int(request.headers.get('Content-Length')) / 1024 / 1024
    limit_size = MAX_FILE_SIZE / 1024 / 1024
    logger.error('File too large: {}MB'.format(file_size))
    return make_response('File too large. Limit {}MB'.format(limit_size), 413)


@app.route('/', defaults={'filename': ''}, methods=['POST', 'PUT'])
@app.route('/<string:filename>', methods=['POST', 'PUT'])
def upload(filename):
    ''' Write data '''
    if request.method == 'POST':
        if filename:
            abort(404, 'Endpoint \'{}\' not found'.format(filename))
        file_obj = request.files.get('file')
        if not file_obj:
            abort(400, 'Data not received')
        filename = secure_filename(file_obj.filename)
        utils.validate_data(filename)
    elif request.method == 'PUT':
        if not filename:
            abort(400, 'Data not received')
        filename = secure_filename(filename)
        utils.validate_data(filename)
        file_obj = None

    rand_dir = utils.rand_dir()
    store_dir = os.path.join(UPLOAD_DIR, rand_dir)
    utils.mkdir(store_dir)
    url_path = '/'.join([rand_dir, filename])
    utils.save(os.path.join(store_dir, filename), file_obj)

    return url_for("download", path=url_path, _external=True), 201


@app.route('/<path:path>', methods=['GET'])
def download(path):
    ''' Return file from path directory'''
    logger.info('GET {}'.format(path))
    return send_from_directory(UPLOAD_DIR, path)
