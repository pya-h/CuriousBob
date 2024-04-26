from field.gui import Field
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
        self.field.add_random_holes(number_of_holes)
        self.field.add_random_orbs(number_of_height)
        self.candidate = None
        # self.field.place_in_cell(self.agent) # TODO: Add agent to the cells list so that we dont need to pass agent as param everytime to show func
        # for now cause it can cause bugs in finding candidate, its passed as parameter

    def clear_scrren(self):
        '''Clear console. Command may change in different OSes'''
        os.system("@cls||clear")
        
    def wait(self, delay=1):
        '''Delay between agent moves, by calling sleep. delay unit is seconds. If delay value is set None, moves will update with hitting Enter.'''
        if not delay:
            input()
            return
        time.sleep(delay)
        
    def do_next_move(self) -> bool:
        if not self.field.get_remaining_orbs():
            return True
        if self.agent.moves >= self.MAX_MOVES:
            return False
        print("SA@", self.agent.position, " -> ", self.agent.direction)
        self.agent.look_around(self.field)
        has_reached = False
        if not self.candidate:
            self.candidate = self.agent.find_next_best_displacement(self.field)
            if self.candidate:
                '''set the agent the same position as orb to start holding ti'''
                self.agent.move_forward_to(self.candidate.orb)
            
        else:
            # if there is self.candidate from before
            has_reached = self.agent.direct_into(self.candidate)
        print("Current self.candidate: ", self.candidate)
        if not has_reached:
            self.agent.move(self.field, self.candidate) # move one step closer to near hole
            # entity: Entity = self.field.cells[self.agent.position.val()]
            # if entity:
            #     if self.candidate:
            #         if entity.type == EntityType.HOLE and isinstance(entity, Hole) and entity.has_room():
            #             self.candidate.hole = entity
            #             has_reached = self.candidate.hole.has_room() and not self.candidate.orb.hole
            #         elif entity.type == EntityType.ORB and isinstance(entity, Orb) and not entity.hole:
            #             self.candidate.orb = entity
            #             has_reached = self.candidate.hole.has_room() and not self.candidate.orb.hole
                        
            #         if has_reached:
            #             self.candidate.drop()
            #             self.candidate = None
        else:
            try:
                self.candidate.drop()
                self.field.shake()
                self.candidate = None
            except:
                pass
        return False
    
    def simulate(self):
        self.field.run(game)
        while True:
            self.clear_scrren()
            self.field.update_ui(self.agent)
            game_ended = self.do_next_move()
            if game_ended:
                return
            self.wait()
            
if __name__ == '__main__':
    game = Game()
    won = game.simulate()
    if won:
        print("All orbs are placed in holes.")
    else:
        print(f"Agent failed to complete its duty within {Game.MAX_MOVES} moves.")
        
    