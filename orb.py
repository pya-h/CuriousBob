from coordinates import Coordinates
from entity import Entity
from hole import Hole


class Orb(Entity):
    
    def __init__(self, id: int, position: Coordinates | None = None, imagePath: str|None = None) -> None:
        '''Orbs: orbs are sphere entities which would fill the holes inside the field.
            Params note: Not specifying coordinates will make it randomise its position, not specifying imagePath will make the app use default image.'''
        super().__init__(name="Orb", id=id, imagePath=imagePath, position=position)
        
        self.hole: Hole|None = None  # The hole which this orb is dropped to. If orb.hole is None it means this orb is still outside in the field