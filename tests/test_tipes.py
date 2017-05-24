from unittest import TestCase

from april.exceptions import ValidationError
from april.tipes import listof


class TestListof(TestCase):

    def test_listof(self):
        listof_str = listof(str)
        str_list = ['hello', 'world']
        str_list_new = listof_str(str_list)
        self.assertEqual(str_list, str_list_new)

    def test_listof_2(self):
        """listof initialized with a object which is not a class"""
        listof_str = listof(str)
        self.assertRaises(TypeError, listof_str, [1, 2])

    def test_listof_3(self):
        """when datatype is not a class"""
        self.assertRaises(TypeError, listof, 1)

    def test_listof_4(self):
        """when listof_class initialized with a object which is not a list"""
        listof_str = listof(str)
        self.assertRaises(TypeError, listof_str, 'name')

    def test_listof_5(self):
        listof_str = listof(str)
        self.assertRaises(ValidationError, listof_str.deserialize, 'name')

    def test_isinstance(self):
        listof_str = listof(str)
        listof_str(['hello', 'world'])
