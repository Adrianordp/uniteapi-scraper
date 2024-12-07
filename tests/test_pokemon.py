import pytest

from unite_api_client.pokemon import Pokemon, Role  # Assuming Role is an Enum


def test_pokemon_init():
    pokemon = Pokemon("Pikachu")
    assert pokemon.name == "Pikachu"
    assert pokemon.url_name == "pikachu"
    assert pokemon.role is None
    assert pokemon.pick_rate == 0
    assert pokemon.win_rate == 0
    assert pokemon.moves_1 == set()
    assert pokemon.moves_2 == set()


def test_pokemon_set_role():
    pokemon = Pokemon("Pikachu")
    pokemon.set_role(Role.ATTACKER)  # Assuming Role.ATTACKER is a valid role
    assert pokemon.role == Role.ATTACKER


def test_pokemon_set_pick_rate():
    pokemon = Pokemon("Pikachu")
    pokemon.set_pick_rate(50.5)
    assert pokemon.pick_rate == 50.5


def test_pokemon_set_win_rate():
    pokemon = Pokemon("Pikachu")
    pokemon.set_win_rate(60.5)
    assert pokemon.win_rate == 60.5


def test_pokemon_add_move_1():
    pokemon = Pokemon("Pikachu")
    pokemon.add_move_1("Thunderbolt")
    assert pokemon.moves_1 == {"Thunderbolt"}


def test_pokemon_add_move_2():
    pokemon = Pokemon("Pikachu")
    pokemon.add_move_2("Quick Attack")
    assert pokemon.moves_2 == {"Quick Attack"}


def test_pokemon_str():
    pokemon = Pokemon("Pikachu")
    assert str(pokemon) == "Pikachu"


def test_pokemon_invalid_role():
    pokemon = Pokemon("Pikachu")
    with pytest.raises(ValueError):
        pokemon.set_role("Invalid Role")


def test_pokemon_invalid_pick_rate():
    pokemon = Pokemon("Pikachu")
    with pytest.raises(ValueError):
        pokemon.set_pick_rate(-1)


def test_pokemon_invalid_win_rate():
    pokemon = Pokemon("Pikachu")
    with pytest.raises(ValueError):
        pokemon.set_win_rate(-1)


def test_pokemon_invalid_move():
    pokemon = Pokemon("Pikachu")
    with pytest.raises(TypeError):
        pokemon.add_move_1(["Invalid Move"])
