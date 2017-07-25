# april

[![Build Status](https://travis-ci.org/cosven/april.svg?branch=master)](https://travis-ci.org/cosven/april)
[![Coverage Status](https://coveralls.io/repos/github/cosven/april/badge.svg?branch=master)](https://coveralls.io/github/cosven/april?branch=master)

simplified data deserialization

`april` do following things:

- simple type validation
- python object serialization and data deserialization

typical usage:

- simple model representation

**temporarily python3 only.**

## Usage

### simple usage

```python
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
```

### complex usage

```python

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
```
