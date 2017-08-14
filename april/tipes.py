# -*- coding: utf-8 -*-

import inspect
from .exceptions import ValidationError


__all__ = ('listof')


class BaseContainerType(object):
    def __new__(cls, obj_list):
        if not isinstance(obj_list, list):
            raise TypeError('obj_list should be a list')

        for obj in obj_list:
            if not isinstance(obj, cls.nested_type):
                raise TypeError('object must be a %s' % cls.nested_type.__name__)

        return obj_list

    @classmethod
    def is_instance(cls, data):
        if not isinstance(data, (list, set, tuple)):
            raise ValidationError('value should be a list set or tuple, got {}'
                                  .format(type(data)))

        for each in data:
            if not isinstance(each, cls.nested_type):
                raise ValidationError("nested element should be '%s'" % cls.nested_type)


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
