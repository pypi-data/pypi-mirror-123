# -*- coding: utf-8 -*-
import time
import threading
import os

import numpy as np
from qpython import qconnection

from pyconn import logger
from pyconn.db.advancedqreader import AdvancedQReader


class Server:
    def __init__(self, **kwargs):
        self.name = ""
        self.host = ""
        self.port = 0
        self.username = ""
        self.password = ""
        self.pandas = False
        self.callback = None
        self.__dict__.update(kwargs)


class MonitorThread(threading.Thread):
    def __init__(self):
        super(MonitorThread, self).__init__()
        self.pool = ConnectionPool()

    def run(self):
        while True:
            if self.pool is not None:
                for server_name, handle in self.pool.handle_dict.items():
                    if handle.is_connected:
                        try:
                            handle.sendSync('til 1')
                        except ConnectionError:
                            logger.error(server_name + ' heartbeat failed')
                            handle.is_connected = False
                    else:
                        handle = self.pool.create_connection(handle.server)
                        if handle is not None and handle.is_connected:
                            logger.info('Reconnected to {}'.format(handle.server.name))
                            callback = handle.server.callback
                            if callable(callback):
                                callback()
                time.sleep(30)


class QHandle(qconnection.QConnection):
    def __init__(self, server):
        super(QHandle, self).__init__(host=server.host, port=server.port, username=server.username,
                                      password=server.password, pandas=server.pandas, reader_class=AdvancedQReader)
        self.is_connected = False
        self.server = server
        self.lock = threading.Lock()

    def is_valid(self):
        pass


class ConnectionPool:
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls, server_list=None):
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super(ConnectionPool, cls).__new__(cls)
                    cls._instance.handle_dict = {}
                    cls.start_monitor_thread()
        return cls._instance

    def __init__(self, server_list=None):
        if server_list is None:
            return
        for server in server_list:
            if server.name not in self._instance.handle_dict.keys():
                self.create_connection(server)

    @staticmethod
    def start_monitor_thread():
        thread = MonitorThread()
        thread.start()

    def create_connection(self, server):
        conn = QHandle(server)
        self.handle_dict[server.name] = conn
        try:
            conn.open()
        except ConnectionError:
            logger.error('Connect to {} failed'.format(server.name))
            conn.is_connected = False
        else:
            conn.is_connected = True
        return conn

    def get_connection(self, server):
        return self.handle_dict.get(server.name)


class Query:

    def __init__(self, server):
        self.pool = ConnectionPool()
        self.server = server
        self.conn = None

    def query_sync(self, query, *parameters, **options):
        result = None
        self.conn = self.pool.get_connection(self.server)
        if self.conn is not None and self.conn.is_connected:
            try:
                with self.conn.lock:
                    result = self.conn.sendSync(query, *parameters, **options)
            except Exception as e:
                log_str = "DB[{}] error: {}, query: {}, params: {}, options: {}"
                logger.error(log_str.format(self.server.name, e.args[0], query, parameters, options))
            return result

    def to_sym(self, s):
        return np.string_(s, encoding='utf-8')

    def to_sym_list(self, l):
        """
        convert np.array[object] to np.array[np.string_ with utf-8]
        :param l: df['col'].values
        :return: np.string_ with utf-8
        """
        return np.char.encode(l.astype(np.unicode_), encoding='utf-8')

    def to_date(self, l):
        return l.astype('M8[D]')
