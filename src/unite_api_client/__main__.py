import timeit
from asyncio import create_task, gather, run

from httpx import AsyncClient

from unite_api_client.db_client import DatabaseClient
from unite_api_client.unite_api_client import UniteAPIClient


async def uniteapi_client():
    api = UniteAPIClient()
    async with AsyncClient() as session:
        check_last_update_details = create_task(
            api.check_last_update_details(session)
        )
        (date, number_of_games) = await check_last_update_details

        if not api.register_new_table(date, number_of_games):
            return

        task = create_task(api.update_pokemon_list(session))
        await task

        result = gather(
            *[
                api.get_pokemon_meta(pokemon, session)
                for pokemon in api.pokemons
            ]
        )
        await result
    api.save_builds_to_database()


def main():
    run(uniteapi_client())
    db = DatabaseClient()
    db._load_all_builds()
    db.print_by_build_win_rate25()


if __name__ == "__main__":
    main()
