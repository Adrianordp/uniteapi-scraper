import timeit
from asyncio import create_task, gather, run

from unite_api_client.unite_api_client import UniteAPIClient


async def uniteapi_client():
    api = UniteAPIClient()
    task = create_task(api.update_pokemon_list())
    await task

    result = gather(
        *[api.get_pokemon_meta(pokemon) for pokemon in api.pokemons]
    )
    await result
    api.save_build_win_rate()
    api.save_build_pick_rate()
    api.save_pokemon_name()
    api.save_pokemon_win_rate()
    api.save_pokemon_pick_rate()


def main():
    start = timeit.default_timer()
    run(uniteapi_client())
    stop = timeit.default_timer()
    print("Time: ", stop - start)


if __name__ == "__main__":
    main()
