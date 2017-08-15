from unittest import TestCase

from april import Model
from april.tipes import listof
from april.exceptions import ValidationError


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

    def test_usage_2(self):
        class AlbumModel(Model):
            name = str

        class SongModel(Model):
            name = str
            album = AlbumModel

        album = AlbumModel(**{'name': 'years'})
        song = SongModel(name='i love you', album=album)
        self.assertEqual(song.album.name, 'years')

    def test_usage_3(self):
        class ArtistModel(Model):
            name = str

        class SongModel(Model):
            name = str
            artists = listof(ArtistModel)

        artists = [ArtistModel(**{'name': u'谭咏麟'}),
                   ArtistModel(**{'name': u'周华健'})]

        song = SongModel(name=u'朋友', artists=artists)
        self.assertEquals(song.artists[0].name, u'谭咏麟')

#     def test_usage_4(self):
#         class ArtistModel(Model):
#             name = str
#
#         class SongModel(Model):
#             name = str
#             artists = listof(ArtistModel)
#
#         artists = [{'name': u'谭咏麟'}, {'name': u'周华健'}]
#
#         song = SongModel(name=u'朋友', artists=artists)
#         self.assertEquals(song.artists[0].name, u'谭咏麟')


    def test_init_with_wrong_type(self):
        class UserModel(Model):
            name = str

        self.assertRaises(ValidationError, UserModel, name=0)

    def test_lack_of_required_field(self):

        class UserModel(Model):
            name = str

        self.assertRaises(ValidationError, UserModel, age=0)

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

        self.assertRaises(ValidationError, UserModel, phones=['1', '2'])

    def test_validate_not_a_field_attr(self):
        class UserModel(Model):
            name = str
            msg = 'hello world'

        UserModel.validate({'name': 'lucy', 'strict': True})

    def test_inherit_usage(self):

        class CarModel(Model):
            trade_mark = str

        class BaseUserModel(Model):
            name = str
            car = CarModel

        class UserModel(BaseUserModel):
            age = int

        user = UserModel(name='lucy',
                         age=11,
                         car=CarModel(**{'trade_mark': 'benzi'}))
        self.assertEqual(user.name, 'lucy')
        self.assertEqual(user.car.trade_mark, 'benzi')

    def test_inherit_optional_feilds(self):

        class BaseUserModel(Model):
            name = str

            _optional_fields = ['name']

        class UserModel(BaseUserModel):
            age = int

        UserModel(age=11)

    def test_inherit_override_optional_feilds(self):
        class BaseUserModel(Model):
            name = str

            _optional_fields = ['name']

        class UserModel(BaseUserModel):
            age = int

            _optional_fields = ['age']

        self.assertRaises(ValidationError, UserModel, age=11)

    def test_init_with_optional_fields(self):
        class User(Model):
            name = str
            age = int

            _optional_fields = ['age']

        user = User(name='Tom', age=10)
        self.assertTrue(user.age, 10)

    def test_init_with_model(self):
        class User(Model):
            name = str

        user = User(name='seven')
        self.assertTrue(user.name, 'seven')

        user2 = User(user)
        self.assertTrue(user2.name, 'seven')

        user3 = User(user, name='mos')
        self.assertTrue(user3.name, 'mos')
