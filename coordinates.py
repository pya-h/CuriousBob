from random import randint


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
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"