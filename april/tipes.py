# -*- coding: utf-8 -*-

import inspect
from .models import Model
from .exceptions import ValidationError


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
    def deserialize(cls, value):
        """deserialize value to listof nested type object

        Example::

            class ArtistModel(Model):
                name = str

            listof_ArtistModel = listof(ArtistModel)
            artists = llistof_ArtistModel.deserialize([{'name': 'hybrid'}])
        """
        cls.validate(value)

        if issubclass(cls._ntype, Model):
            return [cls._ntype.deserialize(each) for each in value]

        serialized_data = []
        for each in value:
            serialized_data.append(cls._ntype(each))
        return serialized_data

    @classmethod
    def validate(cls, data):
        if not isinstance(data, list):
            raise ValidationError('data should be a list')

        for each in data:
            if issubclass(cls._ntype, Model):
                cls._ntype.validate(each)
                continue

            if not isinstance(each, cls._ntype):
                raise ValidationError("list element should be '%s'" % cls._ntype)

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
