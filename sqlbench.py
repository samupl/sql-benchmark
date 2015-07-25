# -*- coding: utf-8 -*-
from sqlbenchmark import SQLBenchmark
from sqlbenchmark.query_loader import QueryLoader

benchmark = SQLBenchmark()
benchmark.set_adapter('mysql')
benchmark.set_connection_data(
    host='localhost',
    user='benchmark',
    password='benchmark',
    database='benchmark'
)
benchmark.set_benchmark('blog')
benchmark.run_benchmark()
