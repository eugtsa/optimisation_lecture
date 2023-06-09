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

To start the game without the gui, use `run_no_gui` for example:

```shell
make run_no_gui algo=annealing
``` 

### How to write your own algorithm?

In order to write your algorithm you should create class which implements BaseAlgo. BaseAlgo have two methods which you need to implement: ``get_action``. Here is an example of the naive_random_walk_agent.py:


```python
import random

from domain.action import Action
from domain.world import World
from domain.base_agent import BaseAgent


class NaiveRandomWalkAgent(BaseAgent):
    def get_action(self, world: World) -> Action:
        # taking random actions!
        return random.choice([Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT])
``` 

As you can see, naive random walk agent does not take any information about the ``world`` variable at all! It just return random action.

Here is another example, where you can see the usage of world information. This one is a random walk agent which is not bumping into the walls:


```python
import random

from domain.action import Action
from domain.world import World
from domain.base_agent import BaseAgent
from domain.point import Point


class RandomWalkAgent(BaseAgent):
    def get_action(self, world: World) -> Action:
        allowed_actions = list()

        cur_pos = world.cur_pos
        # let's not bump into walls to avoid -3 penalty
        if Point(cur_pos.x - 1, cur_pos.y) not in world.map.walls:
            allowed_actions.append(Action.LEFT)
        if Point(cur_pos.x + 1, cur_pos.y) not in world.map.walls:
            allowed_actions.append(Action.RIGHT)
        if Point(cur_pos.x, cur_pos.y - 1) not in world.map.walls:
            allowed_actions.append(Action.UP)
        if Point(cur_pos.x, cur_pos.y + 1) not in world.map.walls:
            allowed_actions.append(Action.DOWN)

        return random.choice(allowed_actions)
``` 

As you can see, this agent will first create the list of allowed actions and get random one from the list. 

### How to plug your algorithm (agent) into eat all dots game

Currently, only python is supported. If you whould like to see any other language here, please mail me - I'll extend this game to support other languages.

To plug your python agent into this game:

- Create new file with your python program (extention ``.py``) in the ``./agents`` folder
- Write your agent class based on the ``BaseAgent`` in this file (see examples above)
- Your agent class should implement ``get_action`` method (see examples above)
- Name of the class and name of the file should follow the rules:
    - names of the class and file should be semantically the same, but in different notations
    - name of the file should be in [snake_case](https://en.wikipedia.org/wiki/Snake_case) notation
    - name of the class should be in [camel_caps](https://en.wikipedia.org/wiki/Camel_case) (``BumpyCaps``) notation


Check out examples of the last rule:

- ``my_agent.py`` file name -> ``MyAgent`` class name
- ``super_agent`` file name -> ``SuperAgent`` class name
- ``wtf_agent`` file name -> ``WtfAgent`` class name

To run your agent, plug it's file name without ``.py`` extention into any command with ``agent`` argument. For example:

- make run agent=my_agent
- make run_no_gui agent=super_agent

## What commands are supported?

- ``make run`` will run ``keyboard_agent`` by default
- ``make run`` command with ``agent=`` argument will run agent specified after equal sign with graphical user interface. To advance the agent to the next level you can either:
    - skip the level pressing ``n`` on the keyboard
    - wait until agent will finish the current level and then press any key on the keyboard
- ``make run_no_gui`` command with ``agent=`` argument will run agent specified after equal sign without graphical user interface
- ``make list_agents`` will list all possible agents currently available
- ``make install`` will install all dependencies (based in miniconda) into the local game folder
- ``make clean`` will remove all dependencies

 
## Who is the author?

Evgenii Tsatsorin - eugtsa@gmail.com
