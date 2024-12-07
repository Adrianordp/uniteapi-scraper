from unittest.mock import Mock, patch

import pytest

from unite_api_client.build import Build
from unite_api_client.pokemon import Pokemon
from unite_api_client.unite_api_client import UniteAPIClient


@pytest.fixture
def api_client():
    return UniteAPIClient()


def test_init(api_client: UniteAPIClient):
    assert api_client.base_url == "https://uniteapi.dev/"
    assert api_client.route_meta == "meta/"
    assert api_client.meta_url == "https://uniteapi.dev/meta/"
    assert api_client.route_pokemon_meta == "pokemon-unite-meta-for-"
    assert (
        api_client.route_pokemon_meta_url
        == "https://uniteapi.dev/meta/pokemon-unite-meta-for-"
    )
    assert api_client.pokemons == []
    assert api_client.builds == []


# @pytest.mark.asyncio
# @patch("unite_api_client.unite_api_client.AsyncClient")
# async def test_update_pokemon_list(
#     mock_async_client, api_client: UniteAPIClient
# ):
#     mock_response = Mock()
#     mock_response.status_code = 200
#     mock_response.content = b"<html><body>Mock HTML content</body></html>"
#     mock_async_client.return_value.get.return_value.__aenter__.return_value = (
#         mock_response
#     )
#     await api_client.update_pokemon_list(mock_async_client())
#     assert (
#         api_client.pokemons == []
#     )  # Assuming the HTML content is not parsed correctly


# @pytest.mark.asyncio
# @patch("unite_api_client.unite_api_client.AsyncClient")
# async def test_get_pokemon_meta(mock_async_client, api_client: UniteAPIClient):
#     pokemon = Pokemon("Pikachu")
#     api_client.pokemons = [pokemon]
#     mock_response = Mock()
#     mock_response.status_code = 200
#     mock_response.content = b"<html><body>Mock HTML content</body></html>"
#     mock_async_client.return_value.get.return_value.__aenter__.return_value = (
#         mock_response
#     )
#     await api_client.get_pokemon_meta(pokemon, mock_async_client())
#     # Assuming the HTML content is not parsed correctly, no assertions are made


def test_print_by_pokemon_name(api_client: UniteAPIClient):
    pokemon1 = Pokemon("Pikachu")
    pokemon2 = Pokemon("Charizard")
    build1 = Build(pokemon1, "move1", "move2", 50, 50)
    build2 = Build(pokemon2, "move3", "move4", 60, 60)
    api_client.builds = [build1, build2]
    api_client.print_by_pokemon_name()
    # No assertions are made as this method only prints to the console


def test_save_pokemon_name(api_client: UniteAPIClient):
    pokemon1 = Pokemon("Pikachu")
    pokemon2 = Pokemon("Charizard")
    build1 = Build(pokemon1, "move1", "move2", 50, 50)
    build2 = Build(pokemon2, "move3", "move4", 60, 60)
    api_client.builds = [build1, build2]
    api_client.save_pokemon_name()
    # No assertions are made as this method only writes to a file
