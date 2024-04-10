from field import Field
from agent import Agent

class Game:
    MAX_MOVES = 30
    def __init__(self, fieldWidth: int = 5, fieldHegiht: int = 5, number_of_holes: int = 5, number_of_height: int = 5,) -> None:
        self.field = Field(fieldWidth, fieldHegiht)
        self.agent = Agent()
        self.field.occupy_cell(self.agent)
        self.field.add_random_holes(number_of_holes)
        self.field.add_random_orbs(number_of_height)
        

    def simulate(self):
        self.field.show()
        self.agent.look_around(self.field)

if __name__ == '__main__':
    game = Game()
    game.simulate()