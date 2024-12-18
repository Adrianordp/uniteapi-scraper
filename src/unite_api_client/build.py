from unite_api_client.pokemon import Pokemon


class Build:
    def __init__(
        self,
        pokemon: Pokemon,
        move1: str,
        move2: str,
        m1m2_win_rate: float,
        m1m2_pick_rate: float,
        item: str = "Any",
        m1m2i_win_rate: float = 0,
        m1m2i_pick_rate: float = 0,
    ):
        self.pokemon = pokemon
        self.move1 = move1
        self.move2 = move2
        self.m1m2_win_rate = m1m2_win_rate
        self.m1m2_pick_rate = m1m2_pick_rate
        self.item = item
        self.m1m2i_win_rate = m1m2i_win_rate
        self.m1m2i_pick_rate = m1m2i_pick_rate

        self.pkm_win_rate = pokemon.win_rate
        self.pkm_pick_rate = pokemon.pick_rate

        self.win_rate = self.m1m2_win_rate
        self.build_pick_rate = (
            self.pokemon.pick_rate * self.m1m2_pick_rate / 100
        )
        self.pick_rate = self.build_pick_rate
        if self.item != "Any":
            self.win_rate = self.m1m2i_win_rate
            self.pick_rate = self.build_pick_rate * self.m1m2i_pick_rate / 100

    def __str__(self):
        if self.item == "Any":
            return (
                f"pkm: {self.pokemon}, "
                f"m1: {self.move1}, "
                f"m2: {self.move2}, "
                f"i: {self.item}, "
                f"m1m2WR: {self.m1m2_win_rate} %, "
                f"m1m2PR: {self.m1m2_pick_rate} %, "
                f"pkmWR: {self.pkm_win_rate} %, "
                f"pkmPR: {self.pkm_pick_rate} %, "
                f"BPR: {self.build_pick_rate:.3f} %"
            )
        return (
            f"pkm: {self.pokemon}, "
            f"m1: {self.move1}, "
            f"m2: {self.move2}, "
            f"i: {self.item}, "
            f"m1m2WR: {self.m1m2_win_rate} %, "
            f"m1m2PR: {self.m1m2_pick_rate} %, "
            f"pkmWR: {self.pkm_win_rate} %, "
            f"pkmPR: {self.pkm_pick_rate} %, "
            f"m1m2iWR: {self.m1m2i_win_rate} %, "
            f"m1m2iPR: {self.m1m2i_pick_rate} %, "
            f"BPR: {self.build_pick_rate:.3f} %, "
            f"PR: {self.pick_rate:.3f} %"
        )

    @staticmethod
    def convert_db_data_to_build(data):
        return Build(
            pokemon=Pokemon(data[1], data[10], data[11], role=data[2]),
            move1=data[3],
            move2=data[4],
            m1m2_win_rate=data[6],
            m1m2_pick_rate=data[7],
            item=data[5],
            m1m2i_win_rate=data[8],
            m1m2i_pick_rate=data[9],
        )

    def __gt__(self, other):
        return self.win_rate > other.win_rate

    def __lt__(self, other):
        return self.win_rate < other.win_rate

    def __eq__(self, other):
        return self.win_rate == other.win_rate

    def __ge__(self, other):
        return self.win_rate >= other.win_rate

    def __le__(self, other):
        return self.win_rate <= other.win_rate

    def __ne__(self, other):
        return self.win_rate != other.win_rate

    def __repr__(self):
        return (
            f"Build(pokemon={self.pokemon}, "
            f"win_rate={self.m1m2i_win_rate}, "
            f"pick_rate={self.m1m2i_pick_rate}, "
            f"move1={self.move1}, "
            f"move2={self.move2})"
        )
