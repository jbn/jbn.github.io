#!/usr/bin/env python
import sys

EMPTY_PY_CELL = """```python

```"""

print(sys.stdin.read().replace(EMPTY_PY_CELL, ""))
