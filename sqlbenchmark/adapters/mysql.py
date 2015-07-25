# -*- coding: utf-8 -*-
import MySQLdb

from sqlbenchmark.adapters.base import BaseAdapter


class MySQLBenchmarkAdapter(BaseAdapter):

    def __init__(self, host, port, username, password, database):
        super(MySQLBenchmarkAdapter, self).__init__(host, port, username, password, database)
        self.db = None

        if port is None:
            self.port = 3306

    def connect(self):
        self.db = MySQLdb.connect(
            host=self.host,
            user=self.username,
            passwd=self.password,
            db=self.database,
            port=self.port
        )

    def query(self, query_str):
        if type(query_str) in (list, tuple):
            query_list = query_str
        else:
            query_list = [query_str]

        self.query_count = 0
        for q in query_list:
            cursor = self.db.cursor()
            cursor.execute(q)
            if q.startswith("INSERT"):
                self.db.commit()
            _ = cursor.fetchall()
            self.query_count += 1


    def disconnect(self):
        self.db.close()

    def get_adapter_name(self):
        return 'mysql'
