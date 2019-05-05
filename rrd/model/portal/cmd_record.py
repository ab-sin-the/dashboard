__author__ = 'Yiwen Chen'

from .bean import Bean
from rrd.config import MAINTAINERS
from rrd.store import db

class CMDRecorder(Bean):
    _tbl = 'command_record'
    _cols = 'id, username, command1, command2, command3, command4, command5'

    def __init__(self, _id, username, command1, command2, command3, command4, command5):
        self.id = _id
        self.username = username
        self.command1 = command1
        self.command2 = command2
        self.command3 = command3
        self.command4 = command4
        self.command5 = command5