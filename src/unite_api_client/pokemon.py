from enum import Enum


class Role(Enum):
    ATTACKER = 1
    SUPPORT = 2
    DEFENDER = 3
    SPEEDSTER = 4
    ALLROUNDER = 5


class Pokemon:
    def __init__(
        self,
        name: str,
        win_rate: float = 0,
        pick_rate: float = 0,
        role: Role = None,
        moves_1: set[str] = set(),
        moves_2: set[str] = set(),
    ):
        self.name = name
        self.url_name = name.casefold().replace(" ", "").replace(".", "")
        self.role = role
        self.pick_rate = pick_rate
        self.win_rate = win_rate
        self.moves_1 = moves_1
        self.moves_2 = moves_2

    def __str__(self):
        return self.name

    def set_role(self, role: Role):
        self.role = role

    def set_pick_rate(self, pick_rate: float):
        self.pick_rate = pick_rate

    def set_win_rate(self, win_rate: float):
        self.win_rate = win_rate

    def add_move_1(self, move_1: str):
        self.moves_1.add(move_1)

    def add_move_2(self, move_2: str):
        self.moves_2.add(move_2)
