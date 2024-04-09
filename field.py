from typing import List
from orb import Orb
from hole import Hole
from coordinates import Coordinates

class Field:
    
    def __init__(self, width: int = 5, height: int = 5) -> None:
        self.height: int = height
        self.width: int = width
        self.orbs: List[Orb] = []
        self.holes: List[Hole] = []
        
    def add_random_holes(self, number_of_holes: int):
        if number_of_holes <= 0:
            raise ValueError('Number of holes must be a positive number.')
        last_id = Hole.GetNextId(self.holes)
        for _ in range(1, number_of_holes + 1):
            self.holes.append(Hole(id=last_id))
            last_id += 1
            
    def add_hole(self, position: Coordinates):
        self.holes.append(Hole(id=Hole.GetNextId(self.holes), position=position))
        
    def add_random_orbs(self, number_of_orbs: int):
        if number_of_orbs <= 0:
            raise ValueError('Number of orbs must be a positive number.')
        last_id = Orb.GetNextId(self.orbs)
        for _ in range(1, number_of_orbs + 1):
            self.orbs.append(Orb(id=last_id))
            last_id += 1
            
    def add_orb(self, position: Coordinates):
        self.orbs.append(Orb(id=Orb.GetNextId(self.orbs), position=position))