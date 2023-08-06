
<img src="elba.png" alt="drawing" width="500"/>


# elba

`elba` is a Python-based software for graph-based data persistence. It has the following features:

* Disk-caching hashable data 
* Workflow caching, i.e. end-to-end data optimization rather than at the single-function level.
* Coming soon: JAX support for automatic differentiation

## Install

`elba` is on the `pypi` repository, and relies on `mpi` libraries

```bash
apt-get update
apt-get install build-essential libopenmpi-dev libgmsh-dev
pip install --upgrade --no-cache elba
```

To start using `elba`, we need to initialize it

```bash
elba init
```

## The rationale

The main purpose of `elba` is data persistence at the workflow level, that is: assume `f1` takes `a` and gives `b` and `f2` takes `b` and gives `c`; then if we run this workflow twice with the same `a`, then only `c` is loaded, instead of `b` and `c` (assuming caching at the single-function level). This approach may save significant computing time for large computational graphs where only some of the nodes are fed with different sets of data. 

## Caching

To cache a function's output, we simply use the decorator `elba`

```python
from elba import elba,get,config
config.set_debug(True)

@elba
def add(a,b):
    return a + b

print(get(add(1.0,2.0)))
```

```bash
RUN add
3.0
```

If we run the same script again, the function `add` is not run. Note that data is retrieved with the command `get`.

```bash
LOAD add
3.0
```


## Function composition

The key feature of `elba` is graph-based caching, i.e. data is loaded only when needed across the entire computational graph. Here is an example:

```python
@elba
def multiply(c,d):

    return c*d

print(get(multiply(add(1.0,2.0),3.0)))

```

```bash
RUN multiply
LOAD c version: 0
TRANSLATE add -> c

9.0
```

Then, if we run it again, we simply get
```bash
LOAD multiply version: 0
9.0
```

Note that the output of `add` is not loaded.


## Author

Giuseppe Romano (romanog@mit.edu)













