# -*- coding: utf-8 -*-

import inspect

from .utils import is_nested_type
from .exceptions import ValidationError


class ModelMeta(type):

    def __new__(cls, name, bases, attrs):
        _fields = list()

        # get inherited fileds
        for base in bases:
            inherited_fields = base._fields if hasattr(base, '_fields') else []
            _fields.extend(inherited_fields)

        # save fields metainfo in klass._fields
        class_attrs = {}
        for key, field_type in attrs.items():
            if inspect.isclass(field_type):
                _fields.append((key, field_type))
            else:
                class_attrs[key] = field_type

        _fields = list(set(_fields))

        # ``_optional_fields`` should be a list or tuple
        _optional_fields = attrs.get('_optional_fields', [])
        if _optional_fields is not None:
            if not isinstance(_optional_fields, (list, tuple)):
                raise TypeError('_optional_fields should be a list')

        if not _optional_fields:
            # try to use parent's _optional_fields
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
        assert user.name == 'xxx'

        user2 = UserModel(user)
        assert user2.name = 'xxx'
    """
    def __init__(self, model=None, **kwargs):
        context = dict()
        fields_dict = dict(self._fields)

        if model is not None:
            for field_name, _ in self._fields:
                context[field_name] = getattr(model, field_name)

        context.update(kwargs)
        self.validate(context)

        for key, value in context.items():
            if key in fields_dict:
                self.__dict__[key] = fields_dict[key](value)
            else:
                self.__dict__[key] = value

        # set all optional_fields value as None
        for field_name in self._optional_fields:
            if field_name not in self.__dict__:
                self.__dict__[field_name] = None

    @classmethod
    def validate(cls, data):

        # check if all required fields exists
        fields_dict = dict(cls._fields)
        _optional_fields = cls._optional_fields
        for key, field_type in fields_dict.items():
            if key not in _optional_fields and key not in data:
                raise ValidationError('field:"{}" is required'.format(key))

        # validate each field
        for name, value in data.items():
            if cls.is_field(name):
                cls.validate_field(name, value)

    @classmethod
    def validate_field(cls, name, value):
        """validate the type of field value"""
        fields_dict = dict(cls._fields)
        field_type = fields_dict[name]
        if not any([is_nested_type(field_type) and field_type.is_instance(value),
                    isinstance(value, field_type)]):
            raise ValidationError('the value of filed:"{}" should be "{}", got {}'
                                  .format(name, field_type, type(value)))
    @classmethod
    def is_field(cls, name):
        """check if a attribute belongs to model fields"""
        return name in dict(cls._fields)
