import pytest

from unite_api_client.build import Build
from unite_api_client.pokemon import Pokemon


def test_build_init():
    pokemon = Pokemon("Pikachu")
    build = Build(pokemon, "move1", "move2", 50, 50)
    assert build.pokemon == pokemon
    assert build.move1 == "move1"
    assert build.move2 == "move2"
    assert build.m1m2_win_rate == 50
    assert build.m1m2_pick_rate == 50
    assert build.item == "Any"
    assert build.m1m2i_win_rate == 0
    assert build.m1m2i_pick_rate == 0
    assert build.pkm_win_rate == 0
    assert build.pkm_pick_rate == 0
    assert build.win_rate == 50


def test_build_str():
    pokemon = Pokemon("Pikachu")
    build = Build(pokemon, "move1", "move2", 50, 50)
    expected_str = (
        f"pkm: {pokemon}, "
        f"m1: move1, "
        f"m2: move2, "
        f"i: Any, "
        f"m1m2WR: 50 %, "
        f"m1m2PR: 50 %, "
        f"pkmWR: 0 %, "
        f"pkmPR: 0 %, "
        f"PR: 0.0000 %"
    )
    assert str(build) == expected_str


def test_build_str_with_item():
    pokemon = Pokemon("Pikachu", pick_rate=100)
    build = Build(
        pokemon,
        "move1",
        "move2",
        50,
        100,
        item="item1",
        m1m2i_win_rate=50,
        m1m2i_pick_rate=50,
    )
    expected_str = (
        f"pkm: Pikachu, "
        f"m1: move1, "
        f"m2: move2, "
        f"i: item1, "
        f"m1m2WR: 50 %, "
        f"m1m2PR: 100 %, "
        f"pkmWR: 0 %, "
        f"pkmPR: 100 %, "
        f"m1m2iWR: 50 %, "
        f"m1m2iPR: 50 %, "
        f"PR: 50.000000 %"
    )
    assert str(build) == expected_str


def test_build_with_pokemon_win_rate_and_pick_rate():
    pokemon = Pokemon("Pikachu")
    pokemon.set_win_rate(60)
    pokemon.set_pick_rate(60)
    build = Build(pokemon, "move1", "move2", 50, 50)
    assert build.pkm_win_rate == 60
    assert build.pkm_pick_rate == 60
