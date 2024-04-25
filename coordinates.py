from random import randint
from typing import Union

class Coordinates:
    
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x: int = x 
        self.y: int = y
        
    @staticmethod
    def Random(x_max = 5, y_max = 5):
        return Coordinates(randint(1, x_max), randint(1, y_max))
    
    def Randomize(self, x_max = 5, y_max = 5):
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
