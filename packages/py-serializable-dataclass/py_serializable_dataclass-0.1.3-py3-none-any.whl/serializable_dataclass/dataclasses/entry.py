from dataclasses import _process_class

from .consts import Lang, _SERIALIZABLE_SIGN
from .json import json_serializer, json_deserializer
from .registry import SerializableDataclassRegistry


def serializable_dataclass(
    cls=None,
    *,
    language=Lang.JSON,
    init=True,
    repr=True,
    eq=True,
    order=False,
    unsafe_hash=False,
    frozen=False,
):
    def wrapper(cls):
        processed_class = _process_class(
            cls, init=init, repr=repr, eq=eq, order=order, unsafe_hash=unsafe_hash, frozen=frozen
        )
        if language == Lang.JSON:
            serialize_fn = json_serializer
            deserialize_fn = json_deserializer
        else:
            raise NotImplementedError(f"language {language} does not supported")
        setattr(processed_class, _SERIALIZABLE_SIGN, True)
        setattr(processed_class, "serialize", serialize_fn)
        setattr(processed_class, "deserialize", deserialize_fn)
        return processed_class

    # call with no parameters
    if cls is None:
        return wrapper

    SerializableDataclassRegistry().register(cls)

    # class with parameters
    return wrapper(cls)
