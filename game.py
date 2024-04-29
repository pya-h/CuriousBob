from field.gui import Field
from agent import Agent
import os
import time
from field.logic import FieldType
from typing import List
from hole import Hole
from movement import Direction


class Game:
    MAX_MOVES = 30

    def __init__(self, fieldWidth: int = 7, fieldHegiht: int = 7, number_of_holes: int = 5, number_of_height: int = 5,) -> None:
        self.field = Field(fieldWidth, fieldHegiht)
        self.agents: List[Agent] = [Agent(), Agent()]
        self.field.add_random_holes(number_of_holes)
        self.field.add_random_orbs(number_of_height)
        self.no_move_rep = 0
        
    def clear_scrren(self):
        '''Clear console. Command may change in different OSes'''
        os.system("clear")
        
    def wait(self, delay=1):
        '''Delay between agent moves, by calling sleep. delay unit is seconds. If delay value is set None, moves will update with hitting Enter.'''
        if not delay:
            input()
            return
        time.sleep(delay)
        
    def agents_has_won(self):
        return not self.field.get_remaining_orbs()
    
    def do_next_move(self) -> bool:
        if not self.field.get_remaining_orbs():
            return True
        for _, agent in enumerate(self.agents):

            if agent.moves >= self.MAX_MOVES:
                continue
            print("A@", agent.position, " -> ", agent.direction)

            agent.look_around(self.field)
            candidate_transfer_fulfilled = False
            if not agent.candidate:
                if not agent.reach_to_candidate:
                    agent.reach_to_candidate = agent.find_next_best_displacement(self.field)
                if agent.reach_to_candidate:
                    '''set the agent the same position as orb to start holding ti'''
                    reached = agent.move_forward_to(agent.reach_to_candidate.orb, self.agents)
                    if reached == 1:
                        agent.candidate = agent.reach_to_candidate
                        agent.reach_to_candidate = None
                        self.no_move_rep = 0
                    elif reached == -1:
                        self.no_move_rep += 1
                    else:
                        self.no_move_rep = 0
                    if self.no_move_rep >= 3:
                        agent.force_move(self.field, self.agents)
                        self.no_move_rep = 0
                    continue
            else:
                # if there is agent.candidate from before
                candidate_transfer_fulfilled = agent.direct_into(agent.candidate)
            print("Current agent.candidate: ", agent.candidate)
            if not candidate_transfer_fulfilled:
                r = agent.move(self.field, agent.candidate, self.agents) # move one step closer to near hole
                if r == -1:
                    self.no_move_rep += 1
                else:
                    self.no_move_rep = 0
                    
                if self.no_move_rep >= 3:
                    agent.force_move(self.field, self.agents)
                    self.no_move_rep = 0
                # if not agent.candidate:
                #     most = int(0.8 * self.field.width)
                #     mid = int(0.5 * self.field.width)
                #     if agent.direction == Direction.RIGHT and self.field.width - agent.position.x >= most:
                #         if agent.position.y <= mid:
                #             agent.direction = Direction.DOWN
                #         else:
                #             agent.direction = Direction.UP
                            
                #     if agent.direction == Direction.DOWN and self.field.height - agent.position.y >= most:
                #         if agent.position.x <= mid:
                #             agent.direction = Direction.RIGHT
                #         else:
                #             agent.direction = Direction.LEFT
                #     continue
            do_drop = False
            if agent.candidate and agent.candidate.fulfilled():
                do_drop = True
            elif agent.candidate:
                x, y = agent.position.convert_to_indices()
                cell = self.field.cells[y][x]
                if cell:
                    if len(cell) == 1 and isinstance(cell[0], Hole) and not cell[0].orbs:
                        do_drop = True
                        agent.candidate.hole = cell[0]
            if candidate_transfer_fulfilled or do_drop:
                try:
                    agent.candidate.drop()
                    self.field.shake()
                    agent.candidate = None
                except Exception as ex:
                    print("ERROR", ex)
                    agent.candidate = None
        return self.agents[0].moves >= self.MAX_MOVES and self.agents[1].moves >= self.MAX_MOVES
    
    def simulate(self):
        self.field.run(game)
        if self.field.type != FieldType.GUI:
            while True:
                self.clear_scrren()
                self.field.update_ui(self.agents)
                game_ended = self.do_next_move()
                if game_ended:
                    return
                self.wait()
                
if __name__ == '__main__':
    game = Game()
    game.simulate()
    if game.agents_has_won():
        print("All orbs are placed in holes.")
    else:
        print(f"Agent failed to complete its duty within {Game.MAX_MOVES} moves.")
        
    