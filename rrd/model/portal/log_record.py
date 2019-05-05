__author__ = 'Yiwen Chen'

from .bean import Bean
from rrd.config import MAINTAINERS
from rrd.store import db

class LogRecorder(Bean):
    _tbl = 'filepath_record'
    _cols = 'id, username, path1, path2, path3, path4, path5'

    def __init__(self, _id, username, path1, path2, path3, path4, path5):
        self.id = _id
        self.username = username
        self.path1 = path1
        self.path2 = path2
        self.path3 = path3
        self.path4 = path4
        self.path5 = path5