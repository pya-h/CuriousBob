from typing import List
from orb import Orb
from hole import Hole

class Field:
    
    def __init__(self, width: int = 5, height: int = 5) -> None:
        self.height: int = height
        self.width: int = width
        self.orbs: List[Orb] = []
        self.holes: List[Hole] = []
        
    