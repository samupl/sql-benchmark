# -*- coding: utf-8 -*-
from Queue import Empty
from multiprocessing import Queue
import threading
import time
from sqlbenchmark.worker import BenchmarkWorker


def threaded(fn):
    def wrapper(*args, **kwargs):
        th = threading.Thread(target=fn, args=args, kwargs=kwargs)
        th.daemon = True
        th.start()
    return wrapper


class ProcessInformationManager(object):

    def __init__(self):
        self.process_list = []
        self.new_process_attributes = {}
        self.num_processes = None
        self.queues = []
        self.running = True
        self.process_info_thread = None
        self.qps = []

    @threaded
    def run_info_thread(self):
        while self.running:
            time.sleep(1)
            i = 0

            for q in self.queues:
                try:
                    query_count = q.get_nowait()
                except Empty:
                    pass
                else:
                    #old_query_count = self.qps[i]
                    # qps = query_count - old_query_count # diff = number of queries done during 1s
                    # print "qps:", qps, " old:", old_query_count, " current:", query_count
                    self.qps[i] = query_count

                self.process_list[i].reset_counter()
                i += 1

    def start_processes(self):
        for p in range(self.num_processes):
            queue = Queue()

            self.queues.append(queue)
            self.qps.append(0)

            process = BenchmarkWorker()
            process.queue = queue
            # Copy data to processes
            for key in self.new_process_attributes:
                setattr(process, key, self.new_process_attributes[key])

            self.process_list.append(process)
            process.start()

    def start(self):
        self.run_info_thread()
        self.start_processes()
        self.display_nice_output()

    def stop(self):
        self.running = False
        for p in self.process_list:
            p.stop()

    @threaded
    def display_nice_output(self):
        while self.running:
            time.sleep(1)
            print(chr(27) + "[2J")
            i = 0
            total_qps = 0
            for qps in self.qps:
                print "Worker {id:>4}:   {qps:>10} queries/sec".format(id=i, qps=qps)
                i += 1
                total_qps += qps

            print "--------"
            print "Total: {qps:>18} queries/sec".format(qps=total_qps)
