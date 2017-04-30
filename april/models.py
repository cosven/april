# -*- coding: utf-8 -*-


class ModelMeta(type):
    """metaclass for Models"""

    def __new__(cls, name, bases, attrs):
        """class constructor"""
        new_class = type.__new__(cls, name, bases, attrs)
        return new_class


class Model(metaclass=ModelMeta):
    """

    Usage::

        from april import Model
        class UserModel(Model):
            name = str

        user = UserModel(name='xxx')
    """

    def __init__(self, *args, **kwargs):
        pass
