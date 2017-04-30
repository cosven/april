from unittest import TestCase

from april import Model


class ModelTest(TestCase):

    def test_usage(self):

        class UserObj(Model):
            name = str

        user = UserObj(name='xxx')
        import ipdb
        ipdb.set_trace()
        self.assertEqual(user.name, 'xxx')
