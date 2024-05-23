from movement import Coordinates, Direction
from enum import Enum
from random import randint
from entity import Entity, EntityType
from typing import Union, List, Dict
from hole import Hole
from orb import Orb
from resources.avatar import Avatar



class Candidate:
    def __init__(self, orb: Orb, hole: Hole) -> None:
        self.orb = orb
        self.hole = hole

    @property
    def distance(self):
        return self.orb - self.hole

    def drop(self):
        if not self.hole.has_room():
            raise ValueError("Hole cant be full for drop")
        self.orb.hole = self.hole
        self.hole.orbs.append(self.orb)

    def __str__(self) -> str:
        return f"Candidate: Orb@{self.orb.position} -> Hole@{self.hole.position}"

    def fulfilled(self):
        return self.orb and self.hole and self.orb.position == self.hole.position

class Agent(Entity):
    NumberOfAgents = 0
    @staticmethod
    def DefaultAvatar(id: int) -> Dict[Direction, Avatar]:
        return {
            Direction.UP: Avatar(f'resources/agent{id}/up.png', 60),
            Direction.DOWN: Avatar(f'resources/agent{id}/down.png', 60),
            Direction.RIGHT: Avatar(f'resources/agent{id}/right.png', 60),
            Direction.LEFT: Avatar(f'resources/agent{id}/left.png', 60),
        }

    def __init__(self, position: Coordinates | None = None, avatars: Dict[Direction, Avatar] = None) -> None:
        Agent.NumberOfAgents += 1
        super().__init__(id=Agent.NumberOfAgents, name="Smart Agent", avatar=avatars, entityType=EntityType.AGENT, position=position)
        self.direction: Direction = Direction.Random()
        self.moves = 0
        self.actions = 0
        self.__avatars = avatars if avatars else Agent.DefaultAvatar(self.id)
        self.reach_to_candidate: Candidate = None
        self.candidate: Candidate = None
        self.no_point_moving_orb = None  # for when there's no candidate, this could be useful by moving orb, so it isnt required to move back to it just for moving it again.
        self.one_directional_moves = 0

    @property
    def avatar(self):
        '''return the avatar of the agent base of the direction'''
        return self.__avatars[self.direction]

    def __str__(self) -> str:
        return f"A{self.id}{self.direction}" if self.direction != Direction.LEFT else f"{self.direction}A{self.id}"

    def extract_cooordinates(self) -> Union[int, int]:
        return self.position.x, self.position.y

    def look_around(self, field):
        '''Look around in 8 directions and find som holes and orbs'''
        x, y = self.extract_cooordinates()
        steps = [-1, 0, 1]
        new_founds = 0
        print("Proximity Identied:")
        for i in steps:
            for j in steps:
                if x + i >= 1 and y + j >= 1 and x + i <= field.width and y + j <= field.height:
                    cell = Coordinates(x + i, y + j)
                    entities = field.get_cell(cell)
                    for entity in entities:
                        if entity and (isinstance(entity, Hole) or isinstance(entity, Orb)):
                            # identified
                            entity.identified = self.id
                            new_founds += 1
                            print(cell, entity.name)

        return new_founds

    def find_next_best_displacement(self, field):
        orbs: List[Orb] = []
        holes: List[Hole] = []

        for row in field.cells:
            for cell in row:
                if cell:
                    for item in cell:
                        if item.identified == self.id:
                            if isinstance(item, Orb) and not item.hole and not item.targeted:
                                orbs.append(item)
                            elif isinstance(item, Hole) and not item.orbs and not item.targeted:
                                holes.append(item)

        if not holes or not orbs:
            return None
        candidate: Candidate = Candidate(orbs[0], holes[0])
        for orb in orbs:
            for hole in holes:
                if (hole.has_room()) and (not orb.hole) and (candidate.distance > orb - hole):
                    candidate = Candidate(orb, hole)
                    orb.targeted = hole.targeted = self.id
        return candidate

    def direct_into(self, target: Candidate):
        if not target or not target.orb or not target.hole:
            return
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
        self.check_one_directional_moves(prev_dir, field.width, field.height)
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
            field.update_cells(self)

        other = agents[0] if agents[0] != self else agents[-1]

        if other.position == self.position:
            self.position = prev_pos
            return -1
        self.moves += 1
        return None

    def move_forward_to(self, target: Entity, agents: List[Entity]):
        prev_pos = Coordinates(self.position.x, self.position.y)
        other = agents[0] if agents[0] != self else agents[-1]

        if self.position.x < target.position.x:
            self.direction = Direction.RIGHT
            self.position.x += 1
            if other.position == self.position:
                self.position = prev_pos
                return -1
            else:
                self.moves += 1
            return int(self.position == target.position)

        if self.position.x > target.position.x:
            self.direction = Direction.LEFT
            self.position.x -= 1
            if other.position == self.position:
                self.position = prev_pos
                return -1
            else:
                self.moves += 1
            return int(self.position == target.position)

        if self.position.y < target.position.y:
            self.direction = Direction.DOWN
            self.position.y += 1
            if other.position == self.position:
                self.position = prev_pos
                return -1
            else:
                self.moves += 1
            return int(self.position == target.position)

        if self.position.y > target.position.y:
            self.direction = Direction.UP
            self.position.y -= 1
            if other.position == self.position:
                self.position = prev_pos
                return -1
            else:
                self.moves += 1
            return int(self.position == target.position)
        return -1

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
