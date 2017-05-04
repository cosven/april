# -*- coding: utf-8 -*-


class ModelMeta(type):
    """metaclass for Models"""

    def __new__(cls, name, bases, attrs):
        klass = type.__new__(cls, name, bases, attrs)

        klass.fields = [(name, ftype) for key, ftype in attrs.items()
                        if type(ftype) == type]
        return klass


class Model(metaclass=ModelMeta):
    """base class for data models

    Usage::

        from april import Model

        class UserModel(Model):
            name = str
            title = str

            _optional_fields = ('name')

        user = UserModel(name='xxx')
    """

    def __init__(self, *args, **kwargs):
        pass
