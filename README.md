# Crab Debugger (crab_dbg)
This repo contains the Python equivalent of Rust's `dbg!()` macro debugging tool, which helps developers inspect variables and expressions during development. The `crab_dbg` function allows users to trace the values of variables, objects, lists, dictionaries, and other data structures in real-time without cluttering their codebase with multiple print statements. Essentially, this function replaces Python's `print()` function altogether. 

## Features
- Easily print values of variables and expressions using the `dbg()` function, eliminating the need for multiple `print()` statements
- Supports primitive types (int, char, str, bool, etc.) along with basic and complex data structures (lists, arrays, NumPy arrays, PyTorch tensors, etc.)
- When `dbg()` is called, the output also includes the file name, line number, and other key info for context
- Able to process multi-line arguments and recursively inspects user-defined classes and nested objects. 

## Installation
- Clone Repo
    - `git clone https://github.com/yourusername/crab_dbg.git`
- When testing out the code in the example.py file, you may need to add this line in before importing crab_dbg:
    - `sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))`
    - This line tells Python to search for the crab_dbg module in the parent directory of the current file which in this case is example.py
- Ensure that you have the correct dependencies installed using pip
- Ensure your Python is up to date amd compatible with the fucntions being used in the program. 

## Example Usage

Case 1:
```
from sys import stderr
import numpy as np
import torch
from crab_dbg import dbg

# Basic variables
pai = 3.14
ultimate_answer = 42
country_to_capital_cities = {
    "China": "Beijing",
    "United Kingdom": "London",
    "Liyue": "Liyue Harbor",
}

dbg(
    pai,
    ultimate_answer,
    country_to_capital_cities,
)
```
Output:
```
[file_path:79:1] pai = 3.14
[file_path:79:1] ultimate_answer = 42
[file_path:88:1] country_to_capital_cities = {
    China: Beijing
    United Kingdom: London
    Liyue: Liyue Harbor
}
```
Case 2: 
```
# You can also use dbg to inspect expressions.
dbg(1 + 1)

# When used with objects, it will show all fields contained by that object.
linked_list = LinkedList.create(2)
dbg(linked_list)
```
Output:
 ```
[file_path:91:1] Expression = 2
[file_path:95:1] Expression = LinkedList {        
    start: Node {
        val: 0
        next: Node {
            val: 1
            next: None
        }
    }
}
```

The result of these code snippets will return  variable names and their corresponding values along with their file_path and line number. This repo also contains tests which you can use to validate that the `dbg()` function works correctly. 

## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](./LICENSE) file for details.
