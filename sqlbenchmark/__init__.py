# -*- coding: utf-8 -*-
from sqlbenchmark.adapters import AdapterFactory
from sqlbenchmark.worker import BenchmarkWorker


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
        self.process_count = 1

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
        for i in range(self.process_count):
            process = BenchmarkWorker()
            # Copy data to processes
            process.adapter_class = self.adapter_class
            process.host = self.host
            process.database = self.database
            process.user = self.user
            process.password = self.password
            process.port = self.port
            process.benchmark = self.benchmark

            self.process_list.append(process)
            process.start()

    def init_database(self):
        self.adapter = self.adapter_class(
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.password,
            database=self.database
        )
        self.adapter.connect()

    def cleanup_database(self):
        pass

    def run_benchmark(self):
        self.start_processes()
