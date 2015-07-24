# -*- coding: utf-8 -*-
from sqlbenchmark.adapters import AdapterFactory


class SQLBenchmark(object):

    def __init__(self):
        self.adapter_class = None

    def set_adapter(self, name):
        self.adapter_class = AdapterFactory.create_adapter(name)
