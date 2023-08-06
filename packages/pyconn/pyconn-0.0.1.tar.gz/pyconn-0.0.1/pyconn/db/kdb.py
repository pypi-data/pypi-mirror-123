import numpy as np
from qpython import qconnection
from .advancedqreader import AdvancedQReader

from pyconn import logger


class Server:
    def __init__(self):
        self.name = ""
        self.host = ""
        self.port = 0
        self.username = ""
        self.password = ""
        self.pandas = False

    def to_string(self):
        return self.name


class KDB:
    def __init__(self, server):
        self.server_name = server.name
        self.q = qconnection.QConnection(host=server.host, port=server.port, username=server.username,
                                         password=server.password,
                                         pandas=server.pandas,
                                         reader_class=AdvancedQReader)

    def get_conn(self):
        return self.q

    def close_conn(self):
        self.q.close()

    def query_sync(self, query, *parameters, **options):
        try:
            self.q.open()
            return self.q.sendSync(query, *parameters, **options)
        except ConnectionError as e:
            log_str = "DB[{}] error: {}, query: {}, params: {}, options: {}"
            logger.error(log_str.format(self.server_name, e.args[1], query, parameters, options))
        finally:
            self.close_conn()

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
