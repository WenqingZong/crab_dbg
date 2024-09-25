# Crab Debugger (crab_dbg)

This repo contains the Python equivalent of Rust's `dbg!()` macro debugging tool, which helps developers inspect variables and expressions during development. The `crab_dbg` function allows users to trace the values of variables, objects, lists, dictionaries, and other data structures in real-time without cluttering their codebase with multiple print statements. 

## Features
- Easily print values of variables and expressions using `crab_dbg()` function, eliminating the need for multiple `print` statements
- Supports basic data structures (lists, arrays, etc) including primitive types
- Able to use custom repr support to show variable's value if a class has a custom repr or str method
- Allows you to redirect output to stderr or a custom file for debugging purposes

## Installation
- Clone Repo
    - `git clone https://github.com/yourusername/crab_dbg.git`
- Install requriements.txt
    - `pip install -r requirements.txt`

## Example Usge

```
from crab_dbg import dbg

pai = 3.14
ultimate_answer = 42
flag = True
fruits = ["apple", "peach", "watermelon"]

dbg(pai, ultimate_answer, flag, fruits)

```

The result of this code will return the variable names and their corresponding values. This repo also contains tests which you can use to vaidate that crab_dbg works correctly. 

## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](./LICENSE) file for details.
