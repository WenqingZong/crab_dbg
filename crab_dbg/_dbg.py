from dis import Positions
import inspect
from typing import List

def _is_built_in_types(val) -> bool:
    """
    Determine if a values is an instance of python built-in types.
    """
    print(val, type(val), type(val).__module__)
    return type(val).__module__ == 'builtins'

def _get_dbg_arguments(source_code: str, positions: Positions) -> List[str]:
    """
    Get the arguments to dbg() function as a list of strings.
    """
    full_code = source_code.split('\n')

    # Get the dbg function call. This might across multiple lines.
    code_lines = list(map(lambda x: x.strip(), full_code[positions.lineno - 1: positions.end_lineno]))

    # Concat them into one line.
    stript_source_code = ''.join(code_lines)

    # Delete 'dbg(' and the last ')'.
    arguments_str = stript_source_code[4: -1]

    # Split arguments string by ',', and delete any empty argument (this might happen if the last argument is followed
    # by a ',')
    arguments = list(filter(lambda x: len(x) > 0, arguments_str.split(',')))

    # Clear any remaining whitespaces in argument.
    return list(map(lambda x: x.strip(), arguments))


def dbg(*args):
    frame = inspect.currentframe().f_back
    info = inspect.getframeinfo(frame)
    arguments = _get_dbg_arguments(inspect.getsource(frame), info.positions)

    assert len(arguments) == len(args), "Number of arguments does not equal to number of received args"
    for argument, val in zip(arguments, args):
        val_repr = val if _is_built_in_types(val) else val.__dict__
        print(
            "[%s:%s:%s] %s = %s" % (
                info.filename,
                info.lineno,
                info.positions.col_offset + 1,  # Because this is col idx.
                argument,
                val_repr,
            )
        )
