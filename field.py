from typing import List
from orb import Orb
from hole import Hole
from coordinates import Coordinates
from typing import Dict
from entity import Entity, EntityType
import math
from random import randint
from agent import Direction

class Field:
    def __init__(self, width: int = 5, height: int = 5) -> None:
        if width < 2 or height < 2:
            raise ValueError("Field dimention cant be that small.")
        self.height: int = height
        self.width: int = width
        self.orbs: List[Orb] = []
        self.holes: List[Hole] = []
        self.cells: Dict[str, Entity|None] = {}
        self.extra: Dict[str, Entity|None] = {}
        
        self.init_cells()

    def init_cells(self):
        for i in range(1, self.width + 1):
            for j in range(1, self.height + 1):
                self.cells[Coordinates(i, j).val()] = None
                self.extra[Coordinates(i, j).val()] = None
                
      
    def update_cells(self):
        self.init_cells()
        for h in self.holes:
            self.cells[h.position.val()] = h
        for o in self.orbs:
            self.cells[o.position.val()] = o
            
    def place_in_cell(self, coords: Coordinates, entity: Entity|None):
        self.cells[coords.val()] = entity

    def occupy_cell(self, entity: Entity):
        if not entity:
            return
        self.cells[entity.position.val()] = entity
            
    def add_random_holes(self, number_of_holes: int):
        if number_of_holes <= 0:
            raise ValueError('Number of holes must be a positive number.')
        last_id = Hole.GetNextId(self.holes)
        for _ in range(1, number_of_holes + 1):
            hole = Hole(id=last_id)
            self.holes.append(hole)
            self.occupy_cell(hole)
            last_id += 1
            
    def add_hole(self, position: Coordinates):
        hole = Hole(id=Hole.GetNextId(self.holes), position=position)
        self.holes.append(hole)
        self.occupy_cell(hole)

    def add_random_orbs(self, number_of_orbs: int):
        if number_of_orbs <= 0:
            raise ValueError('Number of orbs must be a positive number.')
        last_id = Orb.GetNextId(self.orbs)
        for _ in range(1, number_of_orbs + 1):
            orb = Orb(id=last_id)
            self.orbs.append(orb)
            self.occupy_cell(orb)
            last_id += 1
            
    def add_orb(self, position: Coordinates):
        self.orbs.append(Orb(id=Orb.GetNextId(self.orbs), position=position))
      
    def get_remaining_orbs(self):
        out_orbs = list(filter(lambda o: not o.hole, self.orbs))
        return len(out_orbs)
        
    def show(self):
        print()
        cell_width, cell_height = 4, 3
        for h in range(self.height):
            for ch in range(cell_height):
                for w in range(self.width):
                    if not w:
                        print('|', end='')
                        if not ch:
                            for _ in range(self.width):
                                print(('- ' * cell_width) + '|', end='')
                            print()
                            print('|', end='')
                    coords = Coordinates(w + 1, h + 1)
                    entity = self.cells[coords.val()]
                    if not entity or math.floor(cell_height / 2) != ch:
                        print(('  ' * cell_width) + '|', end='')
                    else:
                        if entity.identified:
                            if (isinstance(entity, Hole) and entity.orbs):
                                x = entity.orbs[0]
                                en = f" {x.shortname}{entity.shortname}"
                            elif (isinstance(entity, Orb) and entity.hole):
                                x = entity.hole
                                en = f" {x.shortname}{entity.shortname}"
                            else:
                                en = f"   {entity.shortname}"
                        else:
                            en = ' '
                        print(f"{en:{cell_width*2}}" + '|', end='')
                            
                print()
        print('|', end='')
        for _ in range(self.width):
            print((' -' * cell_width) +  '|', end='')
        print()
        
    def shake(self):
        orbs = list(map(
            lambda coord: self.cells[coord] , filter(lambda key: self.cells[key] and isinstance(self.cells[key], Orb) and self.cells[key].hole is None, self.cells)
        ))
        for orb in orbs:
            rnd = randint(0, 100)
            if rnd < 10:
                # 10% of moving the orb
                rnd_direction = Direction.Random()
                match rnd_direction:
                    case Direction.RIGHT:
                        if orb.position.x < self.width:
                            orb.position.x += 1
                        else:
                            orb.position.x -= 1
                    case Direction.LEFT:
                        if orb.position.x > 1:
                            orb.position.x -= 1
                        else:
                            orb.position.x += 1
                    case Direction.UP:
                        if orb.position.y > 1:
                            orb.position.y -= 1
                        else:
                            orb.position.y += 1
                    case Direction.DOWN:
                        if orb.position.y < self.height:
                            orb.position.y += 1
                        else:
                            orb.position.y -= 1
                orb.identified = False