from enum import Enum, auto


_SERIALIZABLE_SIGN = "__is_serializable__"


class Lang(Enum):
    JSON = auto()
