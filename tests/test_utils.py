#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tempfile
from context import utils
from context import config


def test_rand_dir():
    assert len(utils.rand_dir()) == config.RAND_DIR_LENGTH


def test_mkdir():
    tmpfile = tempfile.mkdtemp()
