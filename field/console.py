from field.logic import FieldLogic
from movement import Coordinates
import math
from hole import Hole
from orb import Orb
from agent import Agent


class Field(FieldLogic):
    '''Field illustration in a console app.'''  
    def run(self):
        print("Welcome! Press enter to start...")
        input()
        return self
    
    def update_ui(self, agent: Agent):
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
                    entities = self.get_cell(coords)
                    entity = entities[0] if entities else None 
                    if not entity or math.floor(cell_height / 2) != ch:
                        print(('  ' * cell_width) + '|', end='')
                    else:
                        en = agent.__str__() if agent.position == coords else ''
                        if entity.identified or True: # FIXME: remove or true
                            if (isinstance(entity, Hole) and entity.orbs):
                                x = entity.orbs[0]
                                en += f" {x.shortname}{entity.shortname}"
                            elif (isinstance(entity, Orb) and entity.hole):
                                x = entity.hole
                                en += f" {x.shortname}{entity.shortname}"
                            else:
                                en += f"   {entity.shortname}"
                        else:
                            en += ' '
                        print(f"{en:{cell_width*2}}" + '|', end='')
                            
                print()
        print('|', end='')
        for _ in range(self.width):
            print((' -' * cell_width) +  '|', end='')
        print()