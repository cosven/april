# -*- coding: utf-8 -*-

from six import with_metaclass


class StructMeta(type):

    def __new__(cls, name, bases, attrs):
        _fields = list()

        # get inherited fileds
        for base in bases:
            inherited_fields = getattr(base, '_fields', [])
            _fields.extend(inherited_fields)

        _fields.extend(attrs.get('_fields', []))
        _fields = list(set(_fields))

        attrs['_fields'] = _fields

        klass = type.__new__(cls, name, bases, attrs)
        return klass


class Struct(object, with_metaclass(StructMeta)):
    """base class for data models

    Usage::

        from april import Struct

        class User(Struct):
            _fields = ['name', 'title']

        user = UserModel(name='xxx')
        assert user.name == 'xxx'

        user2 = UserModel(user)
        assert user2.name = 'xxx'
    """

    def __init__(self, obj=None, **kwargs):
        for field in self._fields:
            setattr(self, field, getattr(obj, field, None))

        for k, v in kwargs.items():
            if k in self._fields:
                setattr(self, k, v)
