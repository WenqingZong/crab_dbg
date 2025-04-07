import io
import sys

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
    dbg_outputs: list[str] = list(filter(lambda x: len(x) > 0, dbg_outputs.split("\n")))
    expected_outputs: list[str] = list(
        filter(lambda x: len(x) > 0, expected_outputs.split("\n"))
    )

    assert dbg_outputs[0].startswith("[tests/test_dbg.py:")
    assert len(dbg_outputs) == len(expected_outputs)
    for dbg_output, expected_output in zip(dbg_outputs, expected_outputs):
        print(dbg_output, expected_output)
        assert dbg_output.endswith(expected_output)


def test_no_argument():
    stdout, _ = _redirect_stdout_stderr_to_buffer()

    dbg()
    _reset_stdout_stderr()

    actual_output = stdout.getvalue().strip()
    assert actual_output.startswith("[tests/test_dbg.py") and actual_output.endswith(
        "]"
    )


def test_single_argument():
    stdout, _ = _redirect_stdout_stderr_to_buffer()

    pi = 3.14
    dbg(pi)
    _reset_stdout_stderr()

    _assert_correct(stdout.getvalue(), "pi = 3.14")


def test_print_to_stderr():
    _, stderr = _redirect_stdout_stderr_to_buffer()

    pi = 3.14
    dbg(pi, file=sys.stderr)
    _reset_stdout_stderr()

    _assert_correct(stderr.getvalue(), "pi = 3.14")


def test_single_argument_with_comment():
    stdout, _ = _redirect_stdout_stderr_to_buffer()

    pi = 3.14
    dbg(
        pi,  # This comment should not show in dbg output
    )
    _reset_stdout_stderr()

    _assert_correct(stdout.getvalue(), "pi = 3.14")


def test_multiple_arguments():
    stdout, _ = _redirect_stdout_stderr_to_buffer()

    pi = 3.14
    ultimate_answer = 42
    flag = True
    stock_price = [100, 99, 101, 1]
    country_to_capital_cities = {
        "China": "Beijing",
        "United Kingdom": "London",
        "Liyue": "Liyue Harbor",
    }
    dbg(
        pi,
        1 + 1,
        sorted(stock_price),
        "This string contains (, ' and ,",
        ultimate_answer,
        flag,  # You can leave a comment here as well, dbg() won't show this comment.
        stock_price,
        country_to_capital_cities,
    )
    _reset_stdout_stderr()

    expected_outputs = """
pi = 3.14
1 + 1 = 2
sorted(stock_price) = [
    1,
    99,
    100,
    101
]
"This string contains (, ' and ," = "This string contains (, ' and ,"
ultimate_answer = 42
flag = True
stock_price = [
    100,
    99,
    101,
    1
]
country_to_capital_cities = {
    China: 'Beijing'
    United Kingdom: 'London'
    Liyue: 'Liyue Harbor'
}
"""

    _assert_correct(stdout.getvalue(), expected_outputs)


def test_cyclic_reference():
    stdout, _ = _redirect_stdout_stderr_to_buffer()

    infinite_list = []
    infinite_list.append(infinite_list)

    infinite_dict = {}
    infinite_dict["self"] = infinite_dict
    dbg(infinite_list, infinite_dict)
    _reset_stdout_stderr()

    expected_outputs = """
infinite_list = [
    [...]
]
infinite_dict = {
    self: {...}
}
"""

    _assert_correct(stdout.getvalue(), expected_outputs)


class Phone:
    def __init__(self, brand, color, price):
        self.brand = brand
        self.color = color
        self.price = price

    def __repr__(self):
        return "Phone:\n    Color: %s\n    Brand: %s\n    Price: %s\n" % (
            self.color,
            self.brand,
            self.price,
        )


def test_custom_repr():
    stdout, _ = _redirect_stdout_stderr_to_buffer()

    phone = Phone("Apple", "White", 1099)
    dbg(phone)
    _reset_stdout_stderr()

    expected_outputs = """
Phone:
    Color: White
    Brand: Apple
    Price: 1099
"""

    _assert_correct(stdout.getvalue(), expected_outputs)


class Node:
    def __init__(self, val=0, next_=None, prev=None):
        self.val = val
        self.next = next_
        self.prev = prev


class DoubleLinkedList:
    def __init__(self, head=None, tail=None):
        self.head = head
        self.tail = tail

    @staticmethod
    def create(n: int) -> "DoubleLinkedList":
        """
        Create a LinkedList of n elements, value ranges from 0 to n - 1.
        """
        if n <= 0:
            raise ValueError("A double linked list with %d element is meaningless", n)

        head = Node(0)

        cur = head
        for i in range(1, n):
            new_node = Node(i)
            cur.next = new_node
            new_node.prev = cur
            cur = cur.next

        return DoubleLinkedList(head=head, tail=cur)


