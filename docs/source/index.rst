Welcome to april's documentation!
=================================

simplified data deserialization

`april` do following things:

- simple type validation
- object serialization and data deserialization

Usage
-----

simple usage
""""""""""""

.. sourcecode:: python

    from datetime import datetime
    from april import Model


    class UserModel(Model):
        name = str
        age = int
        birthday = datetime

    data = dict(name='lucy', age=20, birthday=datetime.now())
    user = UserModel()
    # user = UserModel.deserialize(data)

    user.serialize()

complex usage
"""""""""""""

.. sourcecode:: python

    from april import Model
    from april.tipes import listof


    class ArtistModel(Model):
        name = str


    class AlbumModel(Model):
        name = str


    class SongModel(Model):
        title = str
        album = AlbumModel
        artists = listof(ArtistModel)


    data = {
        'title': 'in the end',
        'album': {
            'name': 'in the end'
        },
        'artists': [
            {
                'name': 'Linkin Park'
            },
            {
                'name': 'Fort Minor'
            }
        ]
    }

    song = SongModel.deserialize(data)
    print(song.artists[0].name)

.. toctree::
   :maxdepth: 2
   :caption: Contents:
