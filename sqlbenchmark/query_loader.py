# -*- coding: utf-8 -*-
import pprint
import os
import sqlparse


class QueryLoader(object):

    query_cache = {}

    def __init__(self, benchmark=None, adapter_name=None):
        self.benchmark = benchmark
        self.adapter_name = adapter_name

    def get_base_path(self):
        return os.path.join('benchmarks', self.benchmark)

    def load_file(self, name, directory):
        fp = open(os.path.join(self.get_base_path(), directory, self.adapter_name + '_' + name + '.sql'), 'r')
        return fp

    def get_query(self, name):
        if name in self.query_cache:
            return self.query_cache.get(name)

        fp = self.load_file(name, 'queries')
        query = fp.read()
        queries = sqlparse.split(query)
        ret_queries = [q.strip() for q in queries if q.strip()]
        self.query_cache[name] = ret_queries
        return ret_queries

    def get_schema(self, name):
        fp = self.load_file(name, 'schemas')
        query = fp.read()
        # queries = query.split(';')
        queries = sqlparse.split(query)
        ret_queries = [q.strip() for q in queries if q.strip()]
        return ret_queries

    def list_queries(self):
        query_path = os.path.join(self.get_base_path(), 'queries')
        files = os.listdir(query_path)
        return_files = []
        for f in files:
            if f.startswith(self.adapter_name + "_") and f.endswith(".sql"):
                file_name = f[len(self.adapter_name + "_"):-len('.sql')]
                return_files.append(file_name)

        return return_files
