import sqlite3


class HandleDatabase:
    def __init__(self):
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()
        self.table_name: str = None
        self.initialize()

    def initialize(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS table_list (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                number_of_games INTEGER,
                table_name TEXT UNIQUE
            )
            """
        )
        self.conn.commit()

    def get_table_names(self):
        self.cursor.execute("SELECT * FROM sqlite_master WHERE type='table'")
        return self.cursor.fetchall()

    def register_new_table(self, date, number_of_games, table_name):
        self.table_name = table_name
        try:
            self.cursor.execute(
                """
                INSERT INTO table_list (date, number_of_games, table_name)
                VALUES (?, ?, ?)
                """,
                (date, number_of_games, table_name),
            )
        except sqlite3.IntegrityError:
            # print(f"Table {table_name} already registered")
            return False
        print(f"New data found. Table {table_name} registered")
        self.conn.commit()
        return True

    def create_table(self, table_name):
        self.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pokemon TEXT,
                role TEXT,
                move1 TEXT,
                move2 TEXT,
                item TEXT,
                m1m2_win_rate REAL,
                m1m2_pick_rate REAL,
                m1m2i_win_rate REAL,
                m1m2i_pick_rate REAL,
                pkm_win_rate REAL,
                pkm_pick_rate REAL,
                win_rate REAL,
                pick_rate REAL
            )
            """
        )
        self.conn.commit()

    def close(self):
        self.conn.close()

    def insert_build(self, build):
        print(build)
        self.cursor.execute(
            f"""
            INSERT INTO {self.table_name} (pokemon, role, move1, move2, item, m1m2_win_rate, m1m2_pick_rate, m1m2i_win_rate, m1m2i_pick_rate, pkm_win_rate, pkm_pick_rate, win_rate, pick_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                build.pokemon.name,
                build.pokemon.role,
                build.move1,
                build.move2,
                build.item,
                build.m1m2_win_rate,
                build.m1m2_pick_rate,
                build.m1m2i_win_rate,
                build.m1m2i_pick_rate,
                build.pkm_win_rate,
                build.pkm_pick_rate,
                build.win_rate,
                build.pick_rate,
            ),
        )
        self.conn.commit()

    def get_all_builds(self, table_name=None):
        if table_name is not None:
            self.table_name = table_name
        self.cursor.execute(f"SELECT * FROM {self.table_name}")
        return self.cursor.fetchall()

    def get_builds_by_pokemon(self, pokemon):
        self.cursor.execute(
            f"SELECT * FROM {self.table_name} WHERE pokemon=?", (pokemon,)
        )
        return self.cursor.fetchall()

    def get_builds_by_role(self, role):
        self.cursor.execute(
            f"SELECT * FROM {self.table_name} WHERE role=?", (role,)
        )
        return self.cursor.fetchall()
