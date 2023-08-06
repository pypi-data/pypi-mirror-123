from decimal import Decimal
from enum import Enum
from types import GeneratorType
from typing import Text, Dict, Union, Sequence, List, Any

from .consts import _SERIALIZABLE_SIGN
from .errors import DeserializeConfusedError, DeserializeFailedError
from .type_system import (
    BASIC_TYPES,
    _is_union_type,
    _is_sequence_type,
    _is_list_type,
    _is_tuple_type,
    _is_set_type,
)


def __serialize_value(value: Any):
    if getattr(value, _SERIALIZABLE_SIGN, False):
        return value.serialize()
    elif isinstance(value, Decimal):
        return str(value)
    elif isinstance(value, Enum):
        return value.value
    elif (
        isinstance(value, list)
        or isinstance(value, set)
        or isinstance(value, tuple)
        or isinstance(value, GeneratorType)
    ):
        return [__serialize_value(v) for v in value]
    elif isinstance(value, dict):
        return {str(k): __serialize_value(value[k]) for k in value}
    else:
        return value


def json_serializer(self):
    cls_annotations = self.__annotations__
    result = {}

    for field_name in cls_annotations:
        value = getattr(self, field_name)
        result[field_name] = __serialize_value(value)

    return result


def __deserialize_value_for_all_assumed_types(value: Any, desired_types: Sequence[type]):
    hashable_possible_values = set()
    unhashable_possible_values = []
    possible_values_len = lambda: len(hashable_possible_values) + len(unhashable_possible_values)

    for desired_type in desired_types:
        possible_value = __deserialize_value(value, desired_type)
        try:
            hashable_possible_values.add(possible_value)
        except TypeError:
            unhashable_possible_values.append(possible_value)

    if possible_values_len() > 1:
        raise DeserializeConfusedError(
            f"more than 1 possible deserialized value for {value}: {hashable_possible_values}"
        )
    if possible_values_len() == 0:
        raise DeserializeFailedError(
            f"could not deserialize value {value} under types {desired_types}"
        )

    if len(hashable_possible_values) > 0:
        return hashable_possible_values.pop()
    else:
        return unhashable_possible_values[0]


def __deserialize_value(value: Any, desired_type: type):
    if desired_type in BASIC_TYPES:
        return value

    # for deserializable_dataclass type
    if getattr(desired_type, _SERIALIZABLE_SIGN, False):
        return desired_type.deserialize(value)

    if desired_type is Decimal:
        return Decimal(value)

    if hasattr(desired_type, "mro") and Enum in desired_type.mro():
        return desired_type(value)

    # for sequence type
    if _is_sequence_type(desired_type) or _is_list_type(desired_type):
        return [__deserialize_value_for_all_assumed_types(v, desired_type.__args__) for v in value]

    if _is_tuple_type(desired_type):
        return tuple(
            __deserialize_value_for_all_assumed_types(v, desired_type.__args__) for v in value
        )

    if _is_set_type(desired_type):
        return {__deserialize_value_for_all_assumed_types(v, desired_type.__args__) for v in value}

    # for Generic types (Union, Option)
    if _is_union_type(desired_type):
        type_args = desired_type.__args__
        return __deserialize_value_for_all_assumed_types(value, type_args)

    raise NotImplementedError(f"deserialize {value} for type {desired_type} is not supported yet")


@classmethod
def json_deserializer(cls, json: Dict[Text, Union[int, complex, bool, List, Sequence, Dict]]):
    cls_annotations = cls.__annotations__
    obj_values = {}

    for field_name in cls_annotations:
        desired_type = cls_annotations[field_name]
        field_value = json.get(field_name)
        obj_values[field_name] = __deserialize_value(field_value, desired_type)

    return cls(**obj_values)
