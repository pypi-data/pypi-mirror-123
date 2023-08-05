# 1. Cartorio

A wrapper on the `logging` module for Python that provides a simple and easy to use interface for logging.

# 2. Contents
- [1. Cartorio](#1-cartorio)
- [2. Contents](#2-contents)
- [3. Installation](#3-installation)
- [4. Usage](#4-usage)

# 3. Installation
```bash
pip install cartorio
```

# 4. Usage
Example:

```python
import sys
from pathlib import Path

from cartorio import fun, log

# Test instantiation of log file
logger = log(filename=Path(__file__).resolve().stem, logs_path=Path(__file__).resolve().parent)

@fun
def multiply(num1, num2):
    return num1 * num2

# Test if entry and exit log messages are correct
multiply(10, 1)
```