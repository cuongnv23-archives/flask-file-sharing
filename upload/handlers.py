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
    logger.error('File not found')
    return make_response('{}'.format(err.description), 404)


@app.errorhandler(405)
def not_allowed(err):
    ''' HTTP 405 code '''
    logger.error('Method not allowed')
    return make_response('{}'.format(err.description), 405)


@app.errorhandler(413)
def file_too_large(err):
    ''' HTTP 413 code '''
    file_size = int(request.headers.get('Content-Length')) / 1024 / 1024
    limit_size = MAX_FILE_SIZE / 1024 / 1024
    logger.error('File too large: {}MB'.format(file_size))
    return make_response('File too large. Limit {}MB'.format(limit_size), 413)


@app.route('/', defaults={'filename': ''}, methods=['POST', 'PUT'])
@app.route('/<string:filename>', methods=['POST', 'PUT'])
def upload(filename):
    ''' Write data '''

    utils.validate_filesize()
    rand_dir = utils.rand_dir()
    store_dir = os.path.join(UPLOAD_DIR, rand_dir)
    if request.method == 'POST':
        file_obj = request.files.get('file', None)
        if file_obj:
            '''
            Request sent in form.
            ex: curl -X POST -F file=@filename
            '''
            if not filename:
                '''
                Only accept request with '/' endpoint.
                Get filename from file object.
                '''
                utils.mkdir(store_dir)
                file_name = secure_filename(file_obj.filename)
                url_path = '/'.join([rand_dir, file_name])
                utils.write_fileobj(os.path.join(store_dir, file_name),
                                    file_obj)
            elif filename:
                '''
                Return 404 if filename is also endpoint
                '''
                abort(404, '{} not found'.format(filename))
            else:
                '''
                Return 400 in unhandled cases
                '''
                abort(400)
        else:
            '''
            This supports uploading file without sepcifying form in request
            ex: curl --upload-file file -X POST
            '''
            if filename:
                '''
                Only allow if filename specified
                '''
                utils.mkdir(store_dir)
                url_path = '/'.join([rand_dir, filename])
                utils.write_stream(os.path.join(store_dir, filename))
            else:
                abort(400, 'Data not received')

    elif request.method == 'PUT':
        if not filename:
            '''
            In PUT request, file name must specified in request URL
            ex: curl --upload-file file
            or curl -X PUT -F file=@filename
            '''
            abort(400, 'Data not received')
        file_name = secure_filename(filename)
        utils.mkdir(store_dir)
        url_path = '/'.join([rand_dir, file_name])
        utils.write_stream(os.path.join(store_dir, file_name))

    return url_for("download", path=url_path, _external=True), 201


@app.route('/<path:path>', methods=['GET'])
def download(path):
    ''' Return file from path directory'''
    logger.info('GET {}'.format(path))
    return send_from_directory(UPLOAD_DIR, path)
