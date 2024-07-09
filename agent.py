import hugchat_interface
from movement import Coordinates, Direction
from entity import Entity, EntityType
from typing import Union, List, Dict
from hole import Hole
from orb import Orb
from resources.avatar import Avatar
from hugchat_interface import HugchatInterface
from decouple import config

primary_prompt = '''
    I need you to Help Spong Bob to do his game as best and fast as he could.
    Here is Bob. He is trying to look around a field, find some Orbs and put them in some Holes, and I need you to help me and Bob to do it the best way we can.
    This field has 5 x 5 cells. There are 3 Orbs and 3 Holes in the game, That are positioned randomly and even bob doesnt know where are them.
    Each hole can contain at most 1 Orb.
    Bob can only move one cell is 4 possible directions: Up, down, right, left. When bob reaches a Orb, he can hold the orb and move until he reaches a hole to put the orb into it.
    Bob doesn't know where the holes and orbs are, but at each position he can inspect his adjacent cells and discover wether there's an orb or hole or nothing in those adjacent cells.
    At each step i will provide you what Bob knows and i need you to tell what course of action bob should take. I will provide you the field and the place of objects that Bob is aware of.
    I show Holes with H, Orbs with O, And Bob with B. for simpliciy i dont provide you of filled holes or Orbs inside a hole positions,. Also for empty cells with no hole or orb or etc i will put -
    Also Each Hole and Orb will have a Integer number between 1 to 3, showing the index of that object, so all objects in the game are: O1, O2, O3, H1, H2, H3, B. So for example if i Sned this line to you: 'O2 (1, 2)' it means that Orb Number 2 is on second row and first column of the field.
    So I provide Object details per line, meaning that each line of my input contains the position of a Hole, Orb or Bob.
    I expect you that at each step return me a short string as answer. Please try to provide me answers the best way you can, so that bob can complete his game as fast as he can, because he is limited to 30 moves.
    If he fill all the holes with available orbs in less than 30 moves he wins the game.
    if by the knowledge provided for you, you can specify that Bob should take which Orb and deliver it to which Hole, You should return a string like This example: 'O1 H2' meaning that Bob must take Orb number 1 and deliver it to Hole Number 2.
    There may be situations that bob has not discovered enough data to link an orb to a hole, in those situations bob go to next cell, so that he may collect new information, this can be done by a random move or a smart one(that depends on you and the information).
    In that case just provide a direction as an integer value: 0 for Down, 1 for Up, 2 for Left and 3 for Right.
    Bob will gain knowledge on each step and I will provide you that knowledge, Then you should provide me the answer  as string only and only in the format i described, then i move bob as you said, and bob will go to next step.
    Please note that do not add anything extra to the result string. I need to use your answer in my code and i need it to be in the format i told you so that my code identifies you answer, so keep in mind you have two type of answers:
    1. If you want to say For example Bob must pick up Orb 3 and put in Hole 2, just return this as string: 'O3 H2'
    2. If therer is only holes available or only orbs available (available means identified by Bob) or None, then you should try to navigate Bob to new places so he can gather new information. you do that by providing current direction. For this you should Only and Only return an integer as:
        0 for DOWN, 1 for Up, 2 for Left and 3 for right. Remember in this case, you should provide only an integer, nothing else not even an extra character. Try to use directions that will lead bob to new cells and new data and also prevent loop moves or stucking bob in corner of field.
    Hope me and you can helpo bob win this game.
    
'''

hugchat_email = config('email')
hugchat_password = config('password')

class Candidate:
    def __init__(self, orb: Orb, hole: Hole) -> None:
        self.orb = orb
        self.hole = hole

    @property
    def distance(self):
        return self.orb - self.hole

    def drop(self, dropper_id: int):
        if not self.hole.has_room():
            raise Exception('Hole is full')
        self.orb.hole = self.hole
        self.hole.orbs.append(self.orb)
        self.orb.drop_by = dropper_id

    def __str__(self) -> str:
        return f"Candidate: Orb@{self.orb.position} -> Hole@{self.hole.position if self.hole else 'Nowhere'}"

    def fulfilled(self):
        return self.orb and self.hole and self.orb.position == self.hole.position