def test_object():
    stdout, _ = _redirect_stdout_stderr_to_buffer()

    double_linke_list = DoubleLinkedList.create(2)
    dbg(double_linke_list)
    _reset_stdout_stderr()

    # Note the CYCLIC REFERENCE here.
    expected_outputs = """
DoubleLinkedList {
    head: Node {
        val: 0
        next: Node {
            val: 1
            next: None
            prev: CYCLIC REFERENCE
        }
        prev: None
    }
    tail: Node {
        val: 1
        next: None
        prev: Node {
            val: 0
            next: CYCLIC REFERENCE
            prev: None
        }
    }
}
"""

    _assert_correct(stdout.getvalue(), expected_outputs)


def test_nested_data_container():
    stdout, _ = _redirect_stdout_stderr_to_buffer()

    double_linked_list = DoubleLinkedList.create(2)
    dbg(
        [double_linked_list, double_linked_list],
        (double_linked_list, double_linked_list),
        {"a": 1, "b": [double_linked_list]},
        [
            1,
            2,
            3,
            4,
        ],
    )
    _reset_stdout_stderr()

    expected_outputs = """
[double_linked_list, double_linked_list] = [
    DoubleLinkedList {
        head: Node {
            val: 0
            next: Node {
                val: 1
                next: None
                prev: CYCLIC REFERENCE
            }
            prev: None
        }
        tail: Node {
            val: 1
            next: None
            prev: Node {
                val: 0
                next: CYCLIC REFERENCE
                prev: None
            }
        }
    },
    DoubleLinkedList {
        head: Node {
            val: 0
            next: Node {
                val: 1
                next: None
                prev: CYCLIC REFERENCE
            }
            prev: None
        }
        tail: Node {
            val: 1
            next: None
            prev: Node {
                val: 0
                next: CYCLIC REFERENCE
                prev: None
            }
        }
    }
]
(double_linked_list, double_linked_list) = (
    DoubleLinkedList {
        head: Node {
            val: 0
            next: Node {
                val: 1
                next: None
                prev: CYCLIC REFERENCE
            }
            prev: None
        }
        tail: Node {
            val: 1
            next: None
            prev: Node {
                val: 0
                next: CYCLIC REFERENCE
                prev: None
            }
        }
    },
    DoubleLinkedList {
        head: Node {
            val: 0
            next: Node {
                val: 1
                next: None
                prev: CYCLIC REFERENCE
            }
            prev: None
        }
        tail: Node {
            val: 1
            next: None
            prev: Node {
                val: 0
                next: CYCLIC REFERENCE
                prev: None
            }
        }
    }
)
{'a': 1, 'b': [double_linked_list]} = {
    a: 1
    b: [
        DoubleLinkedList {
            head: Node {
                val: 0
                next: Node {
                    val: 1
                    next: None
                    prev: CYCLIC REFERENCE
                }
                prev: None
            }
            tail: Node {
                val: 1
                next: None
                prev: Node {
                    val: 0
                    next: CYCLIC REFERENCE
                    prev: None
                }
            }
        }
    ]
}
[1, 2, 3, 4] = [
    1,
    2,
    3,
    4
]
"""

    _assert_correct(stdout.getvalue(), expected_outputs)


class Stack:
    def __init__(self):
        self.data = []

    def push(self, item):
        self.data.append(item)

    def pop(self):
        return self.data.pop()


def test_complex_object():
    stdout, _ = _redirect_stdout_stderr_to_buffer()

    double_linked_list = DoubleLinkedList.create(2)
    stack = Stack()
    stack.push(double_linked_list)
    stack.push(double_linked_list)
    dbg(stack)
    _reset_stdout_stderr()

    expected_outputs = """
Stack {
    data: [
        DoubleLinkedList {
            head: Node {
                val: 0
                next: Node {
                    val: 1
                    next: None
                    prev: CYCLIC REFERENCE
                }
                prev: None
            }
            tail: Node {
                val: 1
                next: None
                prev: Node {
                    val: 0
                    next: CYCLIC REFERENCE
                    prev: None
                }
            }
        },
        DoubleLinkedList {
            head: Node {
                val: 0
                next: Node {
                    val: 1
                    next: None
                    prev: CYCLIC REFERENCE
                }
                prev: None
            }
            tail: Node {
                val: 1
                next: None
                prev: Node {
                    val: 0
                    next: CYCLIC REFERENCE
                    prev: None
                }
            }
        }
    ]
}
"""

    _assert_correct(stdout.getvalue(), expected_outputs)


def test_indent_with_multi_line_repr():
    stdout, _ = _redirect_stdout_stderr_to_buffer()

    phone = Phone("Apple", "White", 1099)
    dbg({"my_phones": [phone]})
    _reset_stdout_stderr()

    expected_outputs = """
{'my_phones': [phone]} = {
    my_phones: [
        Phone:
            Color: White
            Brand: Apple
            Price: 1099
    ]
}
"""

    _assert_correct(stdout.getvalue(), expected_outputs)
