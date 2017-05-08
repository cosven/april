# -*- coding: utf-8 -*-

import inspect


__all__ = ('listof')


class BaseNestedType(object):
    def __new__(cls, obj_list):
        if not isinstance(obj_list, list):
            raise TypeError('obj_list should be a list')

        for obj in obj_list:
            if not isinstance(obj, cls.get_ntype()):
                raise TypeError('object must be a %s' % cls._ntype.__name__)

        return obj_list

    @classmethod
    def validate_instance(cls, instance):
        """check if the type of instance match with cls"""
        if not isinstance(instance, list):
            raise TypeError('instance should be a list')
        for obj in instance:
            ntype = cls.get_ntype()
            if not isinstance(obj, ntype):
                raise TypeError("list element should be '%s'" % ntype.__class__)

    @classmethod
    def get_ntype(cls):
        return cls._ntype


class listof:
    """listof type creator

    Usage::

        listof_str = listof(str)
        str_list = listof_str(['hello', 'world'])
    """

    def __new__(cls, ntype):
        if not inspect.isclass(ntype):
            raise TypeError('ntype must be a class')
        return type('listof_' + ntype.__name__, (BaseNestedType, ), {
            '_ntype': ntype,
        })
