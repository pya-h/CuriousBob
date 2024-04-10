from field import Field
from agent import Agent, Candidate, Direction
import os
import time
from entity import Entity, EntityType
from hole import Hole
from orb import Orb


class Game:
    MAX_MOVES = 30
    def __init__(self, fieldWidth: int = 5, fieldHegiht: int = 5, number_of_holes: int = 5, number_of_height: int = 5,) -> None:
        self.field = Field(fieldWidth, fieldHegiht)
        self.agent = Agent()
        # self.field.occupy_cell(self.agent)
        self.field.add_random_holes(number_of_holes)
        self.field.add_random_orbs(number_of_height)
        

    def simulate(self):
        candidate: Candidate = None
        while True:
            os.system("clear")
            self.field.show()
            if not self.field.get_remaining_orbs():
                return True
            if self.agent.moves >= self.MAX_MOVES:
                return False
            print("SA@", self.agent.position, " -> ", self.agent.direction)
            self.agent.look_around(self.field)
            has_reached = False
            if not candidate:
                candidate = self.agent.find_next_best_displacement(self.field)
                if candidate:
                    '''set the agent the same position as orb to start holding ti'''
                    self.agent.move_forward_to(candidate.orb)
                
            else:
                # if there is candidate from before
                has_reached = self.agent.direct_into(candidate)
            print("Current candidate: ", candidate)
            if not has_reached:
                self.agent.move(self.field, candidate) # move one step closer to near hole
                # entity: Entity = self.field.cells[self.agent.position.val()]
                # if entity:
                #     if candidate:
                #         if entity.type == EntityType.HOLE and isinstance(entity, Hole) and entity.has_room():
                #             candidate.hole = entity
                #             has_reached = candidate.hole.has_room() and not candidate.orb.hole
                #         elif entity.type == EntityType.ORB and isinstance(entity, Orb) and not entity.hole:
                #             candidate.orb = entity
                #             has_reached = candidate.hole.has_room() and not candidate.orb.hole
                            
                #         if has_reached:
                #             candidate.drop()
                #             candidate = None
            else:
                try:
                    candidate.drop()
                    self.field.shake()
                    candidate = None
                except:
                    pass
            time.sleep(1)
            
if __name__ == '__main__':
    game = Game()
    won = game.simulate()
    if won:
        print("All orbs are placed in holes.")
    else:
        print(f"Agent failed to complete its duty within {Game.MAX_MOVES} moves.")
        
    