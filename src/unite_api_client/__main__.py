import timeit
from asyncio import create_task, gather, run

from httpx import AsyncClient

from unite_api_client.unite_api_client import UniteAPIClient


async def uniteapi_client():
    api = UniteAPIClient()
    async with AsyncClient() as session:
        task = create_task(api.update_pokemon_list(session))
        await task

        result = gather(
            *[
                api.get_pokemon_meta(pokemon, session)
                for pokemon in api.pokemons
            ]
        )
        await result
    api.save_build_win_rate()
    api.save_build_pick_rate()
    api.save_pokemon_name()
    api.save_pokemon_win_rate()
    api.save_pokemon_pick_rate()
    api.save_build_win_rate25()


def main():
    start = timeit.default_timer()
    run(uniteapi_client())
    stop = timeit.default_timer()
    print("Time: ", stop - start)


if __name__ == "__main__":
    main()
