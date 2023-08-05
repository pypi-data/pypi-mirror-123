# Bodo IPython Magic
[![Build](https://github.com/Bodo-inc/bodo-magic/actions/workflows/build.yml/badge.svg)](https://github.com/Bodo-inc/bodo-magic/actions/workflows/build.yml)

The Bodo IPython Magic is used to write simpler Python code with `bodo`. For example, you can take the following code:

```python
import bodo
import pandas as pd

@bodo.jit
def test():
  return pd.read_parquet('sample.pq')

df = test()
```
and (using the `%%bodo` magic) convert it to:
```python
%%bodo
import pandas as pd

df = pd.read_parquet('sample.pq)
```

## Why a Magic?
When presenting `bodo`, we like to use very simple examples like loading a CSV file, performing some simple operations, and so on. However, these cases generally look longer and more compilected in comparison to competing solutions like `pyspark`, `dask`, `ray`, and so on. This magic is intended to target these issues.

## Arguments
```
%bodo [-v] [-c] [-d] [-o [OUTPUTS [OUTPUTS ...]]]

optional arguments:
  -v, --verbose         Print Verbose and Debugging Info
  -c, --cache           Enable Caching on the Wrapped Function
  -d, --dry-run         Do Not Execute Any Code or Wrapper Function
  -o <[OUTPUTS [OUTPUTS ...]]>, --outputs <[OUTPUTS [OUTPUTS ...]]>
                        Variables to Output from the Wrapped Function (default: Returns All Defined Variables)
```

## Supported Features
- Inserts `import bodo` automatically
- Imports
- Automatically adds the `@bodo.jit` decorator to any function in the code cell
