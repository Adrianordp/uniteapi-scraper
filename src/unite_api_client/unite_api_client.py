from statistics import quantiles

from bs4 import BeautifulSoup
from httpx import AsyncClient

from unite_api_client.build import Build
from unite_api_client.handle_database import HandleDatabase
from unite_api_client.pokemon import Pokemon


class UniteAPIClient:
    def __init__(self):
        self.base_url = "https://uniteapi.dev/"
        self.route_meta = "meta/"
        self.meta_url = self.base_url + self.route_meta
        self.route_pokemon_meta = "pokemon-unite-meta-for-"
        self.route_pokemon_meta_url = self.meta_url + self.route_pokemon_meta
        self.pokemons: list[Pokemon] = [Pokemon] * 0
        self.builds: list[Build] = [Build] * 0
        self.handle_database = HandleDatabase()
        self.table_name: str = None

    async def check_last_update_details(self, session: AsyncClient):
        response = await session.get(self.meta_url, follow_redirects=True)
        soup = BeautifulSoup(response.content, "html.parser")
        date = soup.select(
            "div:nth-child(1) > p.mantine-focus-auto.simpleStat_count__dG_xB.m_b6d8b162.mantine-Text-root"
        )[0].get_text()
        number_of_games = int(
            soup.select(
                "div:nth-child(2) > p.mantine-focus-auto.simpleStat_count__dG_xB.m_b6d8b162.mantine-Text-root"
            )[0].get_text()
        )
        return (date, number_of_games)

    async def update_pokemon_list(self, session: AsyncClient):
        response = await session.get(self.meta_url, follow_redirects=True)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")

            # Example: Find a specific element by class
            pokemons = soup.find_all("div", class_="sc-9fa03fa-1")
            for pokemon in pokemons:
                pokemon_name = pokemon.get_text()
                pokemon = Pokemon(pokemon_name)
                self.pokemons.append(pokemon)
        else:
            print(
                f"Failed to retrieve the webpage {self.meta_url + pokemon.url_name}. Status code:",
                response.status_code,
            )

    async def get_pokemon_meta(self, pokemon: Pokemon, session: AsyncClient):
        success = False
        retrying_count = 0
        while not success:
            try:
                response = await session.get(
                    self.route_pokemon_meta_url + pokemon.url_name,
                    follow_redirects=True,
                )
                success = True
                if retrying_count > 0:
                    print(f"Successfully retrieved {pokemon.url_name}.")
            except Exception as error:
                print(
                    f"Error: {error} in url {self.route_pokemon_meta_url + pokemon.url_name}. Retrying..."
                )
                retrying_count += 1
                if retrying_count > 10:
                    print(
                        f"Failed to retrieve the webpage {pokemon.url_name}. Status code:",
                        response.status_code,
                    )
                    return False

        # Check if the request was successful (status code 200)
        if response.status_code != 200:
            print(
                f"Failed to retrieve the webpage {self.meta_url + pokemon.url_name}. Status code:",
                response.status_code,
            )
            return False
        soup = BeautifulSoup(response.content, "html.parser")
        pkm_pick_rate_str = soup.select(
            "div > div.m_4081bf90.mantine-Group-root > div:nth-child(1) > div > p"
        )
        pkm_win_rate_str = soup.select(
            "div > div.m_4081bf90.mantine-Group-root > div:nth-child(2) > div > p"
        )
        pkm_pick_rate = float(pkm_pick_rate_str[0].get_text().replace("%", ""))
        pkm_win_rate = float(pkm_win_rate_str[0].get_text().replace("%", ""))
        pokemon.set_pick_rate(pkm_pick_rate)
        pokemon.set_win_rate(pkm_win_rate)
        builds = soup.find_all("div", class_="sc-a9315c2e-0 dNgHcB")
        for build in builds:
            move1and2_pick_rate_str = build.select(
                "div.sc-34a5201c-0.fSlRro > div:nth-child(1) > div:nth-child(1) > p.sc-6d6ea15e-4.eZnfiD"
            )[0].get_text()
            move1and2_win_rate_str = build.select(
                "div.sc-34a5201c-0.fSlRro > div:nth-child(1) > div:nth-child(2) > p.sc-6d6ea15e-4.eZnfiD"
            )
            move1 = build.select(
                "div.fSlRro > div:nth-child(2) > div:nth-child(1) > p"
            )[0].get_text()
            move2 = build.select(
                "div.fSlRro > div:nth-child(2) > div:nth-child(2) > p"
            )[0].get_text()
            items_pick_rate_str = build.select(
                "div.fSlRro > div:nth-child(1) > div:nth-child(1) > p"
            )[1].get_text()
            items_win_rate_str = build.select(
                "div.fSlRro > div:nth-child(1) > div:nth-child(2) > p"
            )[1].get_text()
            pokemon.add_move_1(move1)
            pokemon.add_move_2(move2)
            move1and2_pick_rate = float(
                move1and2_pick_rate_str.replace("%", "")
            )
            move1and2_win_rate = float(
                move1and2_win_rate_str[0].get_text().replace("%", "")
            )
            items_win_rate = float(items_win_rate_str.replace("%", ""))
            items_pick_rate = float(items_pick_rate_str.replace("%", ""))
            build_obj = Build(
                pokemon, move1, move2, move1and2_win_rate, move1and2_pick_rate
            )
            self.builds.append(build_obj)
            for idx in range(3):
                items_pick_rate_str = build.select(
                    "div > div:nth-child(1) > p.sc-6d6ea15e-3.LHyXa"
                )[idx].get_text()
                items_win_rate_str = build.select(
                    "div > div:nth-child(2) > p.sc-6d6ea15e-3.LHyXa"
                )[idx].get_text()
                items_pick_rate = float(items_pick_rate_str.replace("%", ""))
                items_win_rate = float(items_win_rate_str.replace("%", ""))
                item = (
                    build.select(
                        f"div.sc-a9315c2e-3.bpaMUh > div:nth-child("
                        f"{idx + 1}"
                        f") > img"
                    )[0]["src"]
                    .split(".png")[0]
                    .split("_")[-1]
                )
                build_obj = Build(
                    pokemon,
                    move1,
                    move2,
                    move1and2_win_rate,
                    move1and2_pick_rate,
                    item,
                    items_win_rate,
                    items_pick_rate,
                )
                self.builds.append(build_obj)

    def save_builds_to_database(self):
        for build in self.builds:
            self.handle_database.insert_build(build)

    def register_new_table(self, date, number_of_games):
        self.table_name = f"{date}_{number_of_games}".replace(" ", "_")
        if not self.handle_database.register_new_table(
            date, number_of_games, self.table_name
        ):
            return False
        return True
