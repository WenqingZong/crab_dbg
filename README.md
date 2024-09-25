# Crab Debugger (crab_dbg)

This repo contains the Python equivalent of Rust's `dbg!()` macro debugging tool, which helps developers inspect variables and expressions during development. The `crab_dbg` function allows users to trace the values of variables, objects, lists, dictionaries, and other data structures in real-time without cluttering their codebase with multiple print statements. 

## Features
- Easily print values of variables and expressions using `crab_dbg()` function, eliminating the need for multiple `print` statements
- Supports primitive types (int, char, str, bool, etc.) along with basic and complex data structures (lists, arrays, NumPy arrays, PyTorch tensors, etc.)
- Able to use custom repr support to show variable's value in a human-readable format if a class has a custom repr or str method
- Allows you to redirect output to stderr or a custom file for debugging purposes
- When `dbg()` is called, the output also includes the file name, line number, and other key info for context
- Able to process multi-line arguments and recursively inspects user-defined classes and nested objects. 

## Installation
- Clone Repo
    - `git clone https://github.com/yourusername/crab_dbg.git`
- Install requriements.txt
    - `pip install -r requirements.txt`

## Example Usage

Case 1:
```
from crab_dbg import dbg
import numpy as np
import torch

# Basic variables
x = 42
y = "hello"
dbg(x, y)
```
Output:
```
[<file>:<line>:<col>] x = 42
[<file>:<line>:<col>] y = hello
```
Case 2: 
```
arr = np.array([1, 2, 3])
tensor = torch.tensor([4, 5, 6])
dbg(arr, tensor)
```
Output:
 ```
[1 2 3]
 tensor([4, 5, 6])
```

The result of this code will return the variable names and their corresponding values. This repo also contains tests which you can use to validate that crab_dbg works correctly. 

## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](./LICENSE) file for details.
