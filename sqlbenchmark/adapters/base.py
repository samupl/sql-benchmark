# -*- coding: utf-8 -*-


class BaseAdapter(object):

    def __init__(self, host, port, username, password, database):
        self.restart_per_query = False
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.query_count = 0

    def connect(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError

    def query(self, query_str):
        if self.restart_per_query:
            self.disconnect()
            self.connect()
        raise NotImplementedError

    def get_adapter_name(self):
        raise NotImplementedError
