from random import randint
from typing import Union
from enum import Enum


class Coordinates:
    
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x: int = x 
        self.y: int = y
        
    @staticmethod
    def Random(x_max = 7, y_max = 7):
        return Coordinates(randint(1, x_max), randint(1, y_max))
    
    def Randomize(self, x_max = 7, y_max = 7):
        self.x, self.y = randint(1, x_max), randint(1, y_max)
        
    def __eq__(self, other):
        if not isinstance(other, Coordinates):
            return False
        return self.x == other.x and self.y == other.y
    
    def convert_to_indices(self) -> Union[int, int]:
        return self.x - 1, self.y - 1
    
    def val(self) -> str:
        return f"{self.x} {self.y}"
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def __sub__(self, other) -> int:
        if not isinstance(other, Coordinates):
            raise ValueError("Other operand coordinates too.")
        abs = lambda v: v if v >= 0 else -v
        return abs(self.x - other.x) + abs(self.y - other.y)


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
    
    def __str__(self) -> str:
        match self:
            case Direction.UP:
                return '\u2191'
            case Direction.RIGHT:
                return '\u2192'
            case Direction.LEFT:
                return '\u2190'
            case _:
                return '\u2193'