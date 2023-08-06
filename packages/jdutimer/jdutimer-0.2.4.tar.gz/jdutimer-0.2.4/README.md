# jdutimer
 
Singleton implementation of a timer. This package allows you to measure and summarize executions time.


## Installation

``` console
> pip(3) install (-U) jdutimer
```

## Methods

``` python
def add(self, func, *args)
```
... to measure the execution time of function.

``` python
def pack(self, title)
```
... to put all previous measured functions in a block with a given title.

``` python
def show_block(self, id=-1, unit="ms")
```
... to show execution time of a given block. The id can either be an integer, or a string. Display unit (s, ds, cs, ms) can be modified.

``` python
def show(self, unit="ms")
```
... to show all execution time blocks. Display unit (s, ds, cs, ms) can be modified.

``` python
def rename(self, old, new)
```
... to rename a given block. old can be the id or the name of the block to rename, new has to be a string.


## Example usage

This snippet :
``` python
from jdutimer.timer import Timer

def foo(str):
    print(str)

def bar(num):
    print(num)

timer = Timer()
timer.add(foo, "Hello World!")
timer.add(bar, 42)
timer.pack("Display")

timer.show()
```

Shows this in the console :
``` console
Hello World!
42
Display 
        foo        0.04ms
        bar        0.01ms
                   0.04ms
        -----
        TOTAL      0.04ms
```
