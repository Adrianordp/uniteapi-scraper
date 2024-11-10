import requests
from bs4 import BeautifulSoup

from unite_api_client.build import Build


class UniteAPIClient:
    def __init__(self):
        self.base_url = "https://uniteapi.dev/"
        self.route_meta = "meta/"
        self.meta_url = self.base_url + self.route_meta
        self.route_pokemon_meta = "pokemon-unite-meta-for-"
        self.route_pokemon_meta_url = self.meta_url + self.route_pokemon_meta
        self.pokemons: list[str] = [""] * 0
        self.builds: list[Build] = [Build("", 0, 0, "", "")] * 0

    def update_pokemon_list(self):
        response = requests.get(self.meta_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")

            # Example: Find a specific element by class
            pokemons = soup.find_all("div", class_="sc-9fa03fa-1")
            for pokemon in pokemons:
                pokemon_name = pokemon.get_text()
                pokemon_url_name = pokemon_name.casefold().replace(" ", "")
                self.pokemons.append(pokemon_url_name)
        else:
            print(
                "Failed to retrieve the webpage. Status code:",
                response.status_code,
            )

    def get_pokemon_meta(self, pokemon: str):
        response = requests.get(self.route_pokemon_meta_url + pokemon)

        # Check if the request was successful (status code 200)
        if response.status_code != 200:
            print(
                "Failed to retrieve the webpage. Status code:",
                response.status_code,
            )
            return False
        soup = BeautifulSoup(response.content, "html.parser")
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
            win_rate = float(win_rate_str.replace("%", ""))
            pick_rate = float(pick_rate_str.replace("%", ""))
            build_obj = Build(pokemon, win_rate, pick_rate, move1, move2)
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

    def print_by_win_rate(self):
        print("\nSorted by win rate")
        self.builds.sort(reverse=True)
        with open("builds_by_win_rate.log", "w") as f:
            for build in self.builds:
                print(build)
                f.write(str(build) + "\n")

    def print_by_pick_rate(self):
        print("\nSorted by pick rate")
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.pick_rate, reverse=True)
        with open("builds_by_pick_rate.log", "w") as f:
            for build in self.builds:
                print(build)
                f.write(str(build) + "\n")

    def print_by_pokemon(self):
        print("\nSorted by pokemon")
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.pokemon)
        with open("builds_by_pokemon.log", "w") as f:
            for build in self.builds:
                print(build)
                f.write(str(build) + "\n")
