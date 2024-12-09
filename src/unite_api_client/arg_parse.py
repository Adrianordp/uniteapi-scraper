# src/unite_api_client/arg_parse.py
import argparse

from unite_api_client.db_client import DatabaseClient


class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.group_target = self.parser.add_mutually_exclusive_group()
        self.group_threshold = self.parser.add_mutually_exclusive_group()
        self.args = None

    def add_arguments(self):
        self.group_target.add_argument(
            "--Pokemon",
            "-P",
            choices=["name", "win-rate", "pick-rate"],
            help="Display pokemon data. Use choices to filter",
        )

        self.group_target.add_argument(
            "--Build",
            "-B",
            choices=[
                "pkm-name",
                "pkm-win-rate",
                "pkm-pick-rate",
                "win-rate",
                "pick-rate",
            ],
            help="Display builds data. Use choices to filter",
        )

        self.group_target.add_argument(
            "--Full-build",
            "-F",
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
            help="Display full builds data. Use choices to filter",
        )

        self.group_threshold.add_argument(
            "--limit",
            "-l",
            type=float,
            help="Limit the lower percentage to consider while printing",
        )

        self.group_threshold.add_argument(
            "--percentile",
            "-p",
            type=float,
            help="Consider results according to given percentile in meta",
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
        elif self.args.percentile:
            dbc.set_percentile(self.args.percentile)

        if self.args.Pokemon == "name":
            dbc.print_pokemon_by_name()
        elif self.args.Pokemon == "win-rate":
            dbc.print_pokemon_by_win_rate()
        elif self.args.Pokemon == "pick-rate":
            dbc.print_pokemon_by_pick_rate()

        elif self.args.Build == "pkm-name":
            dbc.print_build_by_pokemon_name()
        elif self.args.Build == "pkm-win-rate":
            dbc.print_build_by_pokemon_win_rate()
        elif self.args.Build == "pkm-pick-rate":
            dbc.print_build_by_pokemon_pick_rate()
        elif self.args.Build == "win-rate":
            dbc.print_build_by_win_rate()
        elif self.args.Build == "pick-rate":
            dbc.print_build_by_pick_rate()

        elif self.args.Full_build == "pkm-name":
            dbc.print_full_build_by_pokemon_name()
        elif self.args.Full_build == "pkm-win-rate":
            dbc.print_full_build_by_pokemon_win_rate()
        elif self.args.Full_build == "pkm-pick-rate":
            dbc.print_full_build_by_pokemon_pick_rate()
        elif self.args.Full_build == "build-win-rate":
            dbc.print_full_build_by_build_win_rate()
        elif self.args.Full_build == "build-pick-rate":
            dbc.print_full_build_by_build_pick_rate()
        elif self.args.Full_build == "item":
            dbc.print_full_build_by_item()
        elif self.args.Full_build == "win-rate":
            dbc.print_full_build_by_win_rate()
        elif self.args.Full_build == "pick-rate":
            dbc.print_full_build_by_pick_rate()


if __name__ == "__main__":
    arg_parser = ArgParser()
    arg_parser.run()
