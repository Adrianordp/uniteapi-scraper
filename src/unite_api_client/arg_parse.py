# src/unite_api_client/arg_parse.py
import argparse

from unite_api_client.db_client import DatabaseClient


class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.group = self.parser.add_mutually_exclusive_group()
        self.args = None

    def add_arguments(self):
        self.group.add_argument(
            "--pokemon",
            choices=["name", "win-rate", "pick-rate"],
        )

        self.group.add_argument(
            "--build",
            choices=[
                "pkm-name",
                "pkm-win-rate",
                "pkm-pick-rate",
                "win-rate",
                "pick-rate",
            ],
        )

        self.group.add_argument(
            "--full-build",
            choices=[
                "pkm-name",
                "pkm-win-rate",
                "pkm-pick-rate",
                "build-win-rate",
                "build-pick-rate",
                "item",
                "item-win-rate",
                "item-pick-rate",
                "win-rate",
                "pick-rate",
            ],
            help="Sort by build pick rate",
        )

        self.parser.add_argument(
            "--limit",
            type=float,
            help="Limit the lower percentage to consider",
        )

    def parse_args(self):
        self.args = self.parser.parse_args()

    def run(self, dbc: DatabaseClient = None):
        self.add_arguments()
        self.parse_args()
        if dbc is None:
            return
        self.process_args(dbc)

    def process_args(self, dbc: DatabaseClient):
        if self.args.limit:
            dbc.set_pick_rate_threshold(self.args.limit)

        if self.args.pokemon == "name":
            dbc.print_pokemon_by_name()
        elif self.args.pokemon == "win-rate":
            dbc.print_pokemon_by_win_rate()
        elif self.args.pokemon == "pick-rate":
            dbc.print_pokemon_by_pick_rate()

        elif self.args.build == "pkm-name":
            dbc.print_build_by_pokemon_name()
        elif self.args.build == "pkm-win-rate":
            dbc.print_build_by_pokemon_win_rate()
        elif self.args.build == "pkm-pick-rate":
            dbc.print_build_by_pokemon_pick_rate()
        elif self.args.build == "win-rate":
            dbc.print_build_by_win_rate()
        elif self.args.build == "pick-rate":
            dbc.print_build_by_pick_rate()

        elif self.args.full_build == "pkm-name":
            dbc.print_full_build_by_pokemon_name()
        elif self.args.full_build == "pkm-win-rate":
            dbc.print_full_build_by_pokemon_win_rate()
        elif self.args.full_build == "pkm-pick-rate":
            dbc.print_full_build_by_pokemon_pick_rate()
        elif self.args.full_build == "build-win-rate":
            dbc.print_full_build_by_build_win_rate()
        elif self.args.full_build == "build-pick-rate":
            dbc.print_full_build_by_build_pick_rate()
        elif self.args.full_build == "item":
            dbc.print_by_item()
        elif self.args.full_build == "win-rate":
            dbc.print_full_build_by_win_rate()
        elif self.args.full_build == "pick-rate":
            dbc.print_full_build_by_pick_rate()


if __name__ == "__main__":
    arg_parser = ArgParser()
    arg_parser.run()
