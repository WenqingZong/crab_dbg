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


def _reset_stdout_stderr():
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__


def _assert_correct(dbg_outputs: str, expected_outputs: str) -> None:
    """
    This function checks if dbg() outputs desired variable name and their desired value.
    Note that we do not check line no and col no in the output, as they change for almost every modification of this
    file.
    """
    dbg_outputs: list[str] = dbg_outputs.split("\n")
    expected_outputs: list[str] = expected_outputs.split("\n")

    assert dbg_outputs[0].startswith("[tests/test_dbg.py:")
    for dbg_output, expected_output in zip(dbg_outputs[1:], expected_outputs[1:]):
        assert dbg_output == expected_output


def test_single_argument():
    stdout, stderr = _redirect_stdout_stderr_to_buffer()

    pi = 3.14
    dbg(pi)
    _reset_stdout_stderr()

    # Only one of stdout and stderr will contain the actual output, the other would be empty.
    _assert_correct(stdout.getvalue() + stderr.getvalue(), "pi = 3.14\n")


def test_single_argument_with_comment():
    stdout, stderr = _redirect_stdout_stderr_to_buffer()

    pi = 3.14
    dbg(
        pi,  # This comment should not show in dbg output
    )
    _reset_stdout_stderr()

    # Only one of stdout and stderr will contain the actual output, the other would be empty.
    _assert_correct(stdout.getvalue() + stderr.getvalue(), "pi = 3.14\n")
