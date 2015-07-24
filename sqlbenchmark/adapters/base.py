# -*- coding: utf-8 -*-


class BaseAdapter(object):

    def connect(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError

    def query(self):
        raise NotImplementedError
