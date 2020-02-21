""" Objects and functions related to the state of the game """

if __package__:
    from .planet import Planet
    from .player import Player
else:
    from planet import Planet
    from player import Player
import psycopg2
from psycopg2.extras import DictCursor

class Game(object):
    """ Game state """

    def __init__(self, conn_cur):
        self.tic = 0
        self.conn_cur = conn_cur
        self.planets = []
        self.players = []
        self.variables = {}

        self.update_players()
        self.update_planets()
        self.update_variables()

    def count_planets(self):
        """ Count number of rows in the planets table """

        # Get planets
        query_string = "SELECT COUNT(*) FROM planets;"
        self.conn_cur.execute(query_string)
        results = self.conn_cur.fetchone()

        return results[0]

    def count_players(self):
        """ Count number of players in the online_players table """

        # Get planets
        query_string = "SELECT COUNT(*) FROM online_players;"
        self.conn_cur.execute(query_string)
        results = self.conn_cur.fetchone()

        return results[0]

    def update_planets(self):
        """ Update planets """

        # Reset planets
        self.planets = []

        # Get planets
        query_string = "SELECT * FROM planets;"
        self.conn_cur.execute(query_string)
        results = self.conn_cur.fetchall()

        for i in results:
            self.planets.append(Planet(self.conn_cur, i[0], i[1], i[2], i[3], i[4], i[5]))

    def update_players(self):
        """ Update players """

        # Reset players
        self.players = []

        # Get players
        query_string = "SELECT * FROM online_players;"
        self.conn_cur.execute(query_string)
        results = self.conn_cur.fetchall()

        for i in results:
            self.players.append(Player(self.conn_cur, i[0]))

    def update_tic(self):
        """ Update the Tic """

        # Get latest tic
        query_string = "SELECT last_value FROM tic_seq;"
        self.conn_cur.execute(query_string)
        results = self.conn_cur.fetchone()
        self.tic = results[0]

        return self.tic

    def update_variables(self):
        """ Update list of public_variables """

        query_string = "SELECT * FROM public_variable;"
        self.conn_cur.execute(query_string)
        results = self.conn_cur.fetchall()

        for line in results:
            self.variables[str(line[0])] = int(line[2])
