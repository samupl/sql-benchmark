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

    def disconnect(self):
        self.db.close()

    def get_adapter_name(self):
        return 'mysql'

    def run_query(self, query_str):
        cursor = self.db.cursor()
        cursor.execute(query_str)
        if query_str.startswith("INSERT"):
            self.db.commit()
        _ = cursor.fetchall()
