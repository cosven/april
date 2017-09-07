# -*- coding: utf-8 -*-

from april import Struct


def test_usage():
    class User(Struct):
        _fields = ['name', 'age']

    user = User(name='Tom', age=10)
    assert user.name == 'Tom'
    assert user.age == 10


def test_inherit():
    class Lang(Struct):
        _fields = ['name']

    class Python(Lang):
        _fields = ['author']

    assert 'name' in Python._fields
    p = Python(name='Python', author='Guido')
    assert p.author == 'Guido'
    assert p.name == 'Python'


def test_init_with_obj():
    class User(Struct):
        _fields = ['name']

    u1 = User(name='haha')
    u2 = User(u1)
    assert u2.name == 'haha'


def test_customize_init():
    class User(Struct):
        _fields = ['name']

        def __init__(self, **kwargs):
            super(User, self).__init__(**kwargs)

    class VIP(User):
        _fields = ['level']

        def __init__(self, **kwargs):
            super(VIP, self).__init__(**kwargs)

    u = VIP(name='haha', level=1)
    assert u.name == 'haha'
    assert u.name == 'haha'


def test_mix():
    print('test-mix')
    class User(Struct):
        _fields = ['name', 'age', 'birthday']

    user = User(name='lucy', age=20, birthday='2017')

    class VIP(User):
        _fields = ['level']

    vip = VIP(user, level=1)

    assert vip.name == 'lucy'
    assert vip.level == 1
