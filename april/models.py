# -*- coding: utf-8 -*-

import inspect

from .utils import is_nested_type
from .exceptions import ValidationError


class ModelMeta(type):
    """metaclass for Models"""

    def __new__(cls, name, bases, attrs):
        _fields = list()

        for base in bases:
            tmp_fields = base._fields if hasattr(base, '_fields') else []
            _fields.extend(tmp_fields)

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
            if key in attrs:  # if key is not inherited from parent class
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

        self.validate(kwargs)

        # deserialize each field
        for key, value in kwargs.items():
            if self._is_field(key):
                value = self.deserialize_field(key, value)
            self.__dict__[key] = value

        self._data = kwargs

    @classmethod
    def deserialize(cls, data):
        cls.validate(data)
        return cls(**data)

    def serialize(self):
        return self._data

    @classmethod
    def validate(cls, data):
        if not isinstance(data, dict):
            raise ValidationError(
                "{0}: data should be a dict, but it is a {1}".foramt(cls.__name__, type(data)))
        # validate required field
        fields_dict = dict(cls._fields)
        _optional_fields = cls._optional_fields
        for key, ftype in fields_dict.items():
            if key not in _optional_fields and key not in data:
                raise ValidationError("data missing required field: '%s'" % key)

        for name, value in data.items():
            if cls._is_field(name):
                cls.validate_field(name, value)

    @classmethod
    def deserialize_field(cls, name, value):
        fields_dict = dict(cls._fields)
        ftype = fields_dict[name]

        # if field type is subclass of Model, convert the value to
        # instance of the subclass
        if issubclass(ftype, Model):
            value = ftype.deserialize(value)
        if is_nested_type(ftype):
            value = ftype.deserialize(value)
        return value

    @classmethod
    def validate_field(cls, name, value):
        fields_dict = dict(cls._fields)
        if not cls._is_field(name):
            return

        ftype = fields_dict[name]

        if issubclass(ftype, Model):
            ftype.validate(value)
            return

        if is_nested_type(ftype):
            ftype.validate(value)
        else:
            if not isinstance(value, ftype):
                raise ValidationError("'%s' should be '%s'" % (value, ftype.__class__))

    @classmethod
    def _is_field(cls, name):
        return name in dict(cls._fields)

    def __setattr__(self, name, value):
        """modify self._data when field attr changes"""
        object.__setattr__(self, name, value)
