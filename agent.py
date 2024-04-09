from coordinates import Coordinates
from enum import Enum
from random import randint
from entity import Entity


class Direction(Enum):
    DOWN = 0
    UP = 2
    RIGHT = 3
    LEFT = 1
    
    @staticmethod
    def From(d: int):
        if d < Direction.DOWN.value or d > Direction.RIGHT.value:
            raise ValueError('Unknown direction provided.')
        for v in (Direction.DOWN, Direction.LEFT, Direction.UP, Direction.RIGHT):
            if v.value == d:
                return v
    @staticmethod
    def Random():
        return Direction.From(randint(Direction.DOWN.value, Direction.RIGHT.value))
    
    
class Agent(Entity):
    
    def __init__(self, imagePath: str, position: Coordinates | None = None) -> None:
        super().__init__(id=0, name="Smart Agent", imagePath=imagePath, position=position)
        self.direction: Direction = Direction.Random()
