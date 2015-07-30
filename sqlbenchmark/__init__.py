# -*- coding: utf-8 -*-
from sqlbenchmark.adapters import AdapterFactory
from sqlbenchmark.process_info import ProcessInformationManager
from sqlbenchmark.query_loader import QueryLoader


class SQLBenchmark(object):

    # region constructor
    def __init__(self, adapter_name=None):
        # Adapter & test configuratoin
        self.adapter_class = None
        self.adapter = None
        self.benchmark = None

        # Database configuration
        self.host = None
        self.user = None
        self.password = None
        self.database = None
        self.port = None

        # Workers
        self.process_list = []
        self.process_count = 20
        self.process_manager = None

        # QueryLoader
        self.ql = None

        if adapter_name is not None:
            self.set_adapter(adapter_name)
    # endregion

    def set_adapter(self, name):
        self.adapter_class = AdapterFactory.create_adapter(name)

    def set_benchmark(self, name):
        self.benchmark = name

    def set_connection_data(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def start_processes(self):
        self.process_manager = ProcessInformationManager()
        self.process_manager.num_processes = self.process_count
        self.process_manager.new_process_attributes = {
            'adapter_class': self.adapter_class,
            'host': self.host,
            'database': self.database,
            'user': self.user,
            'password': self.password,
            'port': self.port,
            'benchmark': self.benchmark
        }
        self.process_manager.start()

    def init_database(self):
        self.adapter = self.adapter_class(
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.password,
            database=self.database
        )
        self.adapter.connect()
        self.ql = QueryLoader(self.benchmark, self.adapter.get_adapter_name())
        schema_queries = self.ql.get_schema('init')
        self.adapter.query(schema_queries)

    def cleanup_database(self):
        schema_queries = self.ql.get_schema('destroy')
        self.adapter.query(schema_queries)

    def run_benchmark(self):
        self.init_database()
        self.start_processes()
        raw_input()
        self.process_manager.stop()
        self.cleanup_database()
