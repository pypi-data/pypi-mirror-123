import logging
import numpy

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s',
                              '%Y-%m-%d %H:%M:%S')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


def to_sym(str_):
    return numpy.string_(str_, encoding='utf-8')


def to_sym_list(list_):
    return numpy.char.encode(numpy.array(list_).astype(numpy.unicode_), encoding='utf-8')


def to_date(date_):
    return numpy.datetime64(date_).astype('M8[D]')
