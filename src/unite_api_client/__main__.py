from unite_api_client.unite_api_client import UniteAPIClient


def main():
    api = UniteAPIClient()
    api.update_pokemon_list()
    for pokemon in api.pokemons:
        print(pokemon)
        api.get_pokemon_meta(pokemon)

    api.print_by_build_win_rate()
    api.print_by_build_pick_rate()
    api.print_by_pokemon_name()
    api.print_by_pokemon_win_rate()
    api.print_by_pokemon_pick_rate()


if __name__ == "__main__":
    main()
