# smalltime

<p align="center">
    <img src="https://github.com/nicklambourne/smalltime/raw/master/docs/source/_static/img/smalltime.png" width="250px"/>
</p>

---

![GitHub](https://img.shields.io/github/license/nicklambourne/smalltime)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/smalltime)]()
![PyPI](https://img.shields.io/pypi/v/smalltime)
![PyPI - Downloads](https://img.shields.io/pypi/dm/smalltime)
[![Test](https://github.com/nicklambourne/smalltime/actions/workflows/test.yml/badge.svg)](https://github.com/nicklambourne/smalltime/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/nicklambourne/smalltime/branch/master/graph/badge.svg?token=QBZ9WK9PFA)](https://codecov.io/gh/nicklambourne/smalltime)
[![Read the Docs](https://img.shields.io/readthedocs/smalltime)](https://smalltime.readthedocs.io/en/latest/)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

## What is it?
`smalltime` is a quick and dirty library for timing Python function, sections of code and arbitrary programs on the command line.

---

## Requirements
`smalltime` requires Python >= 3.6.2.

See [`pyproject.toml`](https://github.com/nicklambourne/smalltime/blob/master/pyproject.toml) for dependencies and dev dependencies.

---

## Installation

Via [`poetry`](https://python-poetry.org/):
```bash
poetry add smalltime
```

Via `pip`:
```bash
pip install smalltime
```

---

## Basic Usage
### In Python Code
#### In-Line
```python
import smalltime

timer = smalltime.Timer(name="hello world timer")
timer.start()
print("Hello, ", end="")
print("World!")
timer.stop()
```

#### Via Decorator
```python
import smalltime
import subprocess

@smalltime.timed(name="thing_timer")
def thing_you_want_to_time():
    subprocess.call(["python", "-c", "\"import this\""])


thing_you_want_to_time()
```

### From the Command Line
N.B.: Assumes installation via Poetry and an active [Poetry shell](https://python-poetry.org/docs/cli/#shell).
```bash
# Usage: st <program> [args]
st sleep 10
Starting counter (BNM8rBqP)
Counter stopped (BNM8rBqP): 10007777130ns elapsed
```

---

## Can I use this in my project?
Yes, please do! The code is all open source and BSD-3-Clause licensed.

---