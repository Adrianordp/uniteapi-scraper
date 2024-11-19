import timeit
from asyncio import create_task, gather, run

from unite_api_client.unite_api_client import UniteAPIClient


async def main():
    api = UniteAPIClient()
    task = create_task(api.update_pokemon_list())
    await task

    result = gather(
        *[api.get_pokemon_meta(pokemon) for pokemon in api.pokemons]
    )
    await result
    api.print_by_build_win_rate()
    api.print_by_build_pick_rate()
    api.print_by_pokemon_name()
    api.print_by_pokemon_win_rate()
    api.print_by_pokemon_pick_rate()


if __name__ == "__main__":
    start = timeit.default_timer()
    run(main())
    stop = timeit.default_timer()
    print("Time: ", stop - start)
