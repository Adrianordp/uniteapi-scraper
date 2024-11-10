class Build:
    def __init__(self, pokemon, win_rate, pick_rate, move1, move2, item="Any"):
        self.pokemon = pokemon
        self.win_rate = win_rate
        self.pick_rate = pick_rate
        self.move1 = move1
        self.move2 = move2
        self.item = item

    def __str__(self):
        return (
            f"pokemon: {self.pokemon}, "
            f"pick rate: {self.pick_rate} %, "
            f"win rate: {self.win_rate} %, "
            f"move_1: {self.move1}, "
            f"move_2: {self.move2}, "
            f"item: {self.item}"
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
            f"win_rate={self.win_rate}, "
            f"pick_rate={self.pick_rate}, "
            f"move1={self.move1}, "
            f"move2={self.move2})"
        )
