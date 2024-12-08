import errno
from statistics import quantiles

from unite_api_client.build import Build
from unite_api_client.handle_database import HandleDatabase


def ignore_pipe_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IOError as error:
            if error.errno != errno.EPIPE:
                pass

    return inner


class DatabaseClient:
    def __init__(self):
        self.handle_database = HandleDatabase()
        self.builds: list[Build] = [Build] * 0
        self.table_name: str = self.handle_database.get_table_names()[-1][1]
        self.pick_rate_threshold = 0

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

    def set_pick_rate_threshold(self, pick_rate_threshold):
        self.pick_rate_threshold = pick_rate_threshold

    @ignore_pipe_error
    def _print_pokemons(self):
        seen_pokemon = set()
        for build in self.builds:
            if build.pokemon.name in seen_pokemon:
                continue
            if build.pkm_pick_rate < self.pick_rate_threshold:
                continue
            else:
                seen_pokemon.add(build.pokemon.name)
            string = (
                f"pkm: {build.pokemon}, "
                f"WR: {build.pkm_win_rate} %, "
                f"PR: {build.pkm_pick_rate} %"
            )
            print(string)

    def print_pokemon_by_name(self):
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.pokemon.name)
        self._print_pokemons()

    def print_pokemon_by_win_rate(self):
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.pkm_win_rate, reverse=True)
        self._print_pokemons()

    def print_pokemon_by_pick_rate(self):
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.pkm_pick_rate, reverse=True)
        self._print_pokemons()

    @ignore_pipe_error
    def _print_builds(self):
        for build in self.builds:
            if build.item != "Any":
                continue
            if build.build_pick_rate < self.pick_rate_threshold:
                continue
            string = (
                f"pkm: {build.pokemon}, "
                f"m1: {build.move1}, "
                f"m2: {build.move2}, "
                f"pkmWR: {build.pkm_win_rate} %, "
                f"pkmPR: {build.pkm_pick_rate} %, "
                f"m1m2WR: {build.m1m2_win_rate} %, "
                f"m1m2PR: {build.m1m2_pick_rate} %, "
                f"PR: {build.build_pick_rate:.4f} %"
            )
            print(string)

    def print_build_by_pokemon_name(self):
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.pokemon.name)
        self._print_builds()

    def print_build_by_pokemon_win_rate(self):
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.pkm_win_rate, reverse=True)
        self._print_builds()

    def print_build_by_pokemon_pick_rate(self):
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.pkm_pick_rate, reverse=True)
        self._print_builds()

    def print_build_by_win_rate(self):
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.m1m2_win_rate, reverse=True)
        self._print_builds()

    def print_build_by_pick_rate(self):
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.pick_rate, reverse=True)
        self._print_builds()

    def print_full_build_by_pokemon_name(self):
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.pokemon.name)
        for build in self.builds:
            if build.item == "Any":
                continue
            if build.pick_rate < self.pick_rate_threshold:
                continue
            print(build)

    def print_full_build_by_pokemon_win_rate(self):
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.pkm_win_rate, reverse=True)
        for build in self.builds:
            if build.item == "Any":
                continue
            if build.pick_rate < self.pick_rate_threshold:
                continue
            print(build)

    def print_full_build_by_pokemon_pick_rate(self):
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.pokemon.pick_rate, reverse=True)
        for build in self.builds:
            if build.item == "Any":
                continue
            if build.pick_rate < self.pick_rate_threshold:
                continue
            print(build)

    def print_full_build_by_build_win_rate(self):
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.m1m2_win_rate, reverse=True)
        for build in self.builds:
            if build.item == "Any":
                continue
            if build.pick_rate < self.pick_rate_threshold:
                continue
            print(build)

    def print_full_build_by_build_pick_rate(self):
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.build_pick_rate, reverse=True)
        for build in self.builds:
            if build.item == "Any":
                continue
            if build.pick_rate < self.pick_rate_threshold:
                continue
            print(build)

    def print_full_build_by_item(self):
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.item, reverse=True)
        for build in self.builds:
            if build.item == "Any":
                continue
            if build.pick_rate < self.pick_rate_threshold:
                continue
            print(build)

    def print_full_build_by_win_rate(self):
        self.builds.sort(reverse=True)
        for build in self.builds:
            if build.item == "Any":
                continue
            if build.pick_rate < self.pick_rate_threshold:
                continue
            print(build)

    def print_full_build_by_pick_rate(self):
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.pick_rate, reverse=True)
        for build in self.builds:
            if build.item == "Any":
                continue
            if build.pick_rate < self.pick_rate_threshold:
                continue
            print(build)

    def print_by_build_win_rate25(self):
        threshold = self._get_pick_rate_threshold()
        self.builds.sort(reverse=True)
        for build in self.builds:
            if build.pick_rate < threshold:
                continue
            print(build)

    def print_by_item(self):
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.item)
        for build in self.builds:
            print(build)
