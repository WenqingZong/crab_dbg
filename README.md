# Crab Debugger
This repo contains the Python equivalent of Rust's `dbg!()` macro debugging tool, which helps developers inspect variables and expressions during development. The `dbg` method is a perfect replacement for Python built-in function `print` so if that is your way of debugging, then you can switch to `crab_dbg` with just a `Ctrl + R` to replace `print(` with `dbg(`.

## Features
- Easily print values of variables and expressions using the `dbg()` function, eliminating the need for multiple `print()` statements
- Supports primitive types (int, char, str, bool, etc.) along with basic and complex data structures (lists, arrays, NumPy arrays, PyTorch tensors, etc.)
- When `dbg()` is called, the output also includes the file name, line number, and other key info for context
- Able to process multi-line arguments and recursively inspects user-defined classes and nested objects. 

## Example Usage
```python
from sys import stderr
from crab_dbg import dbg

pai = 3.14
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
    pai,
    ultimate_answer,
    flag,  # You can leave a comment here as well, dbg() won't show this comment.
    fruits,
    country_to_capital_cities,
)

# Or, you can ust dbg to inspect one. Note that you can pass any keyword arguments originally supported by print()
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

# It works with your favorite machine learning data structures as well.
import numpy as np
import torch
numpy_array = np.zeros(shape=(2, 3))
dbg(numpy_array)

torch_tensor = torch.from_numpy(numpy_array)
dbg(torch_tensor)

# If invoked without arguments, then it will just print the filename and line number.
dbg()
```

The above example will generate the following output in your terminal:
```text
[/Users/wenqingzong/Projects/crab_dbg/examples/example.py:76:5] pai = 3.14
[/Users/wenqingzong/Projects/crab_dbg/examples/example.py:76:5] ultimate_answer = 42
[/Users/wenqingzong/Projects/crab_dbg/examples/example.py:76:5] flag = True
[/Users/wenqingzong/Projects/crab_dbg/examples/example.py:76:5] fruits = [
    'apple',
    'peach',
    'watermelon'
]
[/Users/wenqingzong/Projects/crab_dbg/examples/example.py:76:5] country_to_capital_cities = {
    China: Beijing
    United Kingdom: London
    Liyue: Liyue Harbor
}
[/Users/wenqingzong/Projects/crab_dbg/examples/example.py:85:5] country_to_capital_cities = {
    China: Beijing
    United Kingdom: London
    Liyue: Liyue Harbor
}
[/Users/wenqingzong/Projects/crab_dbg/examples/example.py:88:5] 1 + 1 = 2
[/Users/wenqingzong/Projects/crab_dbg/examples/example.py:92:5] linked_list = LinkedList {
    start: Node {
        val: 0
        next: Node {
            val: 1
            next: None
        }
    }
}
[/Users/wenqingzong/Projects/crab_dbg/examples/example.py:95:5] [linked_list, linked_list] = [
    LinkedList {
        start: Node {
            val: 0
            next: Node {
                val: 1
                next: None
            }
        }
    },
    LinkedList {
        start: Node {
            val: 0
            next: Node {
                val: 1
                next: None
            }
        }
    }
]
[/Users/wenqingzong/Projects/crab_dbg/examples/example.py:95:5] (linked_list, linked_list) = (
    LinkedList {
        start: Node {
            val: 0
            next: Node {
                val: 1
                next: None
            }
        }
    },
    LinkedList {
        start: Node {
            val: 0
            next: Node {
                val: 1
                next: None
            }
        }
    }
)
[/Users/wenqingzong/Projects/crab_dbg/examples/example.py:95:5] {"a": 1, "b": linked_list} = {
    a: 1
    b: LinkedList {
        start: Node {
            val: 0
            next: Node {
                val: 1
                next: None
            }
        }
    }
}
[/Users/wenqingzong/Projects/crab_dbg/examples/example.py:95:5] [1,2,3,4,] = [
    1,
    2,
    3,
    4
]
[/Users/wenqingzong/Projects/crab_dbg/examples/example.py:111:5] stack = Stack {
    data: [
        LinkedList {
            start: Node {
                val: 0
                next: Node {
                    val: 1
                    next: None
                }
            }
        },
        LinkedList {
            start: Node {
                val: 0
                next: Node {
                    val: 1
                    next: None
                }
            }
        }
    ]
}
[/Users/wenqingzong/Projects/crab_dbg/examples/example.py:113:5] "What if my input is a string?" = 'What if my input is a string?'
[/Users/wenqingzong/Projects/crab_dbg/examples/example.py:117:5] phone = A white phone made by Apple, official price: 1099.
[/Users/wenqingzong/Projects/crab_dbg/examples/example.py:120:5] numpy_array = 
array([[0., 0., 0.],
       [0., 0., 0.]])
[/Users/wenqingzong/Projects/crab_dbg/examples/example.py:123:5] torch_tensor = 
tensor([[0., 0., 0.],
        [0., 0., 0.]], dtype=torch.float64)
[/Users/wenqingzong/Projects/crab_dbg/examples/example.py:126:5]

```

For full executable code please refer to [./examples/example.py](./examples/example.py).

## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](./LICENSE) file for details.
