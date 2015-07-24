# -*- coding: utf-8 -*-
from sqlbenchmark.adapters.mysql import MySQLBenchmarkAdapter


class AdapterFactory(object):

    adapter_map = {
        'mysql': MySQLBenchmarkAdapter
    }

    @staticmethod
    def create_adapter(name):
        adapter_class = AdapterFactory.adapter_map.get(name)
        if adapter_class is not None:
            return adapter_class

        raise KeyError("Adapter {name} is not supported".format(name=name))
