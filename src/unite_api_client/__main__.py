import sys
from asyncio import create_task, gather, run

from httpx import AsyncClient

from unite_api_client.arg_parse import ArgParser
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
    arg_parser = ArgParser()

    if "-h" in sys.argv or "--help" in sys.argv:
        arg_parser.run()
        return

    run(uniteapi_client())

    dbc = DatabaseClient()

    arg_parser.run(dbc)


if __name__ == "__main__":
    main()
