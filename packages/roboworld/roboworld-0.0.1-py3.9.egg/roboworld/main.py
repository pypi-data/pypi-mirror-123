from .world import World
import random


def threeRightAndUp():
    world = World(nrows=5, ncols=10)
    agent = world.get_agent()
    agent.move_right()
    agent.move_right()
    agent.move_right()
    agent.move_up()
    agent.move_up()
    agent.move_up()
    anim = world.get_animation()
    anim.save('./asserts/steps.gif', writer='imagemagick')


def randomWalk():
    world = World(nrows=5, ncols=10)
    agent = world.get_agent()
    while not agent.reached_goal():
        move = random.choice(
            [agent.move_right, agent.move_left, agent.move_up, agent.move_down])
        move()

    anim = world.get_animation()
    anim.save('./asserts/random-walk.gif', writer='imagemagick')


def randomWalkImproved():
    world = World(nrows=5, ncols=10)
    agent = world.get_agent()
    while not agent.reached_goal():
        choices = []
        if agent.can_move_left():
            choices.append(agent.move_left)
        if agent.can_move_right():
            choices.append(agent.move_right)
        if agent.can_move_up():
            choices.append(agent.move_up)
        if agent.can_move_down():
            choices.append(agent.move_down)
        move = random.choice(choices)
        move()

    anim = world.get_animation()
    anim.save('./asserts/random-walk-improved.gif', writer='imagemagick')


def deterministicWalk():
    world = World(nrows=5, ncols=10)
    agent = world.get_agent()

    while not agent.reached_goal() and agent.can_move_left():
        agent.move_left()

    while not agent.reached_goal() and agent.can_move_up():
        agent.move_up()

    while not agent.reached_goal() and count > 0:
        while not agent.reached_goal() and agent.can_move_down():
            agent.move_down()
        if not agent.reached_goal():
            agent.move_right()
        while not agent.reached_goal() and agent.can_move_up():
            agent.move_up()
        if not agent.reached_goal():
            agent.move_right()

    anim = world.get_animation()
    anim.save('./asserts/deterministic-walk.gif', writer='imagemagick')


if __name__ == "__main__":
    threeRightAndUp()
    randomWalk()
    randomWalkImproved()
    deterministicWalk()
