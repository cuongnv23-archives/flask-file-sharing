#!/usr/bin/env python
# -*- coding: utf-8 -*-


from StringIO import StringIO
from .context import app
import pytest
from config import MAX_FILE_SIZE


# Test application methods
@pytest.fixture
def client():
    ''' Create test_client '''
    app.testing = True
    test = app.test_client()
    return test


def test_get(client):
    ''' Test GET '''
    rv_405 = client.get('/')
    assert rv_405.status_code == 405


def test_post(client):
    ''' Test POST '''
    data_sample = {'file': (StringIO('file content'), 'test.txt')}
    empty_data = {'file': 'test.txt'}
    large_data = {'file': (StringIO('file content' * MAX_FILE_SIZE),
                           'test.txt')}
    rv_201 = client.post('/', data=data_sample)
    rv_201_stream = client.post('/test.txt', data='file content')
    rv_400_empty = client.post('/', data=empty_data)
    rv_400_stream = client.post('/test.txt')
    rv_413 = client.post('/', data=large_data)

    assert rv_201.status_code == 201
    assert rv_201.data.endswith('test.txt')
    assert rv_201_stream.status_code == 201
    assert rv_201_stream.data.endswith('test.txt')
    assert rv_400_empty.status_code == 400
    assert rv_400_empty.data == 'Data not received'
    assert rv_400_stream.status_code == 400
    assert rv_413.status_code == 413
    assert rv_413.data == 'File too large. Limit {}MB'.format(
        MAX_FILE_SIZE / 1024 / 1024)


def test_put(client):
    ''' Test PUT '''
    data_sample = 'file content'
    rv_201 = client.put('/test.txt', data=data_sample)
    rv_400 = client.put('/', data=data_sample)
    rv_413 = client.put('/test.txt', data=data_sample * MAX_FILE_SIZE)

    assert rv_201.status_code == 201
    assert rv_201.data.endswith('test.txt')
    assert rv_400.status_code == 400
    assert rv_400.data == 'Data not received'
    assert rv_413.status_code == 413
    assert rv_413.data == 'File too large. Limit {}MB'.format(
        MAX_FILE_SIZE / 1024 / 1024)
