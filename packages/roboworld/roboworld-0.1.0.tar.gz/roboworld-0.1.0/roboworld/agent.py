from .cellstate import CellState
from .direction import Direction
from .roboexception import WallInFrontException, ObjectMissingException, SpaceIsFullException, SpaceIsEmptyException, ObjectInFrontException
import random


class Agent():
    def __init__(self, position, world, agent_direction=Direction.EAST, print_actions=True) -> None:
        self.world = world
        self.position = position
        self.headway = agent_direction
        self.object = None
        self.marks = 0
        self.print_actions = print_actions

    def disable_print(self):
        self.print_actions = False

    def enable_print(self):
        self.print_actions = True

    def print(self, fstring):
        if self.print_actions:
            print(fstring)

    # non-privates
    def is_object_in_front(self):
        return self.__get_state_at(self.headway) == CellState.OBJECT

    def take(self):
        if self.object != None:
            raise SpaceIsFullException()
        if self.is_wall_in_front():
            raise WallInFrontException()
        if not self.is_object_in_front():
            raise ObjectMissingException()
        self.object = self.world.get_object_at(*self.__front())
        self.print(f'takes {self.object}')

    def put(self):
        if not self.is_carrying_object():
            raise SpaceIsEmptyException()
        if self.is_wall_in_front():
            raise WallInFrontException()
        if self.is_object_in_front():
            raise ObjectInFrontException()

        self.world.set_object_at(*self.__front())
        self.print(f'puts {self.object}')
        self.object = None

    def front_is_clear(self):
        return not self.is_wall_in_front()

    def is_mark_in_front(self) -> bool:
        return self.front_is_clear() and self.__is_mark_at(self.headway)

    def is_wall_in_front(self) -> bool:
        return not self.__is_reachable(self.headway)

    def move(self):
        before = [self.position[0], self.position[1]]
        if self.is_wall_in_front():
            raise WallInFrontException()
        if self.is_object_in_front():
            raise ObjectInFrontException()
        self.position[0] += self.headway.value[0]
        self.position[1] += self.headway.value[1]
        self.world.set_state(*before, CellState.EMPTY)
        self.world.set_state(*self.position, CellState.AGENT)

        # if self.is_carrying_object():
        #    self.object.set_position(self.position)
        self.world.push()
        self.print(
            f'move ({before[1]},{before[0]}) -> ({self.position[1]},{self.position[0]})')
        return self.position

    def set_mark(self):
        self.world.set_mark_at(*self.position)
        self.print(f'mark ({self.position[1]},{self.position[0]})')

    def unset_mark(self):
        self.world.unset_mark_at(*self.position)
        self.print(f'remove mark ({self.position[1]},{self.position[0]})')

    def is_carrying_object(self) -> bool:
        return self.object != None

    def turn_left(self):
        before = self.headway
        self.headway = self.headway.next()
        self.print(f'turn {before} -> {self.headway}')

    def is_facing_north(self) -> bool:
        return self.headway == Direction.NORTH

    def toss(self):
        toss = random.randint(0, 1) == 1
        self.print(f'toss {toss}')
        return toss

    def is_at_goal(self):
        return self.position[0] == self.world.goal[0] and self.position[1] == self.world.goal[1]

    def __get_state_at(self, direction) -> CellState:
        y, x = self.position
        if direction == Direction.WEST:
            return self.world.get_state(y, x-1)
        elif direction == Direction.EAST:
            return self.world.get_state(y, x+1)
        elif direction == Direction.NORTH:
            return self.world.get_state(y+1, x)
        else:
            return self.world.get_state(y-1, x)

    def __is_mark_at(self, direction) -> bool:
        y, x = self.position
        if direction == Direction.WEST:
            return self.world.is_mark_at(y, x-1)
        elif direction == Direction.EAST:
            return self.world.is_mark_at(y, x+1)
        elif direction == Direction.NORTH:
            return self.world.is_mark_at(y+1, x)
        else:
            return self.world.is_mark_at(y-1, x)

    def __is_reachable(self, direction) -> bool:
        y, x = self.position
        if direction == Direction.WEST:
            return x-1 >= 0 and self.world.get_state(y, x-1) != CellState.OBSTACLE
        elif direction == Direction.EAST:
            return x+1 < self.world.ncols and self.world.get_state(y, x+1) != CellState.OBSTACLE
        elif direction == Direction.NORTH:
            return y+1 < self.world.nrows and self.world.get_state(y+1, x) != CellState.OBSTACLE
        else:
            return y-1 >= 0 and self.world.get_state(y-1, x) != CellState.OBSTACLE

    def __front(self):
        return self.position[0] + self.headway.value[0], self.position[1] + self.headway.value[1]

    def __back(self):
        return self.position[0] - self.headway.value[0], self.position[1] - self.headway.value[1]

    # These methods should be implemented by the students in excercises!
    def __turn(self) -> int:
        self.turn_left()
        self.turn_left()
        return 2

    def __turn_right(self) -> int:
        self.turn_left()
        self.turn_left()
        self.turn_left()
        return 3

    def __turn_to_north(self) -> int:
        turns = 0
        while not self.is_facing_north():
            self.turn_left()
            turns += 1
        return turns

    def __turn_to_south(self) -> int:
        turns = self.__turn_to_north()
        turns += self.__turn()
        return turns

    def __turn_to_east(self) -> int:
        turns = self.__turn_to_south()
        self.turn_left()
        return turns + 1

    def __turn_to_west(self) -> int:
        turns = self.__turn_to_north()
        self.turn_left()
        return turns + 1

    def __reverse_turns(self, turns):
        for _ in range(4 - (turns % 4)):
            self.turn_left()

    def __is_wall_at(self, direction) -> bool:
        if direction == Direction.NORTH:
            turns = self.__turn_to_north()
        elif direction == Direction.EAST:
            turns = self.__turn_to_east()
        elif direction == Direction.SOUTH:
            turns = self.__turn_to_south()
        else:
            turns = self.__turn_to_west()
        result = self.is_wall_in_front()
        self.__reverse_turns(turns)
        return result

    def __is_wall_at_west(self) -> bool:
        return self.__is_wall_at(Direction.WEST)

    def __is_wall_at_east(self) -> bool:
        return self.__is_wall_at(Direction.EAST)

    def __is_wall_at_north(self) -> bool:
        return self.__is_wall_at(Direction.NORTH)

    def __is_wall_at_south(self) -> bool:
        return self.__is_wall_at(Direction.SOUTH)

    def __move_west(self):
        self.__turn_to_west()
        return self.move()

    def __move_east(self):
        self.__turn_to_east()
        return self.move()

    def __move_north(self):
        self.__turn_to_north()
        return self.move()

    def __move_south(self):
        self.__turn_to_south()
        return self.move()

    # methods for testing
    def __get_direction(self):
        return self.headway
