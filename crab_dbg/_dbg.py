from ast import parse, unparse
import dis
import inspect
from os import path
from sys import stderr
from typing import Any


def _is_numpy_tensor_pandas_data(val: Any) -> bool:
    """Check if the value is numpy ndarray, pytorch tensor, or pandas data frame"""

    # Cannot use isinstance() here as import those large library is too time-consuming.
    cls = val.__class__
    module = cls.__module__
    name = cls.__name__

    # Check for numpy.ndarray
    if module == "numpy" and name == "ndarray":
        return True

    # Check for PyTorch Tensor
    if module == "torch" and name == "Tensor":
        return True

    # Check for pandas DataFrame (module starts with 'pandas' and class name is 'DataFrame')
    if module.startswith("pandas.") and name == "DataFrame":
        return True

    return False


def _has_custom_repr(val: Any) -> bool:
    """Check if the value has a custom __repr__."""
    return val.__class__.__repr__ is not object.__repr__


def _has_custom_str(val: Any) -> bool:
    """Check if the value has a custom __str__."""
    return val.__class__.__str__ is not object.__str__


def _is_built_in_types(val: Any) -> bool:
    """
    Determine if a values is an instance of python built-in types.
    """
    return type(val).__module__ == "builtins"


def _get_dbg_raw_args(source_code: str, positions: dis.Positions) -> list[str]:
    """
    Get the arguments to dbg() function as a list of strings. Does not include keyword arguments.
    """
    source_code_lines: list[str] = source_code.split("\n")

    # Get the dbg function call. This might across multiple lines.
    dbg_call_lines: list[str] = list(
        map(
            lambda x: x.strip(),
            source_code_lines[positions.lineno - 1 : positions.end_lineno],
        )
    )

    dbg_call: str = "\n".join(dbg_call_lines)
    dbg_call_args = parse(dbg_call).body[0].value.args
    return [unparse(arg) for arg in dbg_call_args]


def _get_human_readable_repr(object_: Any, indent: int = 0) -> str:
    """
    Get a useful dbg representation of an object.

    By default, python just prints things like '<__main__.Linkedlist object at 0x102c47560>', which is useless.
    This function returns things like:
    Linkedlist {
        start: Node {
            val: 0,
            next: Node {
                val: 1,
                next: Node {
                    val: 2,
                    next: None,
                }
            }
        }
    }
    """
    INDENT_INCREMENT = 4
    fields_dbg_repr = []

    # Handle data containers.
    if isinstance(object_, (list, set, tuple)):
        for item in object_:
            # <num_of_ident><val>
            fields_dbg_repr.append(
                "%s%s"
                % (
                    " " * (indent + INDENT_INCREMENT),
                    _get_human_readable_repr(item, indent + INDENT_INCREMENT),
                )
            )

        if isinstance(object_, list):
            return "[\n" + ",\n".join(fields_dbg_repr) + "\n" + " " * indent + "]"
        elif isinstance(object_, tuple):
            return "(\n" + ",\n".join(fields_dbg_repr) + "\n" + " " * indent + ")"
        else:
            return "{\n" + ",\n".join(fields_dbg_repr) + "\n" + " " * indent + "}"
    elif isinstance(object_, dict):
        for key, value in object_.items():
            if _is_built_in_types(value):
                # <num_of_ident><key>: <val>
                fields_dbg_repr.append(
                    "%s%s: %s" % (" " * (indent + INDENT_INCREMENT), key, value)
                )
            else:
                fields_dbg_repr.append(
                    "%s%s: %s"
                    % (
                        " " * (indent + INDENT_INCREMENT),
                        key,
                        _get_human_readable_repr(value, indent + INDENT_INCREMENT),
                    )
                )
        return "{\n" + "\n".join(fields_dbg_repr) + "\n" + " " * indent + "}"
    elif _is_numpy_tensor_pandas_data(object_):
        return "\n" + repr(object_)
    elif _has_custom_repr(object_):
        return repr(object_)
    elif _has_custom_str(object_) or _is_built_in_types(object_):
        return str(object_)

    # Just an object without __repr__ or __str__ provided.
    for key, value in object_.__dict__.items():
        fields_dbg_repr.append(
            "%s%s: %s"
            % (
                " " * (indent + INDENT_INCREMENT),
                key,
                _get_human_readable_repr(value, indent + INDENT_INCREMENT),
            )
        )
    return (
        object_.__class__.__name__
        + " {\n"
        + "\n".join(fields_dbg_repr)
        + "\n"
        + " " * indent
        + "}"
    )


# TODO: How to add typehint for frame argument?
def _get_source_code(frame, filename: str) -> str | None:
    """
    Get the source code of this frame as a single string.
    We try to read the named file first, if failed, then try inspect.getsource() to handle the cases where source code
    file is not available.
    """
    try:
        with open(filename, "r") as f:
            return f.read()
    except OSError:
        pass

    try:
        return inspect.getsource(frame)
    except OSError:
        return None


def dbg(*evaluated_args, sep=" ", end="\n", file=None, flush=False):
    """
    Python implementation of rust's dbg!() macro. All behaviors should be the same (or similar at least) as dbg!().

    This implementation is meant to be a perfect replacement to python's built-in function print(), so it supports all
    keyword raw_args accepted by print().

    @param sep: Same as print().
    @param end: Same as print().
    @param file: Same as print().
    @param flush: Same as print().
    """
    frame = inspect.currentframe().f_back
    info = inspect.getframeinfo(frame)

    # Cannot use inspect.getsource, limited by dynamic environment, such like pytest.
    source_code = _get_source_code(frame, info.filename)
    if source_code is None:
        print("crab_dbg: Sorry, cannot get original code", file=stderr)
        return

    raw_args = _get_dbg_raw_args(source_code, info.positions)

    assert len(raw_args) == len(evaluated_args), (
        "Number of raw_args does not equal to number of received args"
    )

    # If no arguments at all.
    if len(raw_args) == 0:
        print(
            # [<file_rel_path>:<line_no>:<col_no>]
            "[%s:%s:%s]"
            % (
                path.relpath(info.filename),
                info.lineno,
                info.positions.col_offset + 1,  # Because this is col idx.
            ),
            sep=sep,
            end=end,
            file=file,
            flush=flush,
        )

    for raw_arg, evaluated_arg in zip(raw_args, evaluated_args):
        human_readable_repr = _get_human_readable_repr(evaluated_arg)
        print(
            # [<file_rel_path>:<line_no>:<col_no>] <raw_args> = <dbg_repr>
            "[%s:%s:%s] %s = %s"
            % (
                path.relpath(info.filename),
                info.lineno,
                info.positions.col_offset + 1,  # Because this is col idx.
                raw_arg,
                human_readable_repr,
            ),
            sep=sep,
            end=end,
            file=file,
            flush=flush,
        )
