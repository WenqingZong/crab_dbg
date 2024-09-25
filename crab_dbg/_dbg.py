import dis
import inspect
from io import StringIO
import tokenize
from typing import Any

import numpy as np
import pandas
import torch


def _is_numpy_tensor_pandas_data(val: Any):
    """Check if the value is numpy ndarray, pytorch tensor, pandas data frame"""
    return (
        isinstance(val, np.ndarray)
        or isinstance(val, torch.Tensor)
        or isinstance(val, pandas.DataFrame)
    )


def _has_custom_repr(val: Any):
    """Check if the value has a custom __repr__."""
    return val.__class__.__repr__ is not object.__repr__


def _has_custom_str(val: Any):
    """Check if the value has a custom __str__."""
    return val.__class__.__str__ is not object.__str__


def _is_built_in_types(val: Any) -> bool:
    """
    Determine if a values is an instance of python built-in types.
    """
    return type(val).__module__ == "builtins"


def _is_data_container(val: Any) -> bool:
    """
    Determine if a value's type if list, tuple, or dict.
    """
    return isinstance(val, list) or isinstance(val, tuple) or isinstance(val, dict)


def _get_dbg_raw_args(source_code: str, positions: dis.Positions) -> list[str]:
    """
    Get the arguments to dbg() function as a list of strings. Does not include keyword arguments.
    """

    def _split_by_out_most_comma(input_: str) -> list[str]:
        """
        Split a long string by the out most ','

        E.g. Input is "[linked_list, linked_list], (linked_list, linked_list), {'a': 1, 'b': linked_list}, pai, flag,"
        Expected outcome is: [
            "[linked_list, linked_list]",
            "(linked_list, linked_list)",
            {'a': 1, 'b': linked_list},
            "pai",
            "flag",
        ]
        """
        parts = []
        current_part = []
        stack = []

        for char in input_:
            if char == "," and not stack:
                parts.append("".join(current_part).strip())
                current_part = []
            else:
                current_part.append(char)
                if char in "([{":
                    stack.append(char)
                elif char in ")]}":
                    if stack and (
                        (char == ")" and stack[-1] == "(")
                        or (char == "]" and stack[-1] == "[")
                        or (char == "}" and stack[-1] == "{")
                    ):
                        stack.pop()

        # Append the last part if there's any
        if current_part:
            parts.append("".join(current_part).strip())

        return parts

    full_code = source_code.split("\n")

    # Get the dbg function call. This might across multiple lines.
    code_lines = list(
        map(lambda x: x.strip(), full_code[positions.lineno - 1 : positions.end_lineno])
    )

    # Delete inline comments.
    for i, code_line in enumerate(code_lines):
        if "#" in code_line:
            new_line = []
            # We parse the line into python code so we know if the "#" is comment or a part of a string.
            tokens = tokenize.generate_tokens(StringIO(code_line).readline)
            for token_type, token_string, _, _, _ in tokens:
                if token_type != tokenize.COMMENT:
                    new_line.append(token_string)
            code_lines[i] = "".join(new_line)

    # Concat them into one line.
    striped_source_code = "".join(code_lines)

    # Delete 'dbg(' and the last ')'.
    arguments_str = striped_source_code[4:-1]

    # Split each argument.
    arguments = list(
        filter(lambda x: "=" not in x, _split_by_out_most_comma(arguments_str))
    )

    # Clear any remaining whitespaces in argument.
    return list(map(lambda x: x.strip(), arguments))


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
    if isinstance(object_, list) or isinstance(object_, tuple):
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
        else:
            return "(\n" + ",\n".join(fields_dbg_repr) + "\n" + " " * indent + ")"
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


def dbg(*evaluated_args, sep=" ", end="\n", file=None, flush=False) -> list[str]:
    """
    Python implementation of rust's dbg!() macro. All behaviour should be the same (or similar at least) as dbg!().

    This implementation is meant to be a perfect replacement to python's built-in function print(), so it supports all
    keyword raw_args accepted by print().

    @param sep: Same as print().
    @param end: Same as print().
    @param file: Same as print().
    @param flush: Same as print().
    """
    frame = inspect.currentframe().f_back
    info = inspect.getframeinfo(frame)

    # Read the source code file as a single string.
    source_code = ""
    with open(info.filename, "r") as f:
        source_code = f.read()

    raw_args = _get_dbg_raw_args(source_code, info.positions)

    assert len(raw_args) == len(
        evaluated_args
    ), "Number of raw_args does not equal to number of received args"

    # If no arguments at all.
    if len(raw_args) == 0:
        print(
            # [<file_abs_path>:<line_no>:<col_no>]
            "[%s:%s:%s]"
            % (
                info.filename,
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
            # [<file_abs_path>:<line_no>:<col_no>] <raw_args> = <dbg_repr>
            "[%s:%s:%s] %s = %s"
            % (
                info.filename,
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
