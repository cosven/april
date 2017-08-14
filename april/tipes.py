# -*- coding: utf-8 -*-

import inspect
from .exceptions import ValidationError


__all__ = ('listof')


class BaseContainerType(object):
    def __new__(cls, objects):
        if not isinstance(objects, (list, set, tuple)):
            raise TypeError('only list set or tuple can be container type, got {}'
                            .format(type(objects)))

        for obj in objects:
            if not isinstance(obj, cls.nested_type):
                raise TypeError('object must be a %s' % cls.nested_type.__name__)

        return objects

    @classmethod
    def is_instance(cls, data):
        if not isinstance(data, (list, set, tuple)):
            return False

        for each in data:
            if not isinstance(each, cls.nested_type):
                return False
        return True


class listof:
    """list container type

    Usage::

        listof_str = listof(str)
        str_list = listof_str(['hello', 'world'])
    """

    def __new__(cls, nested_type):
        if not inspect.isclass(nested_type):
            raise TypeError('nested_type must be a class')
        return type('listof_' + nested_type.__name__, (BaseContainerType, ), {
            'nested_type': nested_type,
        })
