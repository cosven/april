# -*- coding: utf-8 -*-

import inspect

from .utils import is_nested_type
from .exceptions import ValidationError


class ModelMeta(type):
    """metaclass for Models"""

    def __new__(cls, name, bases, attrs):
        _fields = list()

        # get parent fileds
        for base in bases:
            tmp_fields = base._fields if hasattr(base, '_fields') else []
            _fields.extend(tmp_fields)

        # save fields metainfo in klass._fields
        class_attrs = {}
        for key, ftype in attrs.items():
            if inspect.isclass(ftype):
                _fields.append((key, ftype))
            else:
                class_attrs[key] = ftype

        _fields = list(set(_fields))

        # validate ``_optional_fields`` value type
        _optional_fields = attrs.get('_optional_fields', [])
        if _optional_fields is not None:
            if not isinstance(_optional_fields, (list, tuple)):
                raise TypeError('_optional_fields should be a list')

        # if _optional_fields is not specified, try to use parent's _optional_fields
        if not _optional_fields:
            for base in reversed(bases):
                if hasattr(base, '_optional_fields'):
                    _optional_fields.extend(base._optional_fields)

        klass = type.__new__(cls, name, bases, class_attrs)
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

        self.validate(kwargs)

        for key, value in kwargs.items():
            self.__dict__[key] = value

        # set all optional_fields value as None
        for field in self._optional_fields:
            self.__dict__[field] = None

        self._data = kwargs

    @classmethod
    def validate(cls, data):
        if not isinstance(data, dict):
            raise ValidationError(
                "{0}: data should be a dict, but it is a {1}".format(cls.__name__, type(data)))
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
