""" Create a temporary copy of a path inside a context manager. """
from os import path, remove
from shutil import copyfile


class tmp_copy:  # pylint: disable=invalid-name
    """ Create a temporary copy of a path inside a context manager. """

    def __init__(self, src_path: str, dst_path: str = "."):

        self.src_path = src_path
        _, filename = path.split(src_path)
        self.dst_path = path.join(dst_path, filename)
        copyfile(src_path, self.dst_path)

    def __enter__(self):
        return self

    def __exit__(self, _, value, traceback):

        remove(self.dst_path)
