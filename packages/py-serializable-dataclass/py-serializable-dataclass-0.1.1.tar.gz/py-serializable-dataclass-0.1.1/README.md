# Serializable Dataclass for Python
![](https://github.com/tinyHui/python-serializable-dataclass/actions/workflows/pythonpackage.yaml/badge.svg) [![codecov](https://codecov.io/gh/tinyHui/python-serializable-dataclass/branch/main/graph/badge.svg?token=OXR3RZB0KN)](https://codecov.io/gh/tinyHui/python-serializable-dataclass)

This library provides a very simple API for encoding and decoding Python class to and from a designated serializable type.

## Quickstart

`pip install python=serializable-dataclass`

First, you need to define the data object, e.g.
```python
from serializable_dataclass import serializable_dataclass, Lang

@serializable_dataclass(language=Lang)
class AnyData:
    field1: int
    field2: Optional[str]
    field3: Text
```

Now, enjoy the easy accessed serialization
```python
# To serialize
assert AnyData(field1=1, 
               field2="string", 
               field3="another string").serialize() == {
                        "field1": 1,
                        "field2": "string",
                        "field3": "another string",
                    }

# To deserialize
AnyData.deserialize(
            {
                "field1": 1,
                "field2": None,
                "field3": "another string",
            }
        ) == AnyData(field1=1, field2=None, field3="another string")
```

The `language` parameter is optional and it's default value is `JSON`.
