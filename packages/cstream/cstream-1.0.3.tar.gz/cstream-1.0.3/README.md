# cstream
### C/C++ Style Colorful output stream for Python with level control and thread/process safety options.

<br>
<br>

## Installation
```bash
$ pip install cstream
```

## Introduction
Default `stderr`, `stdwar` and `stdlog` instances are directed to standard error output. Note that `stdout` is also available.

The `devnull` stram is intended to be used as a context manager in order to supress output directed to *stderr* and *stdout*.

Verbosity level control is coherent with the `logging` module and its constants are made available form importing.

## Examples
```python
from cstream import CStream, stderr, stdout, stdlog, stdwar, devnull, WARNING

# Set debug level
CStream.config(level=WARNING)

# Will be printed
stderr << "Error: You are 'redly' wrong"

# Gets printed also
stdwar << "Warning: Just a 'yellowish' warning..."

# Bypassed
stdlog << "DEBUG: Some blue text printed to stderr"

# Suppress all output written to stdout and stderr
with devnull:
    print("Bye World?")
```

## Threads and Multiprocessing
```python
from cstream import CStream

# For usage within threads
CStream.config(lock_type=CStream.T_LOCK)

# For multiprocessing
CStream.config(lock_type=CStream.P_LOCK)

# When no lock is needed (Default)
CStream.config(lock_type=None)
```

## Next steps:
- Complete `logging` integration.
- Thread-safe logging.