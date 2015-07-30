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

    def query(self, queries):
        if self.restart_per_query:
            self.disconnect()
            self.connect()

        for q in queries:
            self.run_query(q)
            self.query_count += 1

    def run_query(self, query_str):
        raise NotImplementedError

    def get_adapter_name(self):
        raise NotImplementedError
