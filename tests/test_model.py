from unittest import TestCase

from april import Model


class TestModel(TestCase):

    def test_usage(self):

        class UserModel(Model):
            name = str

        # user = UserModel(name='Tom')
        # self.assertEqual(user.name, 'Tom')
