# Crab Debugger
This repo contains the Python equivalent of Rust's `dbg!()` macro debugging tool, which helps developers inspect variables and expressions during development. The `dbg` method is a perfect replacement for Python built-in function `print` so if that is your way of debugging, then you can switch to `crab_dbg` with just a `Ctrl + R` to replace `print(` with `dbg(`.

## Unique Selling Point
- Easily print values of variables and expressions using the `dbg()` function, eliminating the need for multiple `print()` statements
- Supports primitive types (int, char, str, bool, etc.) along with basic and complex data structures (lists, arrays, NumPy arrays, PyTorch tensors, etc.)
- When `dbg()` is called, the output also includes the file name, line number, and other key info for context
- Able to process multi-line arguments and recursively inspects user-defined classes and nested objects.

## Optional Features
Currently (version `0.1.1`), this library have three optional features: `numpy`, `pandas`, and `torch`. You should add the corresponding feature if you want to call `dbg()` on `numpy.ndarray`, `pandas.DataFrame`, or `torch.Tensor`.

## Example Usage
```python
from sys import stderr
from crab_dbg import dbg

pi = 3.14
ultimate_answer = 42
flag = True
fruits = ["apple", "peach", "watermelon"]
country_to_capital_cities = {
    "China": "Beijing",
    "United Kingdom": "London",
    "Liyue": "Liyue Harbor",
}

# You can use dbg to inspect a lot of variables.
dbg(
    pi,
    ultimate_answer,
    flag,  # You can leave a comment here as well, dbg() won't show this comment.
    fruits,
    country_to_capital_cities,
)

# Or, you can use dbg to inspect one. Note that you can pass any keyword arguments originally supported by print()
dbg(country_to_capital_cities, file=stderr)

# You can also use dbg to inspect expressions.
dbg(1 + 1)

# When used with objects, it will show all fields contained by that object.
linked_list = LinkedList.create(2)
dbg(linked_list)

# dbg() works with lists, tuples, and dictionaries.
dbg(
    [linked_list, linked_list],
    (linked_list, linked_list),
    {"a": 1, "b": linked_list},
    [
        1,
        2,
        3,
        4,
    ],
)

# For even more complex structures, it works as well.
stack = Stack()
stack.push(linked_list)
stack.push(linked_list)
dbg(stack)

dbg("What if my input is a string?")

# If your type has its own __repr__ or __str__ implementation, no worries, crab_dbg will jut use it.
phone = Phone("Apple", "white", 1099)
dbg(phone)

# It works with your favorite machine learning data structures as well, if you enabled corresponding features.
import numpy as np
import torch
numpy_array = np.zeros(shape=(2, 3))
dbg(numpy_array)

torch_tensor = torch.from_numpy(numpy_array)
dbg(torch_tensor)

# If invoked without arguments, then it will just print the filename and line number.
dbg()

import numpy as np
import torch
# This library can also be used with your favorite data science libraries if you enabled our optional features.
numpy_array = np.zeros(shape=(2, 3))
dbg(numpy_array)

torch_tensor = torch.from_numpy(numpy_array)
dbg(torch_tensor)
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
    'apple',
    'watermelon'
}
[examples/example.py:76:5] country_to_capital_cities = {
    China: 'Beijing'
    United Kingdom: 'London'
    Liyue: 'Liyue Harbor'
}
[examples/example.py:89:5] country_to_capital_cities = {
    China: 'Beijing'
    United Kingdom: 'London'
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
[examples/example.py:136:5] numpy_array = 
array([[0., 0., 0.],
       [0., 0., 0.]])
[examples/example.py:139:5] torch_tensor = 
tensor([[0., 0., 0.],
        [0., 0., 0.]], dtype=torch.float64)
```

For full executable code please refer to [./examples/example.py](./examples/example.py).

## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](./LICENSE) file for details.
