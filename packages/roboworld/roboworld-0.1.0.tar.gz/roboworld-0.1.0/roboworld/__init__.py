__version__ = '0.1.0'
__author__ = 'Benedikt Zoennchen'

from .agent import Agent
from .world import World
from IPython.display import HTML, display


def animate(world):
    anim = world.get_animation(save=True)
    if anim != None:
        display(HTML(anim.to_jshtml()))


def corridor(length=10, random_headway=False, nobjects=0):
    return World.corridor(length=length, random_headway=random_headway, nobjects=nobjects)


def maze():
    return World.maze()


def str_to_world(text):
    return World.str_to_world(text)


def new_world(nrows=5, ncols=9, agent_position=None, goal_position=None):
    return World(nrows=nrows, ncols=ncols, agent_position=agent_position, goal_position=goal_position)


def complex_maze(nrows=10, ncols=10, agent_direction=None):
    return World.complex_maze(nrows=nrows, ncols=ncols, agent_direction=agent_direction)
