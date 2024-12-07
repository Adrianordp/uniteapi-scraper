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
        if not isinstance(role, Role):
            raise ValueError(f"Invalid role: {role}")
        self.role = role

    def set_pick_rate(self, pick_rate: float):
        if pick_rate < 0 or pick_rate > 100:
            raise ValueError(f"Invalid pick rate: {pick_rate}")
        self.pick_rate = pick_rate

    def set_win_rate(self, win_rate: float):
        if win_rate < 0 or win_rate > 100:
            raise ValueError(f"Invalid win rate: {win_rate}")
        self.win_rate = win_rate

    def add_move_1(self, move_1: str):
        if not isinstance(move_1, str):
            raise TypeError(f"Invalid move_1 type: {type(move_1)}")
        self.moves_1.add(move_1)

    def add_move_2(self, move_2: str):
        if not isinstance(move_2, str):
            raise TypeError(f"Invalid move_2 type: {type(move_2)}")
        self.moves_2.add(move_2)
