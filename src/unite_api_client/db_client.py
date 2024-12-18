import errno
from statistics import quantiles

import numpy as np

from unite_api_client.build import Build
from unite_api_client.handle_database import HandleDatabase
from unite_api_client.paint import Paint


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
        self.using_percentile = False
        self.percentile = 0
        self.paint = Paint()

    def set_colors(self, use_colors=True):
        self.paint.set_enabled(use_colors)

    def set_table_name(self, table_name):
        self.table_name = table_name

    def get_table_names(self):
        self.handle_database.cursor.execute("SELECT * FROM table_list")
        fetch = self.handle_database.cursor.fetchall()

        return [row[3] for row in fetch]

    def _load_all_builds(self):
        builds = self.handle_database.get_all_builds(self.table_name)
        self.builds: list[Build] = [Build] * 0
        for build in builds:
            self.builds.append(Build.convert_db_data_to_build(build))

    def _get_pick_rate_threshold(self):
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.pick_rate, reverse=True)
        pr_list = []
        for build in self.builds:
            pr_list.append(build.pick_rate)
        quant = quantiles(pr_list)
        return quant[-1]

    def set_pick_rate_threshold(self, pick_rate_threshold):
        self.pick_rate_threshold = pick_rate_threshold

    def set_percentile(self, percentile):
        self.using_percentile = True
        if percentile > 100 or percentile < 0:
            raise ValueError(f"Invalid percentile: {percentile}")
        self.percentile = percentile

    def _set_percentile_threshold(self, pick_rate_list: list[float]):
        threshold = np.percentile(pick_rate_list, 100 - self.percentile)
        self.set_pick_rate_threshold(threshold)

    def _get_pokemon_builds(self):
        seen_pokemon = set()
        builds: list[Build] = [Build] * 0
        for build in self.builds:
            if build.pokemon.name in seen_pokemon:
                continue
            else:
                seen_pokemon.add(build.pokemon.name)
            builds.append(build)
        return builds

    def _set_threshold_if_using_pkm_percentile(self, builds: list[Build]):
        if self.using_percentile:
            pick_rate_list = [build.pkm_pick_rate for build in builds]
            self._set_percentile_threshold(pick_rate_list)

    @ignore_pipe_error
    def _print_pokemons(self):
        builds = self._get_pokemon_builds()

        self._set_threshold_if_using_pkm_percentile(builds)

        p = self.paint

        for build in builds:
            if build.pkm_pick_rate < self.pick_rate_threshold:
                continue
            string = (
                f"pkm:{p.red(build.pokemon)}, "
                f"WR:{p.green(build.pkm_win_rate)}, "
                f"PR:{p.blue(build.pkm_pick_rate)}"
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

    def _get_move_builds(self):
        builds: list[Build] = [Build] * 0

        for build in self.builds:
            if build.item != "Any":
                continue
            builds.append(build)

        return builds

    def _set_threshold_if_using_move_percentile(self, builds: list[Build]):
        if self.using_percentile:
            pick_rate_list = [build.build_pick_rate for build in builds]
            self._set_percentile_threshold(pick_rate_list)

    @ignore_pipe_error
    def _print_builds(self):
        builds = self._get_move_builds()

        self._set_threshold_if_using_move_percentile(builds)

        p = self.paint

        for build in builds:
            if build.build_pick_rate < self.pick_rate_threshold:
                continue
            string = (
                f"pkm:{p.red(build.pokemon)}, "
                f"m1:{p.orange(build.move1)}, "
                f"m2:{p.orange(build.move2)}, "
                f"pkmWR:{p.green(build.pkm_win_rate)}, "
                f"pkmPR:{p.blue(build.pkm_pick_rate)}, "
                f"m1m2WR:{p.light_green(build.m1m2_win_rate)}, "
                f"m1m2PR:{p.light_blue(build.m1m2_pick_rate)}, "
                f"PR:{p.lighter_blue(f'{build.build_pick_rate:.4f}')}"
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

    def _get_full_builds(self):
        builds: list[Build] = [Build] * 0
        for build in self.builds:
            if build.item == "Any":
                continue
            builds.append(build)
        return builds

    def _set_threshold_if_using_full_build_percentile(
        self, builds: list[Build]
    ):
        if self.using_percentile:
            pick_rate_list = [build.pick_rate for build in builds]
            self._set_percentile_threshold(pick_rate_list)

    @ignore_pipe_error
    def _print_full_builds(self):
        builds = self._get_full_builds()

        self._set_threshold_if_using_full_build_percentile(builds)

        p = self.paint

        for build in builds:
            if build.pick_rate < self.pick_rate_threshold:
                continue
            string = (
                f"pkm:{p.red(build.pokemon)}, "
                f"m1:{p.orange(build.move1)}, "
                f"m2:{p.orange(build.move2)}, "
                f"i:{p.yellow(build.item)}, "
                f"pkmWR:{p.green(build.pkm_win_rate)}, "
                f"pkmPR:{p.blue(build.pkm_pick_rate)}, "
                f"m1m2WR:{p.light_green(build.m1m2_win_rate)}, "
                f"m1m2PR:{p.light_blue(build.m1m2_pick_rate)}, "
                f"m1m2iWR:{p.magenta(build.m1m2i_win_rate)}, "
                f"m1m2iPR:{p.cyan(build.m1m2i_pick_rate)}, "
                f"BPR:{p.lighter_blue(f'{build.build_pick_rate:.3f}')}, "
                f"PR:{p.light_magenta(f'{build.pick_rate:.3f}')}"
            )
            print(string)

    def print_full_build_by_pokemon_name(self):
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.pokemon.name)
        self._print_full_builds()

    def print_full_build_by_pokemon_win_rate(self):
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.pkm_win_rate, reverse=True)
        self._print_full_builds()

    def print_full_build_by_pokemon_pick_rate(self):
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.pokemon.pick_rate, reverse=True)
        self._print_full_builds()

    def print_full_build_by_build_win_rate(self):
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.m1m2_win_rate, reverse=True)
        self._print_full_builds()

    def print_full_build_by_build_pick_rate(self):
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.build_pick_rate, reverse=True)
        self._print_full_builds()

    def print_full_build_by_item(self):
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.item, reverse=True)
        self._print_full_builds()

    def print_full_build_by_win_rate(self):
        self.builds.sort(reverse=True)
        self._print_full_builds()

    def print_full_build_by_pick_rate(self):
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.pick_rate, reverse=True)
        self._print_full_builds()

    def print_full_build_by_item(self):
        self.builds.sort(reverse=True)
        self.builds.sort(key=lambda x: x.item)
        self._print_full_builds()

    def print_by_build_win_rate25(self):
        threshold = self._get_pick_rate_threshold()
        self.builds.sort(reverse=True)
        for build in self.builds:
            if build.pick_rate < threshold:
                continue
            print(build)
