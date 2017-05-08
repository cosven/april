from unittest import TestCase

from april import Model
from april.tipes import listof
from april.class_registry import get_class


class TestModel(TestCase):

    def test_usage(self):

        class UserModel(Model):
            name = str
            phones = list
            age = int

            _optional_fields = ('age', )

        user = UserModel(name='Tom', phones=[123, 234])
        self.assertEqual(user.name, 'Tom')
        self.assertEqual(user.phones, [123, 234])

    def test_init_with_wrong_type(self):
        class UserModel(Model):
            name = str

        self.assertRaises(TypeError, UserModel, name=0)

    def test_init_with_unknown_field(self):

        class UserModel(Model):
            name = str

        self.assertRaises(TypeError, UserModel, age=0)

    def test_optional_field_not_a_tuple_or_list(self):

        def define_model():
            class UserModel(Model):
                name = str

                _optional_fields = ('name')

        self.assertRaises(TypeError, define_model)

    def test_composite_filed_success(self):

        class UserModel(Model):
            phones = listof(int)

        UserModel(phones=[1, 2])

    def test_composite_filed_failed(self):
        class UserModel(Model):
            phones = listof(int)

        self.assertRaises(TypeError, UserModel, phones=['1', '2'])
