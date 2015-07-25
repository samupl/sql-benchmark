# -*- coding: utf-8 -*-
from multiprocessing import Process, Event
import time
from sqlbenchmark.query_loader import QueryLoader


class BenchmarkWorker(Process):

    # region constructor
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        super(BenchmarkWorker, self).__init__(group, target, name, args, kwargs)

        self.port = None
        self.user = None
        self.password = None
        self.database = None
        self.host = None

        self.queue = None
        self.adapter_class = None
        self.adapter = None
        self.benchmark = None
        self.query_loader = None
        self.query_list = []
        self.query_count = 0
        self.exit = Event()
    # endregion

    def initialize(self):
        self.adapter = self.adapter_class(
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.password,
            database=self.database
        )
        self.query_loader = QueryLoader(self.benchmark, self.adapter.get_adapter_name())
        self.query_list = self.query_loader.list_queries()

    def run(self):
        self.initialize()
        self.adapter.connect()

        while not self.exit.is_set():
            for q in self.query_list:
                if self.exit.is_set():
                    break
                query = self.query_loader.get_query(q)
                self.adapter.query(query)
                self.query_count = self.adapter.query_count
                # Clear the queue - only one item should be there
                if not self.queue.empty():
                    self.queue.get()
                self.queue.put(self.query_count)

    def stop(self):
        self.exit.set()
