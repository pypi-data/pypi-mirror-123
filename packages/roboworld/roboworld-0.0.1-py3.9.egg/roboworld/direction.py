from enum import Enum, unique


@unique
class Direction(Enum):
    # ccw ordered (y, x)!!!
    EAST = (0, 1)
    NORTH = (1, 0)
    WEST = (0, -1)
    SOUTH = (-1, 0)

    def next(self):
        if self == Direction.EAST:
            return Direction.NORTH
        if self == Direction.NORTH:
            return Direction.WEST
        if self == Direction.WEST:
            return Direction.SOUTH
        else:
            return Direction.EAST

    def to_float(self):
        if self == Direction.EAST:
            return 0.25
        if self == Direction.NORTH:
            return 0.5
        if self == Direction.WEST:
            return 0.75
        else:
            return 1.0
