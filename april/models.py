# -*- coding: utf-8 -*-

from copy import deepcopy
import inspect

from .utils import is_nested_type
from .class_registry import register, get_class


class ModelMeta(type):
    """metaclass for Models"""

    def __init__(self, name, bases, attrs):
        super(ModelMeta, self).__init__(name, bases, attrs)
        register(name, self)

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
        register(name, klass)
        return klass


class Model(object, metaclass=ModelMeta):
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

            ftype = fields_dict[key]

            # if field type is subclass of Model, convert the value to
            # instance of the subclass
            if issubclass(ftype, Model):
                value = ftype.load(value)

            if is_nested_type(ftype):
                ftype.validate_instance(value)
                ntype = ftype.get_ntype()
                if issubclass(ntype, Model):
                    value = [ntype.load(x) for x in value]
            else:
                if not isinstance(value, ftype):
                    raise TypeError("'%s' should be '%s'" % (value, ftype.__class__))

            self.__dict__[key] = value

    @classmethod
    def load(cls, data):
        if not isinstance(data, dict):
            raise TypeError("'data' should be a dict")
        return cls(**data)
