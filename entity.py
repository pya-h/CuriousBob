from coordinates import Coordinates
from typing import List


class Entity:
    ALL_ENTITIES = []
    
    def __init__(self, id: int, name: str, imagePath: str, position: Coordinates|None = None) -> None:
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
        self.alias: str = f"{self.name} #${self.id}"

        self.imagePath: str = imagePath  # TODO: Check if image exists
        Entity.ALL_ENTITIES.append(self)
        
    
    def overlaps_on_others(self):
        '''Find out if this entity falls upon the exact same position as a previously defined entity'''
        for I in Entity.ALL_ENTITIES:
           if I != self and I.position == self.position:
               return True

        return False