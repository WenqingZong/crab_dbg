import io
import re
import sys
from typing import Any

from crab_dbg import dbg


def _redirect_stdout_stderr_to_buffer() -> tuple[io.StringIO, io.StringIO]:
    """
    By the nature of dbg(), the only way to test it works is by capture stdout.
    We also capture stderr as dbg() is designed to be compatible with print(), which accepts file=sys.stderr as
    an argument.
    """
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()

    sys.stdout = stdout_buffer
    sys.stderr = stderr_buffer

    return stdout_buffer, stderr_buffer


def _revert_stdout_stderr_change():
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__


def _assert_correct(
    dbg_outputs: str, var_names: list[str], var_values: list[Any]
) -> None:
    """
    This function checks if dbg() outputs desired variable name and their desired value.
    dbg() output contains line number, and absolute file path, so we cannot exam them.
    """
    dbg_outputs = dbg_outputs.split("\n")
    print("dbg_outputsssssssss", dbg_outputs)
    assert len(dbg_outputs) - 1 == len(var_names) == len(var_values)

    for dbg_output, var_name, var_value in zip(dbg_outputs[:-1], var_names, var_values):
        dbg_output = re.sub(r"\[.*?\]", "", dbg_output)
        splits = dbg_output.split("=")
        assert splits[0].strip() == var_name
        assert splits[1].strip() == repr(var_value)


def test_single_argument():
    stdout, stderr = _redirect_stdout_stderr_to_buffer()

    pai = 3.14
    dbg(pai)
    _revert_stdout_stderr_change()

    # Only one of stdout and stderr will contain the actual output, the other would be empty.
    _assert_correct(stdout.getvalue() + stderr.getvalue(), ["pai"], [pai])


def test_single_argument_with_comment():
    stdout, stderr = _redirect_stdout_stderr_to_buffer()

    pai = 3.14
    dbg(
        pai,  # This comment should not shown in dbg output
    )
    _revert_stdout_stderr_change()

    # Only one of stdout and stderr will contain the actual output, the other would be empty.
    _assert_correct(stdout.getvalue() + stderr.getvalue(), ["pai"], [pai])
