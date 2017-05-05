# -*- coding: utf-8 -*-

from copy import deepcopy
import inspect


class ModelMeta(type):
    """metaclass for Models"""

    def __new__(cls, name, bases, attrs):
        _fields = list()
        attrs_bak = deepcopy(attrs)

        # save fields metainfo in klass._fields
        for key, ftype in attrs.items():
            if inspect.isclass(ftype):
                attrs_bak.pop(key)
                _fields.append((key, ftype))

        _optional_fields = attrs.get('_optional_fields')
        if _optional_fields is not None:
            if not isinstance(_optional_fields, (list, tuple)):
                raise TypeError('_optional_fields should be a list')

        klass = type.__new__(cls, name, bases, attrs_bak)
        klass._fields = _fields
        return klass


class Model(metaclass=ModelMeta):
    """base class for data models

    Usage::

        from april import Model

        class UserModel(Model):
            name = str
            title = str

            _optional_fields = ('title')

        user = UserModel(name='xxx')
    """
    def __init__(self, **kwargs):
        fields_dict = dict(self._fields)
        for key, value in kwargs.items():
            if key not in fields_dict:
                raise TypeError("__init__ got an unexpected keyword argument '%s'" % key)

            if not isinstance(value, fields_dict[key]):
                raise TypeError("'%s' should be a %s" % (key, fields_dict[key]))

            self.__dict__[key] = value
