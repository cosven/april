# april

[![Build Status](https://travis-ci.org/cosven/april.svg?branch=master)](https://travis-ci.org/cosven/april)
[![Coverage Status](https://coveralls.io/repos/github/cosven/april/badge.svg?branch=master)](https://coveralls.io/github/cosven/april?branch=master)

lightweight & declarative model representation

> `april` usually works along with serialization library, such as [marshmallow](http://marshmallow.readthedocs.io/en/latest/quickstart.html#deserializing-to-objects)

**temporarily python3 only.**

## Usage

### simple usage

```python
from datetime import datetime

from april import Struct


class UserModel(Struct):
    _fields = ['name', 'age', 'birthday']

user = UserModel(name='lucy', age=20, birthday=datetime.now())
```
