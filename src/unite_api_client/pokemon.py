from enum import Enum

from unite_api_client.build import Build


class Role(Enum):
    Attacker = 1
    Support = 2
    Defender = 3
    Speedister = 4
    Allrounder = 5


class Pokemon:
    def __init__(
        self,
        name: str,
        win_rate: float = 0,
        pick_rate: float = 0,
        role: Role = None,
        move_1: str = None,
        move_2: str = None,
    ):
        self.name = name
        self.builds = [Build] * 0
        self.role = role
        self.pick_rate = pick_rate
        self.win_rate = win_rate
        self.move_1 = move_1
        self.move_2 = move_2

    def set_role(self, role: Role):
        self.role = role

    def set_pick_rate(self, pick_rate: float):
        self.pick_rate = pick_rate

    def set_win_rate(self, win_rate: float):
        self.win_rate = win_rate

    def add_build(self, build: Build):
        self.builds.append(build)

    def set_move_1(self, move_1: str):
        self.move_1 = move_1

    def set_move_2(self, move_2: str):
        self.move_2 = move_2
