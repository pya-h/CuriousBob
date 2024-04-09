from coordinates import Coordinates
from entity import Entity
from typing import List
from orb import Orb


class Hole(Entity):
    MAX_CAPACITY = 1  # how many orbs can be contained by a single hole
    def __init__(self, id: int, position: Coordinates | None = None, imagePath: str|None = None) -> None:
        '''Holes; Holes are empty places inside field which can be filled with orbs. 
            Param Notes: Not specifying coordinates will make it randomise its position, not specifying imagePath will make the app use default image.'''
        super().__init__(name="Hole", id=id, imagePath=imagePath, position=position)
        
        self.orbs: List[Orb] = []  # Demonestrates the orbs that are fropped inside this hole. If the list is empty it means its ready to contain upcomming orbs