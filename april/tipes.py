# -*- coding: utf-8 -*-

import inspect


__all__ = ('listof')


def _listof_class_contructor(cls, obj_list):
    """constructor of listof_class"""

    if not isinstance(obj_list, list):
        raise TypeError('obj_list should be a list')

    for obj in obj_list:
        if not isinstance(obj, cls._ntype):
            raise TypeError('object must be a %s' % cls._ntype.__name__)

    return obj_list


class listof:
    """listof type

    Usage::

        listof_str = listof(str)
        str_list = listof_str(['hello', 'world'])
    """

    def __new__(cls, ntype):
        if not inspect.isclass(ntype):
            raise TypeError('ntype must be a class')
        return type('listof_' + ntype.__name__, (), {
            '_ntype': ntype,
            '__new__': _listof_class_contructor
        })
