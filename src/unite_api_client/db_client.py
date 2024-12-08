from statistics import quantiles

from unite_api_client.build import Build
from unite_api_client.handle_database import HandleDatabase


class DatabaseClient:
    def __init__(self):
        self.handle_database = HandleDatabase()
        self.builds: list[Build] = [Build] * 0
        self.table_name: str = self.handle_database.get_table_names()[-1][1]

    def _load_all_builds(self):
        builds = self.handle_database.get_all_builds(self.table_name)
        for build in builds:
            self.builds.append(Build.convert_db_data_to_build(build))

    def _get_pick_rate_threshold(self):
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.pick_rate, reverse=True)
        pr_list = []
        for build in self.builds:
            pr_list.append(build.pick_rate)
        quant = quantiles(pr_list)
        print(f"Quantiles are {quant}")
        return quant[-1]

    def print_by_pokemon_name(self):
        print("\nSorted by pokemon")
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.pokemon.name)
        past_pokemon = set()
        for build in self.builds:
            if build.pokemon.name in past_pokemon:
                continue
            else:
                past_pokemon.add(build.pokemon.name)
            string = (
                f"pkm: {build.pokemon}, "
                f"WR: {build.pkm_win_rate} %, "
                f"PR: {build.pkm_pick_rate} %"
            )
            print(string)

    def print_by_pokemon_win_rate(self):
        print("\nSorted by pokemon win rate")
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.pkm_win_rate, reverse=True)
        past_pokemon = set()
        for build in self.builds:
            if build.pokemon.name in past_pokemon:
                continue
            else:
                past_pokemon.add(build.pokemon.name)
            string = (
                f"pkm: {build.pokemon}, "
                f"WR: {build.pkm_win_rate} %, "
                f"PR: {build.pkm_pick_rate} %"
            )
            print(string)

    def print_by_pokemon_pick_rate(self):
        print("\nSorted by pokemon pick rate")
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.pkm_pick_rate, reverse=True)
        past_pokemon = set()
        for build in self.builds:
            if build.pokemon.name in past_pokemon:
                continue
            else:
                past_pokemon.add(build.pokemon.name)
            string = (
                f"pkm: {build.pokemon}, "
                f"WR: {build.pkm_win_rate} %, "
                f"PR: {build.pkm_pick_rate} %"
            )
            print(string)

    def print_by_build_pokemon_name(self):
        print("\nSorted build by pokemon name")
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.pokemon.name)
        for build in self.builds:
            print(build)

    def print_by_build_win_rate25(self):
        threshold = self._get_pick_rate_threshold()
        self.builds.sort(reverse=True)
        for build in self.builds:
            if build.pick_rate < threshold:
                continue
            print(build)

    def print_by_build_win_rate(self):
        self.builds.sort(reverse=True)
        for build in self.builds:
            print(build)

    def print_by_build_pick_rate(self):
        print("\nSorted by pick rate")
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.m1m2i_pick_rate, reverse=True)
        for build in self.builds:
            print(build)

    def print_by_item(self):
        print("\nSorted by item")
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.item)
        for build in self.builds:
            print(build)
