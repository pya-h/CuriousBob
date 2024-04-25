from coordinates import Coordinates
from enum import Enum
from typing import List

class EntityType(Enum):
    NONE = 0
    ORB = 1
    HOLE = 2
    AGENT = 3

class Entity:
    ALL_ENTITIES = []
    
    def __init__(self, id: int, name: str, image: str, entityType: EntityType = EntityType.NONE, position: Coordinates|None = None) -> None:
        if position:
            self.position = position
        else:
            # if position is not specified, randomise it
            self.position = Coordinates.Random()
            while self.overlaps_on_others():
                self.position.Randomize()
        if id < 0:
            raise ValueError("Invalid id provided.")
        self.id: int = id
        self.name = name
        self.alias: str = f"{self.name} #{self.id}"
        self.shortname: str = f"{''.join([word[0] for word in self.name.split()])}{self.id if self.id else ''}"
        self.image: str = image  # TODO: Check if image existss
        self.identified: bool = False
        self.type = entityType
        Entity.ALL_ENTITIES.append(self)
        
    
    def overlaps_on_others(self):
        '''Find out if this entity falls upon the exact same position as a previously defined entity'''
        for I in Entity.ALL_ENTITIES:
           if I != self and I.position == self.position:
               return True

        return False
    
    @staticmethod
    def GetNextId(entity_list: List[any]) -> int|None:
        '''Get next available id for each type of entity.'''
        try:
            return max(entity_list, key=lambda e: e.id).id + 1 if entity_list else 1
        except:
            pass
        return None
    
    def __str__(self) -> str:
        return f"{self.alias} is at {self.position}"

    def __sub__(self, other):
        if not isinstance(other, Entity):
            raise ValueError("Other operand must an Entity.")
        return self.position - other.position