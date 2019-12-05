""" Temporarily change your python cwd. """

import os
from contextlib import contextmanager


@contextmanager
def tmp_cwd(path):
    """ Change the cwd of your currently executing progam. """
    oldpwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)
