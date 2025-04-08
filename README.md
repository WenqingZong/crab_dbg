# Crab Debugger

This repo contains the Python equivalent of Rust's `dbg!()` macro debugging tool, which helps developers inspect variables and expressions during development. The `dbg` method is a perfect replacement for Python built-in function `print` so if that is your way of debugging, then you can switch to `crab_dbg` with just a `Ctrl + R` to replace `print(` with `dbg(`.

## Unique Selling Point

- Print absolutely ***ANYTHING*** in human friendly way.
- Wherever `print()` works, `dbg()` works.
- You can use this library by just `Ctrl+R` to replace `print(` with `dbg(`.
- When `dbg()` is called, the output also includes the file name, line number, and other key info for context.

## Example Usage

```python
pi = 3.14
ultimate_answer = 42
flag = True
stock_price = [100, 99, 101, 1]
fruits = {"apple", "peach", "watermelon"}
country_to_capital_cities = {
    "China": "Beijing",
    "United Kingdom": "London",
    "Liyue": "Liyue Harbor",
}

# You can use dbg to inspect a lot of variables.
dbg(
    pi,
    1 + 1,
    sorted(stock_price),
    "This string contains (, ' and ,",
    ultimate_answer,
    flag,  # You can leave a comment here as well, dbg() won't show this comment.
    stock_price,
    fruits,
    country_to_capital_cities,
)

# Or, you can use dbg to inspect one. Note that you can pass any keyword arguments originally supported by print()
dbg(country_to_capital_cities, file=stderr)

# You can also use dbg to inspect expressions.
dbg(1 + 1)

# When used with objects, it will show all fields contained by that object.
double_linked_list = DoubleLinkedList.create(2)
dbg(double_linked_list)

# dbg() works with lists, tuples, and dictionaries.
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

# For even more complex structures, it works as well.
stack = Stack()
stack.push(double_linked_list)
stack.push(double_linked_list)
dbg(stack)

dbg("What if my input is a string?")

# If your type has its own __repr__ or __str__ implementation, no worries, crab_dbg will jut use it.
phone = Phone("Apple", "white", 1099)
dbg(phone)
dbg({"my_phones": [phone]})

# If you are extremely bored.
infinite_list = []
infinite_list.append(infinite_list)
dbg(infinite_list)

# If invoked without arguments, then it will just print the filename and line number.
dbg()

import numpy as np

# This library can also be used with your favorite data science libraries if you enabled our optional features.
ndarray = np.array([[1, 2, 3], [4, 5, 6]])
dbg(ndarray)

# And yes, even deeply nested ndarray is possible.
stack = Stack()
stack.push({"dict_key": ndarray})
dbg(stack)
```

The above example will generate the following output in your terminal:

```text
[examples/example.py:76:5] pi = 3.14
[examples/example.py:76:5] 1 + 1 = 2
[examples/example.py:76:5] sorted(stock_price) = [
    1,
    99,
    100,
    101
]
[examples/example.py:76:5] "This string contains (, ' and ," = "This string contains (, ' and ,"
[examples/example.py:76:5] ultimate_answer = 42
[examples/example.py:76:5] flag = True
[examples/example.py:76:5] stock_price = [
    100,
    99,
    101,
    1
]
[examples/example.py:76:5] fruits = {
    'peach',
    'watermelon',
    'apple'
}
[examples/example.py:76:5] country_to_capital_cities = {
    China: 'Beijing',
    United Kingdom: 'London',
    Liyue: 'Liyue Harbor'
}
[examples/example.py:89:5] country_to_capital_cities = {
    China: 'Beijing',
    United Kingdom: 'London',
    Liyue: 'Liyue Harbor'
}
[examples/example.py:92:5] 1 + 1 = 2
[examples/example.py:96:5] double_linked_list = DoubleLinkedList {
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
[examples/example.py:99:5] [double_linked_list, double_linked_list] = [
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
[examples/example.py:99:5] (double_linked_list, double_linked_list) = (
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
[examples/example.py:99:5] {'a': 1, 'b': [double_linked_list]} = {
    a: 1,
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
[examples/example.py:99:5] [1, 2, 3, 4] = [
    1,
    2,
    3,
    4
]
[examples/example.py:115:5] stack = Stack {
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
[examples/example.py:117:5] 'What if my input is a string?' = 'What if my input is a string?'
[examples/example.py:121:5] phone = Phone:
    Color: white
    Brand: Apple
    Price: 1099
[examples/example.py:122:5] {'my_phones': [phone]} = {
    my_phones: [
        Phone:
            Color: white
            Brand: Apple
            Price: 1099
    ]
}
[examples/example.py:127:5] infinite_list = [
    [...]
]
[examples/example.py:130:5]
[examples/example.py:136:5] ndarray = 
array([[1, 2, 3],
       [4, 5, 6]])
[examples/example.py:141:5] stack = Stack {
    data: [
        {
            dict_key: 
                array([[1, 2, 3],
                       [4, 5, 6]])
        }
    ]
}
```

For full executable code please refer to [./examples/example.py](./examples/example.py).

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](./LICENSE) file for details.
