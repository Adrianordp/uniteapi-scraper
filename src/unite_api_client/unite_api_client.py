from httpx import AsyncClient
from bs4 import BeautifulSoup

from unite_api_client.build import Build
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

    async def update_pokemon_list(self):
        async with AsyncClient() as client:
            response = await client.get(self.meta_url, follow_redirects=True)

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
                "Failed to retrieve the webpage. Status code:",
                response.status_code,
            )

    async def get_pokemon_meta(self, pokemon: Pokemon):
        async with AsyncClient() as client:
            response = await client.get(
                self.route_pokemon_meta_url + pokemon.url_name,
                follow_redirects=True,
            )

        # Check if the request was successful (status code 200)
        if response.status_code != 200:
            print(
                "Failed to retrieve the webpage. Status code:",
                response.status_code,
            )
            return False
        soup = BeautifulSoup(response.content, "html.parser")
        pick_rate_str = soup.select(
            "div > div.m_4081bf90.mantine-Group-root > div:nth-child(1) > div > p"
        )
        win_rate_str = soup.select(
            "div > div.m_4081bf90.mantine-Group-root > div:nth-child(2) > div > p"
        )
        pick_rate = float(pick_rate_str[0].get_text().replace("%", ""))
        win_rate = float(win_rate_str[0].get_text().replace("%", ""))
        pokemon.set_pick_rate(pick_rate)
        pokemon.set_win_rate(win_rate)
        builds = soup.find_all("div", class_="sc-a9315c2e-0 dNgHcB")
        for build in builds:
            move1 = build.select(
                "div.fSlRro > div:nth-child(2) > div:nth-child(1) > p"
            )[0].get_text()
            move2 = build.select(
                "div.fSlRro > div:nth-child(2) > div:nth-child(2) > p"
            )[0].get_text()
            pick_rate_str = build.select(
                "div.fSlRro > div:nth-child(1) > div:nth-child(1) > p"
            )[1].get_text()
            win_rate_str = build.select(
                "div.fSlRro > div:nth-child(1) > div:nth-child(2) > p"
            )[1].get_text()
            pokemon.add_move_1(move1)
            pokemon.add_move_2(move2)
            win_rate = float(win_rate_str.replace("%", ""))
            pick_rate = float(pick_rate_str.replace("%", ""))
            build_obj = Build(pokemon, win_rate, pick_rate, move1, move2)
            pokemon.add_build(build_obj)
            self.builds.append(build_obj)
            print(build_obj)
            for idx in range(3):
                pick_rate_str = build.select(
                    "div > div:nth-child(1) > p.sc-6d6ea15e-3.LHyXa"
                )[idx].get_text()
                win_rate_str = build.select(
                    "div > div:nth-child(2) > p.sc-6d6ea15e-3.LHyXa"
                )[idx].get_text()
                pick_rate = float(pick_rate_str.replace("%", ""))
                win_rate = float(win_rate_str.replace("%", ""))
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
                    pokemon, win_rate, pick_rate, move1, move2, item
                )
                self.builds.append(build_obj)
                print(build_obj)

    def print_by_build_win_rate(self):
        print("\nSorted by win rate")
        self.builds.sort(reverse=True)
        with open("log/builds_by_build_win_rate.log", "w") as f:
            for build in self.builds:
                print(build)
                f.write(str(build) + "\n")

    def print_by_build_pick_rate(self):
        print("\nSorted by pick rate")
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.pick_rate, reverse=True)
        with open("log/builds_by_build_pick_rate.log", "w") as f:
            for build in self.builds:
                print(build)
                f.write(str(build) + "\n")

    def print_by_pokemon_name(self):
        print("\nSorted by pokemon")
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.pokemon.name)
        with open("log/builds_by_pokemon_name.log", "w") as f:
            for build in self.builds:
                print(build)
                f.write(str(build) + "\n")

    def print_by_item(self):
        print("\nSorted by item")
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.item)
        with open("log/builds_by_item.log", "w") as f:
            for build in self.builds:
                print(build)
                f.write(str(build) + "\n")

    def print_by_pokemon_win_rate(self):
        print("\nSorted by pokemon win rate")
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.pkm_win_rate, reverse=True)
        with open("log/builds_by_pokemon_win_rate.log", "w") as f:
            for build in self.builds:
                print(build)
                f.write(str(build) + "\n")

    def print_by_pokemon_pick_rate(self):
        print("\nSorted by pokemon pick rate")
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.pkm_pick_rate, reverse=True)
        with open("log/builds_by_pokemon_pick_rate.log", "w") as f:
            for build in self.builds:
                print(build)
                f.write(str(build) + "\n")
