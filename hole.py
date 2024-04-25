from coordinates import Coordinates
from entity import Entity, EntityType
from typing import List


class Hole(Entity):
    CAPACITY = 1  # how many orbs can be contained by a single hole
    DEFAULT_IMAGE = '...'
    def __init__(self, id: int, position: Coordinates | None = None, image: str|None = None) -> None:
        '''Holes; Holes are empty places inside field which can be filled with orbs. 
            Param Notes: Not specifying coordinates will make it randomise its position, not specifying image will make the app use default image.'''
        super().__init__(name="Hole", id=id, image=image or Hole.DEFAULT_IMAGE, entityType=EntityType.HOLE, position=position)
        
        self.orbs: List[Entity] = []  # Demonestrates the orbs that are fropped inside this hole. If the list is empty it means its ready to contain upcomming orbs
        
    def has_room(self) -> bool:
        return len(self.orbs) < self.CAPACITY