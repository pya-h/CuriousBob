from field.gui import Field
from agent import Agent, Candidate
import os
import time
from field.logic import FieldType
from typing import List
from hole import Hole
from movement import Direction


class Game:
    MAX_MOVES = 30

    def __init__(self, fieldWidth: int = 5, fieldHegiht: int = 5, number_of_holes: int = 3, number_of_height: int = 3,) -> None:
        self.field = Field(fieldWidth, fieldHegiht)
        self.agents: List[Agent] = [Agent(name='Bob')]#, Agent(name='Patrick')]
        self.field.add_random_holes(number_of_holes)
        self.field.add_random_orbs(number_of_height)

    def clear_scrren(self):
        '''Clear console. Command may change in different OSes'''
        os.system("clear")

    def wait(self, delay=5):
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
        agent = self.agents[0]
    
        print(f"A{agent.id}", " -> ", agent.direction)

        agent.look_around(self.field)
        try:
            if agent.reach_to_candidate:
                reached = agent.move_forward_to(agent.reach_to_candidate.orb)
                if reached:
                    agent.candidate = agent.reach_to_candidate
                    agent.reach_to_candidate = None
                    reached = False
            elif agent.candidate:
                reached = agent.direct_into(agent.candidate)
                if not reached:
                    agent.move(self.field, agent.candidate, self.agents)
                agent.moves += 1
                if agent.moves >= self.MAX_MOVES:
                    return True
                if reached or agent.candidate.fulfilled():
                    agent.candidate.drop(agent.id)
                    agent.forget(agent.candidate.orb)  # this will make agent forget the orb and hole both
                    self.field.shake(self.agents)
                    agent.candidate = None
                    agent.reach_to_candidate = None
            else:
                prompt = agent.hugchat_data()
                print(prompt)
                print('### Bob is thinking ... ###')
                hugchat_decision = str(agent.ask_hugchat("Here is the current Position of objects that Bob knows:\n" + prompt))
                objects = hugchat_decision.split()
                if len(objects) == 2:
                    orb_id = int(objects[0][1:])
                    orb = self.field.get_orb_by_id(orb_id)
                    hole_id = int(objects[1][1:])
                    hole = self.field.get_hole_by_id(hole_id)
                    print(orb, hole)
                    agent.reach_to_candidate = Candidate(orb, hole)
                    
                else:
                    if agent.candidate:
                        agent.candidate.hole = None
                    agent.candidate = None
                    agent.direction = Direction.From(int(hugchat_decision))
                    agent.move(self.field, None, self.agents)
        except Exception as ex:
            print(ex)
            if agent.candidate:
                agent.candidate.hole = None
            agent.candidate = None

        self.field.set_final_stats(self.agents)

        return agent.moves >= Game.MAX_MOVES
        
    def simulate(self):
        r = self.agents[0].activate_hugchat()

        self.field.run(game)
        if self.field.type != FieldType.GUI:
            while True:
                self.clear_scrren()
                self.field.update_ui(self.agents)
                game_ended = self.do_next_move()
                if game_ended:
                    print(self.field.final_stats)
                    return
                self.wait()

if __name__ == '__main__':
    game = Game()
    game.simulate()
    if game.agents_has_won():
        print("All orbs are placed in holes.")
    else:
        print(f"Agent failed to complete its duty within {Game.MAX_MOVES} moves.")