class Agent(Entity):
    NumberOfAgents = 0
    NO_MOVE_REP_MAX = 4

    @staticmethod
    def DefaultAvatar(id: int) -> Dict[Direction, Avatar]:
        return {
            Direction.UP: Avatar(f'resources/agent{id}/up.png', 60),
            Direction.DOWN: Avatar(f'resources/agent{id}/down.png', 60),
            Direction.RIGHT: Avatar(f'resources/agent{id}/right.png', 60),
            Direction.LEFT: Avatar(f'resources/agent{id}/left.png', 60),
        }

    def __init__(self, position: Coordinates | None = None, avatars: Dict[Direction, Avatar] = None, name: str | None = None) -> None:
        Agent.NumberOfAgents += 1
        super().__init__(id=Agent.NumberOfAgents, name="Smart Agent", avatar=avatars, entityType=EntityType.AGENT, position=position)
        self.direction: Direction | None = Direction.Random()
        self.moves = 0
        self.actions = 0
        self.__avatars = avatars if avatars else Agent.DefaultAvatar(self.id)
        self.reach_to_candidate: Candidate | None = None
        self.candidate: Candidate | None = None
        self.no_point_moving_orb = None  # for when there's no candidate, this could be useful by moving orb, so it isnt required to move back to it just for moving it again.
        self.one_directional_moves = 0
        self.discoveries: List[Orb|Hole] = []
        self.no_move_rep = 0
        self.hang_on = 0
        self.name: str | None = name if not None else f'Agent {self.id}'
        self.throws_count = 0
        self.hugchat = HugchatInterface(hugchat_email, hugchat_password)

    @property
    def avatar(self):
        '''return the avatar of the agent base of the direction'''
        return self.__avatars[self.direction]

    def activate_hugchat(self):
        result = self.hugchat.activate(primary_prompt)
        print(result)
        return result
    
    def __str__(self) -> str:
        return f"A{self.id}{self.direction}" if self.direction != Direction.LEFT else f"{self.direction}A{self.id}"

    def extract_cooordinates(self) -> Union[int, int]:
        return self.position.x, self.position.y

    def look_around(self, field):
        '''Look around in 8 directions and find som holes and orbs'''
        x, y = self.extract_cooordinates()
        steps = [-1, 0, 1]
        new_founds = 0
        for i in steps:
            for j in steps:
                if x + i >= 1 and y + j >= 1 and x + i <= field.width and y + j <= field.height:
                    cell = Coordinates(x + i, y + j)
                    entities = field.get_cell(cell)
                    for entity in entities:
                        if entity is not None and entity not in self.discoveries:
                            if (isinstance(entity, Hole) and entity.has_room()) or (isinstance(entity, Orb) and not entity.hole):
                                # identified
                                self.discoveries.append(entity)
                                new_founds += 1

        return new_founds

    def find_next_best_displacement(self):
        orbs: List[Orb] = list(filter(lambda item: isinstance(item, Orb) and item.is_available, self.discoveries))
        holes: List[Hole] = list(filter(lambda item: isinstance(item, Hole) and item.is_available, self.discoveries))

        if not holes or not orbs:
            return None

        candidate: Candidate = Candidate(orbs[0], holes[0])
        for orb in orbs:
            for hole in holes:
                if (hole.has_room()) and (not orb.hole) and (candidate.distance > orb - hole or candidate.hole is None):
                    candidate = Candidate(orb, hole)
                    orb.targeted = hole.targeted = self.id
        return candidate

    def check_for_less_distant_hole(self):
        if not self.candidate:
            return
        holes: List[Hole] = list(filter(lambda item: isinstance(item, Hole) and item != self.candidate.hole and item.is_available, self.discoveries))

        if not holes:
            return

        for hole in holes:
            if (hole.has_room()) and (self.candidate.distance > self.candidate.orb - hole):
                self.candidate.hole.targeted = None
                self.candidate.hole = hole
                hole.targeted = self.id

    def direct_into(self, target: Candidate):
        if not target or not target.orb or not target.hole:
            return
        # self.check_for_less_distant_hole()

        if target.hole:
            if target.orb.position.x < target.hole.position.x:
                self.direction = Direction.RIGHT
            elif target.orb.position.x > target.hole.position.x:
                self.direction = Direction.LEFT
            elif target.orb.position.y < target.hole.position.y:
                self.direction = Direction.DOWN
            elif target.orb.position.y > target.hole.position.y:
                self.direction = Direction.UP
            else:
                return True

        return False

    def check_one_directional_moves(self, previous_direction: Direction, x_max: int, y_max: int) -> bool:
        '''This is for getting the agen out of one directional move loop; if its taking so long moving in one didrection, this method chanes it for the better'''
        if not self.candidate and previous_direction == self.direction:
            self.one_directional_moves += 1
            # this means random movement has been taking to long in the same direciotn
            if self.direction.is_horizontal() and self.one_directional_moves >= int(x_max / 2):
                if self.position.y <= 0.3 * y_max:
                    self.direction = Direction.DOWN
                elif self.position.y >= 0.8 * y_max:
                    self.direction = Direction.UP
                elif self.one_directional_moves >= 2 + int(x_max / 2):
                    # if the agent is in the middle of the field, it needs a larger threshold
                    self.direction = Direction.Random(axis='v')
            elif self.direction.is_vertical() and self.one_directional_moves >= int(y_max / 2):
                if self.position.x <= 0.3 * x_max:
                    self.direction = Direction.RIGHT
                elif self.position.x >= 0.8 * x_max:
                    self.direction = Direction.LEFT
                elif self.one_directional_moves >= 2 + int(y_max / 2):
                    # if the agent is in the middle of the field, it needs a larger threshold
                    self.direction = Direction.Random(axis='h')
            return True

        self.one_directional_moves = 0
        return False

    def move(self, field, candidate: Candidate|None, agents: List[Entity]) -> None|int:
        prev_pos = Coordinates(self.position.x, self.position.y)
        prev_dir = self.direction
        # self.check_one_directional_moves(prev_dir, field.width, field.height)
        self.check_agent_position(field)
        match self.direction:
            case Direction.RIGHT:
                self.position.x += 1
            case Direction.LEFT:
                self.position.x -= 1
            case Direction.UP:
                self.position.y -= 1
            case Direction.DOWN:
                self.position.y += 1
        if candidate:
            candidate.orb.position.x = self.position.x
            candidate.orb.position.y = self.position.y
            field.update_cells()

        other = (agents[0] if agents[0] != self else agents[-1]) if len(agents) > 1 else None

        if other is not None and other.position == self.position:
            self.return_to_position(prev_pos)
            return -1
        self.moves += 1
        return None

    def move_forward_to(self, target: Entity):

        if self.position.x < target.position.x:
            self.direction = Direction.RIGHT
            self.position.x += 1
            self.moves += 1
            return int(self.position == target.position)

        if self.position.x > target.position.x:
            self.direction = Direction.LEFT
            self.position.x -= 1
            self.moves += 1
            return int(self.position == target.position)

        if self.position.y < target.position.y:
            self.direction = Direction.DOWN
            self.position.y += 1
            self.moves += 1
            return int(self.position == target.position)

        if self.position.y > target.position.y:
            self.direction = Direction.UP
            self.position.y -= 1
            self.moves += 1
            return int(self.position == target.position)
        print(self.position, target)
        return 1

    def return_to_position(self, position: Coordinates):
        self.position = Coordinates(position.x, position.y)
        if self.candidate:
            self.candidate.orb.position = Coordinates(position.x, position.y)  # preventing position of reference copy

    def check_agent_position(self, field):
        '''Prevent egant from going out of the field'''
        while not self.direction \
            or (self.direction == Direction.RIGHT and self.position.x == field.width) \
            or (self.direction == Direction.LEFT and self.position.x == 1) \
            or (self.direction == Direction.UP and self.position.y == 1) \
            or (self.direction == Direction.DOWN and self.position.y == field.height):
                self.direction = Direction.Random()

    def force_move(self, field: any, all_agents: List[Entity]):
        '''This is for when both agents are stock next to each other and cant move'''
        self.direction = Direction.Random()
        while self.move(field, self.candidate, all_agents) == -1:
            self.direction = Direction.Random()

    def forget(self, entity: Orb|Hole, just_entity_itself: bool = False):
        if entity in self.discoveries:
            self.discoveries.remove(entity)
            if just_entity_itself:
                return
            if isinstance(entity, Orb):
                if entity.hole is not None and not entity.hole.has_room():
                    self.forget(entity.hole)
            elif isinstance(entity, Hole) and entity.orbs:
                for orb in entity.orbs:
                    if orb in self.discoveries:
                        self.discoveries.remove(orb)

    def try_to_sabotage(self, field) -> Orb | None:
        cell: List[Entity] = field.get_cell(self.position)
        try:  # skip this function if the cell is not array of entities
            if not len(cell):
                return
        except:
            return

        for entity in cell:
            if isinstance(entity, Orb) and entity.hole is not None and entity.drop_by != self.id:
                # throw the orb to nowhere
                field.throw_orb(cell, entity, self)
                self.throws_count += 1
                return entity
        return None

    def hugchat_data(self):
        orbs: List[Orb] = list(filter(lambda item: isinstance(item, Orb) and item.is_available, self.discoveries))
        holes: List[Hole] = list(filter(lambda item: isinstance(item, Hole) and item.is_available, self.discoveries))
        input_str: str = ''
        for orb in orbs:
            input_str += f'O{orb.id} {orb.position.__str__()}\n'

        for hole in holes:
            input_str += f'H{hole.id} {hole.position.__str__()}\n'

        input_str += f'B {self.position.__str__()}'
        return input_str
    
    def ask_hugchat(self, prompt: str):
        r = self.hugchat.prompt(prompt)
        print('Answer: ', r)
        return r