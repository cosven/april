# -*- coding: utf-8 -*-

import inspect

from .utils import is_nested_type
from .exceptions import ValidationError


class ModelMeta(type):
    """metaclass for Models"""

    def __new__(cls, name, bases, attrs):
        _fields = list()

        # save fields metainfo in klass._fields
        for key, ftype in attrs.items():
            if inspect.isclass(ftype):
                _fields.append((key, ftype))

        # validate ``_optional_fields`` value type
        _optional_fields = attrs.get('_optional_fields', [])
        if _optional_fields is not None:
            if not isinstance(_optional_fields, (list, tuple)):
                raise TypeError('_optional_fields should be a list')
        # pop field from attributes
        for key, ftype in _fields:
            attrs.pop(key)

        klass = type.__new__(cls, name, bases, attrs)
        klass._fields = _fields
        klass._optional_fields = _optional_fields
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
        super().__init__()

        fields_dict = dict(self._fields)

        # validate required field
        _optional_fields = self._optional_fields
        for key, ftype in fields_dict.items():
            if key not in _optional_fields and key not in kwargs:
                raise ValidationError("data missing required field: '%s'" % key)

        # deserialize each field
        for key, value in kwargs.items():

            ftype = fields_dict[key]

            # if field type is subclass of Model, convert the value to
            # instance of the subclass
            if issubclass(ftype, Model):
                value = ftype.deserialize(value)

            if is_nested_type(ftype):
                value = ftype.deserialize(value)
            else:
                if not isinstance(value, ftype):
                    raise TypeError("'%s' should be '%s'" % (value, ftype.__class__))

            self.__dict__[key] = value

        self._data = kwargs

    @classmethod
    def deserialize(cls, data):
        if not isinstance(data, dict):
            raise TypeError("'data' should be a dict")
        return cls(**data)

    def serialize(self):
        return self._data
