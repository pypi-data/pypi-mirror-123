BASIC_TYPES = [int, float, complex, bool, str, type(None)]


def _is_union_type(typing):
    # Python3.8 does not support GenericAlias yet
    if getattr(typing, "__origin__", False):
        type_name = getattr(typing.__origin__, "_name", None)

        return type_name == "Union"

    return False


def _is_sequence_type(typing):
    return getattr(typing, "_name") == "Sequence"


def _is_list_type(typing):
    return getattr(typing, "_name") == "List"


def _is_tuple_type(typing):
    return getattr(typing, "_name") == "Tuple"


def _is_set_type(typing):
    return getattr(typing, "_name") == "Set"
