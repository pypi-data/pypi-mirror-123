from enum import Enum
import copy
import numpy as np
import random

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import animation, rc

from roboworld.direction import Direction
from .roboexception import InvalidWorldArgumentsExeception, ObjectMissingException, ObjectInFrontException, CellOccupiedException
from .cellstate import CellState
from .agent import Agent


class World():
    def __init__(self, nrows, ncols, cells=None, agent_direction=Direction.NORTH, agent_position=None, goal_position=None) -> None:
        if nrows == 0 or ncols == 0 or (cells != None and (len(cells) == 0 or len(cells[0]) == 0)):
            raise InvalidWorldArgumentsExeception()
        self.stack = []
        self.ncols = ncols
        self.nrows = nrows
        self.animation_active = True
        if cells == None:
            self.cells = [
                [CellState.EMPTY for _ in range(ncols)] for _ in range(nrows)]
        elif nrows != len(cells) or ncols != len(cells[0]):
            raise InvalidWorldArgumentsExeception()
        else:
            self.cells = cells

        if agent_position == None:
            agent_position = self.__find_cell(CellState.AGENT)

        if goal_position == None:
            goal_position = self.__find_cell(CellState.GOAL)

        if agent_position == None:
            agent_position = [self.nrows // 2, self.ncols // 2]
        self.agent = Agent(agent_position, self,
                           agent_direction=agent_direction)

        if goal_position == None:
            while goal_position == None or (goal_position == agent_position and (ncols > 1 or nrows > 1)):
                goal_position = [np.random.randint(0, nrows),
                                 np.random.randint(0, ncols)]

        self.goal = goal_position

        #self.objects = []
        self.tokens = []

        self.cells[agent_position[0]][agent_position[1]] = CellState.AGENT
        self.cells[self.goal[0]][self.goal[1]] = CellState.AGENT
        self.marks = [
            [False for _ in range(ncols)] for _ in range(nrows)]
        self.push()

    def disable_animation(self):
        self.animation_active = False

    def enable_animation(self):
        self.animation_active = True

    def is_successful(self):
        return self.agent.position == self.goal

    def get_state(self, row, col):
        return self.cells[row][col]

    def set_state(self, row, col, state):
        self.cells[row][col] = state

    def get_goal_position(self):
        return self.goal

    def is_object_at(self, row, col):
        return self.get_state(row, col) == CellState.OBJECT

    def get_object_at(self, row, col):
        if self.is_object_at(row, col):
            result = self.get_state(row, col)
            self.set_state(row, col, CellState.EMPTY)
            return result
        else:
            raise ObjectMissingException()

    def set_object_at(self, row, col):
        if self.is_object_at(row, col):
            raise CellOccupiedException()
        else:
            self.set_state(row, col, CellState.OBJECT)

    def set_mark_at(self, row, col):
        if self.is_object_at(row, col):
            raise CellOccupiedException()
        else:
            self.marks[row][col] = True

    def unset_mark_at(self, row, col):
        if self.is_object_at(row, col):
            raise CellOccupiedException()
        else:
            self.marks[row][col] = False

    def is_mark_at(self, row, col):
        return self.marks[row][col]

    def values(self):
        values = [[state.value for state in row] for row in self.cells]
        values[self.goal[0]][self.goal[1]] = CellState.GOAL.value
        values[self.agent.position[0]
               ][self.agent.position[1]] = CellState.AGENT.value + self.agent.headway.to_float()
        return values

    def get_robo(self):
        return self.agent

    def push(self):
        if self.animation_active:
            self.stack.append(self.values())

    def pop(self):
        if len(self.stack) > 0:
            return self.stack.pop()
        return None

    def get_animation(self, interval=150, save=False, dpi=80):
        if len(self.stack) <= 1:
            return
        stack_copy = copy.deepcopy(self.stack)
        scale = 0.5
        fig = plt.figure(figsize=(self.ncols * scale,
                         self.nrows * scale), dpi=dpi)
        fig.subplots_adjust(left=0, bottom=0, right=1,
                            top=1, wspace=None, hspace=None)
        ax = fig.add_subplot(1, 1, 1)
        ax.grid(which='both')
        matplt = ax.matshow(
            stack_copy[0], interpolation='nearest', vmin=0, vmax=3)
        x_ticks = np.arange(-0.5, self.ncols+1, 1)
        y_ticks = np.arange(-0.5, self.nrows+1, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xticks(x_ticks, minor=True)
        ax.set_yticks(y_ticks, minor=True)
        ax.set_xlim(-0.5, self.ncols-0.5)
        ax.set_ylim(-0.5, self.nrows-0.5)

        i = {'index': 0}  # trick to enforce sideeffect

        def updatefig(*args):
            i['index'] += 1
            if i['index'] >= len(stack_copy):
                i['index'] = 0
            matplt.set_array(stack_copy[i['index']])
            return matplt,

        plt.close()
        anim = animation.FuncAnimation(
            fig, updatefig, interval=interval, blit=True, save_count=len(stack_copy))
        if save:
            anim.save('robo-world-animation.gif',
                      dpi=dpi, writer='imagemagick')
        self.stack.clear()
        self.push()
        return anim

    def show(self):
        scale = 0.5
        fig = plt.figure(figsize=(self.ncols * scale,
                         self.nrows * scale), dpi=80)
        ax = fig.add_subplot(1, 1, 1)
        x_ticks = np.arange(-0.5, self.ncols+1, 1)
        y_ticks = np.arange(-0.5, self.nrows+1, 1)
        values = self.values()
        # values = np.random.random((self.nrows, self.ncols))
        ax.grid(which='both')
        ax.matshow(values,  interpolation='nearest', vmin=0,
                   vmax=CellState.GOAL.value)  # vmin=0, vmax=5,cmap='gray',
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xticks(x_ticks, minor=True)
        ax.set_yticks(y_ticks, minor=True)
        ax.set_xlim(-0.5, self.ncols-0.5)
        ax.set_ylim(-0.5, self.nrows-0.5)
        plt.close()
        return fig

    def __find_cell(self, cellstate):
        for i, col in enumerate(self.cells):
            for j, state in enumerate(col):
                if state == cellstate:
                    return [i, j]
        return None

    @staticmethod
    def corridor(length=10, random_headway=False, nobjects=0):

        objects = [CellState.OBJECT for _ in range(min(nobjects, length-2))]
        emptys = [CellState.EMPTY for _ in range(length-2-len(objects))]
        combined = objects + emptys
        random.shuffle(combined)

        cells = [[CellState.AGENT] + combined + [CellState.GOAL]]

        agent_direction = Direction.EAST
        if random_headway:
            agent_direction = random.choice(
                [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST])
        return World(nrows=len(cells), ncols=len(cells[0]), cells=cells, agent_direction=agent_direction)

    @ staticmethod
    def maze():
        text = """N#---#---#---
-#-#-#-#-#-#-
-#-#-#-#-#-#-
-#-#-#-#-#-#-
-#-#-#-#-#-#-
---#---#---#G"""
        return World.str_to_world(text)

    @staticmethod
    def complex_maze(nrows=10, ncols=10, agent_direction=None):
        cells = [[CellState.OBSTACLE for _ in range(
            ncols)] for _ in range(nrows)]

        visited = [[False for _ in range(
            ncols)] for _ in range(nrows)]

        stack = []
        start = (np.random.randint(0, nrows), np.random.randint(0, ncols))

        def moore(pos):
            return [(pos[0]-1, pos[1]), (pos[0]-1, pos[1]+1), (pos[0], pos[1]+1), (pos[0]+1, pos[1]+1), (pos[0]+1, pos[1]), (pos[0]+1, pos[1]-1), (pos[0], pos[1]-1), (pos[0]-1, pos[1]-1)]

        def critical(pos):
            l1 = [(pos[0]-1, pos[1]), (pos[0]-1, pos[1]+1), (pos[0], pos[1]+1)]
            l2 = [(pos[0], pos[1]+1), (pos[0]+1, pos[1]+1), (pos[0]+1, pos[1])]
            l3 = [(pos[0]+1, pos[1]), (pos[0]+1, pos[1]-1), (pos[0], pos[1]-1)]
            l4 = [(pos[0], pos[1]-1), (pos[0]-1, pos[1]-1), (pos[0]-1, pos[1])]
            return [l1, l2, l3, l4]

        def contains(pos):
            return pos[0] >= 0 and pos[1] >= 0 and pos[0] < nrows and pos[1] < ncols

        def get_neighbours(position):
            return [pos for pos in [
                (position[0] + 1, position[1]),
                (position[0] - 1, position[1]),
                (position[0], position[1] + 1),
                (position[0], position[1] - 1)] if contains(pos)]

        def random_neighbour(position):
            tmp_neighbours = get_neighbours(position)
            neighbours = []
            for neighbour in tmp_neighbours:
                if not visited[neighbour[0]][neighbour[1]]:
                    neighbours.append(neighbour)

            if len(neighbours) > 0:
                return random.choice(neighbours)
            else:
                return None

        def mark(position):
            visited[position[0]][position[1]] = True
            cells[position[0]][position[1]] = CellState.EMPTY
            for nh in moore(position):
                test_positions = critical(nh)
                for test_pos in test_positions:
                    if all(map(lambda e: contains(e) and cells[e[0]][e[1]] == CellState.EMPTY, test_pos)):
                        visited[nh[0]][nh[1]] = True
                        cells[nh[0]][nh[1]] = CellState.OBSTACLE
                        break

        stack.append(start)
        end = start
        max_distance = 0
        while len(stack) > 0:
            next = random_neighbour(stack[-1])
            # dead end
            if next == None:
                stack.pop()
            else:
                mark(next)
                stack.append(next)
                if max_distance < len(stack):
                    max_distance = len(stack)
                    end = next

        if agent_direction == None:
            agent_direction = random.choice(
                [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST])

        cells[start[0]][start[1]] = CellState.AGENT
        cells[end[0]][end[1]] = CellState.GOAL

        return World(nrows=len(cells), ncols=len(cells[0]), cells=cells, agent_direction=agent_direction)

    @ staticmethod
    def str_to_world(text):
        cells = []
        agent_direction = Direction.EAST
        for row, line in enumerate(text.splitlines()):
            cells.append([])
            for c in line:
                if c in ['N', 'S', 'E', 'W', 'R']:
                    state = CellState.AGENT
                    if c == 'N':
                        agent_direction = Direction.NORTH
                    elif c == 'S':
                        agent_direction = Direction.SOUTH
                    elif c == 'W':
                        agent_direction = Direction.WEST
                    elif c == 'W':
                        agent_direction = Direction.EAST
                    else:
                        agent_direction = random.choice(
                            [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST])
                elif c == '#':
                    state = CellState.OBSTACLE
                elif c == 'G':
                    state = CellState.GOAL
                else:
                    state = CellState.EMPTY
                cells[row].append(state)
        return World(nrows=len(cells), ncols=len(cells[0]), cells=cells, agent_direction=agent_direction)
