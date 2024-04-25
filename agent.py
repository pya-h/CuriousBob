from coordinates import Coordinates
from enum import Enum
from random import randint
from entity import Entity, EntityType
from typing import Union, List
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
                return '\u2191'
            case Direction.RIGHT:
                return '\u2192'
            case Direction.LEFT:
                return '\u2190'
            case _:
                return '\u2193'


class Candidate:
    def __init__(self, orb: Orb, hole: Hole) -> None:
        self.orb = orb
        self.hole = hole
        
    @property
    def distance(self):
        return self.orb - self.hole
    
    def drop(self):
        if not self.hole.has_room():
            raise ValueError("Hole cant be full for drop")
        self.orb.hole = self.hole
        self.hole.orbs.append(self.orb)

    def __str__(self) -> str:
        return f"Candidate: Orb@{self.orb.position} -> Hole@{self.hole.position}"    

   
class Agent(Entity):
    DEFAULT_IMAGE = '...'
    def __init__(self, image: str|None = None, position: Coordinates | None = None) -> None:
        super().__init__(id=0, name="Smart Agent", image=image or Agent.DEFAULT_IMAGE, entityType=EntityType.AGENT, position=position)
        self.direction: Direction = Direction.Random()
        self.moves = 0
        self.actions = 0
        
    def __str__(self) -> str:
        return f"A{self.direction}" if self.direction != Direction.LEFT else f"{self.direction}A"
        
    def extract_cooordinates(self) -> Union[int, int]:
        return self.position.x, self.position.y

    def look_around(self, field):
        '''Look around in 8 directions and find som holes and orbs'''
        x, y = self.extract_cooordinates()
        steps = [-1, 0, 1]
        new_founds = 0
        print("Proximity Identied:")
        for i in steps:
            for j in steps:
                if x + i >= 1 and y + j >= 1 and x + i <= field.width and y + j <= field.height:
                    cell = Coordinates(x + i, y + j)
                    entities = field.get_cell(cell)
                    for entity in entities:
                        if entity and (isinstance(entity, Hole) or isinstance(entity, Orb)):
                            # identified
                            entity.identified = True
                            new_founds += 1
                            print(cell, entity.name)
                        
        return new_founds
    
    def find_next_best_displacement(self, field):
        idents = []

        for row in field.cells:
            for cell in row:
                if cell:
                    for item in cell:
                        if item.identified:
                            idents.append(item)
                    
        orbs: List[Orb] = list(filter(lambda entity: isinstance(entity, Orb) and (entity.hole is None), idents))
        holes: List[Hole] = list(filter(lambda entity: isinstance(entity, Hole) and entity.has_room(), idents))

        if not holes or not orbs:
            return None
        candidate: Candidate = Candidate(orbs[0], holes[0])
        for orb in orbs:
            for hole in holes:
                if (hole.has_room()) and (not orb.hole) and (candidate.distance > orb - hole):
                    candidate = Candidate(orb, hole)
         
        return candidate
    
    def direct_into(self, target: Candidate):
        if not target or not target.orb or not target.hole:
            return
        if target.orb.position.x < target.hole.position.x:
            self.direction = Direction.RIGHT
        elif target.orb.position.x > target.hole.position.x:
            self.direction = Direction.LEFT
        elif target.orb.position.y < target.hole.position.y:
            self.direction = Direction.DOWN
        elif target.orb.position.y > target.hole.position.y:
            self.direction = Direction.UP
        else:
            return True

        return False
         
    def move(self, field, candidate: Candidate|None):
        self.check_agent_position(field)
        match self.direction:
            case Direction.RIGHT:
                self.position.x += 1
            case Direction.LEFT:
                self.position.x -= 1
            case Direction.UP:
                self.position.y -= 1
            case Direction.DOWN:
                self.position.y += 1
        if candidate:
            candidate.orb.position.x = self.position.x
            candidate.orb.position.y = self.position.y
            field.update_cells(self)
        self.moves += 1
        field.shake()
        
    def move_forward_to(self, target: Entity):
        if self.position.x < target.position.x:
            self.position.x += 1
            self.moves += 1
        elif self.position.x > target.position.x:
            self.position.x -= 1
            self.moves += 1
            
        if self.position.y < target.position.y:
            self.position.y += 1
            self.moves += 1
        elif self.position.y > target.position.y:
            self.position.y -= 1
            self.moves += 1
            
    def check_agent_position(self, field):
        '''Prevent egant from going out of the field'''
        while not self.direction \
            or (self.direction == Direction.RIGHT and self.position.x == field.width) \
            or (self.direction == Direction.LEFT and self.position.x == 1) \
            or (self.direction == Direction.UP and self.position.y == 1) \
            or (self.direction == Direction.DOWN and self.position.y == field.height):
                self.direction = Direction.Random()