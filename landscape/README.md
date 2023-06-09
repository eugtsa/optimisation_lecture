## What is this?

This is the "Landscape" demonstration of simple optimization methods!

## Why do we need it?

This demo is used to demonstrate different optimization algorithms in "AI crash course: Optimization" lecture.

## How to install game?

Run `make install` in your terminal (MacOS and Ubuntu based distros are supported):

```shell
make install
```

## How to run demo?

```shell
make run algo=annealing 
```

To start the demo with your own custom optimization algorithm put your algo to the ./algos folder. Algorithm module should be named in underscore notation (my_custom_algo) and algorithm class in it should be named the same but in camel case notation (MyCustomAlgo)

To start the demo without the gui, use `run_no_gui` for example:

```shell
make run_no_gui algo=annealing
``` 

### How to write your own algorithm?

In order to write your algorithm you should create class which implements BaseAlgo. BaseAlgo have two methods which you need to implement: ``get_next_iteration`` and ``get_final_value``. Here is an example of the newton.py:


```python
from domain.world import World
from domain.base_algo import BaseAlgo


class Newton(BaseAlgo):
    f_min = None
    
    def get_next_iteration(self, world: World,f,df,ddf) -> float:
        x = world.cur_pos
        x_next = x-df(x)/ddf(x)
        self.f_min = f(x_next)
        return x_next
    
    def get_final_value(self):
        return self.f_min

``` 

### How to plug your algorithm (agent) into eat all dots game

Currently, only python is supported. If you whould like to see any other language here, please mail me - I'll extend this demo to support other languages.

To plug your python algorithm into this game:

- Create new file with your python program (extention ``.py``) in the ``./algos`` folder
- Write your agent class based on the ``BaseAlgo`` in this file (see examples above)
- Your agent class should implement ``get_next_iteration`` and ``get_final_value`` methods (see examples above)
- Name of the class and name of the file should follow the rules:
    - names of the class and file should be semantically the same, but in different notations
    - name of the file should be in [snake_case](https://en.wikipedia.org/wiki/Snake_case) notation
    - name of the class should be in [camel_caps](https://en.wikipedia.org/wiki/Camel_case) (``BumpyCaps``) notation


Check out examples of the last rule:

- ``my_algo.py`` file name -> ``MyAlgo`` class name
- ``super_algo`` file name -> ``SuperAlgo`` class name
- ``sgd_algo`` file name -> ``SgdAlgo`` class name

To run your demo, plug it's file name without ``.py`` extention into any command with ``algo`` argument. For example:

- make run algo=my_algo
- make run_no_gui algo=super_algo

## What commands are supported?

- ``make run`` will run ``monte_carlo`` by default
- ``make run`` command with ``algo=`` argument will run algorithm specified after equal sign with graphical user interface. To advance the demo to the next level you can either:
    - skip the level pressing ``n`` on the keyboard
    - wait until algorith will finish (50 steps) the current level and then press any key on the keyboard
- ``make run`` command with ``scale=`` argument will demo with scaled aspect ratio. Add ``scale=0.5`` to any command if hte window of demonstration is too big
- ``make run_no_gui`` command with ``algo=`` argument will run algorithm specified after equal sign without graphical user interface
- ``make list_algos`` will list all possible algorithms currently available
- ``make install`` will install all dependencies (based in miniconda) into the local demo folder
- ``make clean`` will remove all dependencies, clean up folder

 
## Who is the author?

Evgenii Tsatsorin - eugtsa@gmail.com
