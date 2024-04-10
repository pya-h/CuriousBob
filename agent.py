from coordinates import Coordinates
from enum import Enum
from random import randint
from entity import Entity
from field import Field
from typing import Union
from hole import Hole
from orb import Orb


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
                return "Up"
            case Direction.RIGHT:
                return "Right"
            case Direction.LEFT:
                return "Left"
            case _:
                return "Down"


class Agent(Entity):
    DEFAULT_IMAGE = '...'
    def __init__(self, imagePath: str|None = None, position: Coordinates | None = None) -> None:
        super().__init__(id=0, name="Smart Agent", imagePath=imagePath or Agent.DEFAULT_IMAGE, position=position)
        self.direction: Direction = Direction.Random()
        self.moves = 0
        self.actions = 0
        
    def __str__(self) -> str:
        return f"{super().__str__()} with direction to {self.direction}"
    
        
    def extract_cooordinates(self) -> Union[int, int]:
        return self.position.x, self.position.y

    def look_around(self, field: Field):
        '''Look around in 8 directions and find som holes and orbs'''
        x, y = self.extract_cooordinates()
        steps = [-1, 0, 1]
        new_founds = 0
        for i in steps:
            for j in steps:
                if x + i >= 1 and y + j >= 1 and x + i <= field.width and y + j <= field.height:
                    cell = Coordinates(x + i, y + j)
                    entity = field.cells[cell.val()]
                    if entity and (isinstance(entity, Hole) or isinstance(entity, Orb)):
                        # identified
                        entity.identified = True
                        new_founds += 1
                        print(cell)
                        
        return new_founds