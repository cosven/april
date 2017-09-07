# april

[![Build Status](https://travis-ci.org/cosven/april.svg?branch=master)](https://travis-ci.org/cosven/april)
[![Coverage Status](https://coveralls.io/repos/github/cosven/april/badge.svg?branch=master)](https://coveralls.io/github/cosven/april?branch=master)

lightweight & declarative model/struct representation

## Usage

### simple usage

```python
from datetime import datetime

from april import Struct


class User(Struct):
    _fields = ['name', 'age', 'birthday']

user = UserModel(name='lucy', age=20, birthday='2017-09-08')

class VIP(User):
    _fields = ['level']

vip = VIP(user, level=1)
vip.name == lucy
```


> tips: `april` usually works along with serialization library, such as [marshmallow](http://marshmallow.readthedocs.io/en/latest/quickstart.html#deserializing-to-objects)

