""" Player objects """

import psycopg2
from psycopg2.extras import DictCursor

class Player(object):
    """ A player in the game """

    def __init__(self, conn_cur, player_id):
        self.conn_cur = conn_cur
        self.player_id = player_id
        query_string = "select * from online_players where id = " + str(self.player_id) + ";"
        self.conn_cur.execute(query_string)
        results = self.conn_cur.fetchone()

        if results is not None:
            self.username = results[1]
        else:
            self.username = ""

        self.damage_taken = 0
        self.damage_done = 0
        self.planets_conquered = 0
        self.planets_lost = 0
        self.ships_built = 0
        self.ships_lost = 0
        self.ship_upgrades = 0
        self.distance_travelled = 0
        self.fuel_mined = 0

    def update(self):
        """ Update the player information """

        # Update from current_player_stats
        query_string = "SELECT * FROM current_player_stats WHERE player_id = " + \
            str(self.player_id) + ";"
        self.conn_cur.execute(query_string)
        results = self.conn_cur.fetchone()

        if results is not None:
            self.username = results[1]
            self.damage_taken = results[2]
            self.damage_done = results[3]
            self.planets_conquered = results[4]
            self.planets_lost = results[5]
            self.ships_built = results[6]
            self.ships_lost = results[7]
            self.ship_upgrades = results[8]
            self.distance_travelled = results[9]
            self.fuel_mined = results[10]

class MyPlayer(Player, object):
    """ The invoking player """

    def __init__(self, conn_cur):
        self.conn_cur = conn_cur
        self.conn_cur.execute("SELECT * FROM my_player;")
        results = self.conn_cur.fetchone()

        self.player_id = results[0]
        self.username = results[1]
        self.created = results[2]
        self.balance = results[3]
        self.fuel_reserve = results[4]
        self.password = results[5]
        self.error_channel = results[6]
        self.starting_fleet = results[7]
        self.symbol = results[8]
        self.rgb = results[9]

        super(MyPlayer, self).__init__(self.conn_cur, self.player_id)

    def update(self):
        """ Update the player information """

        self.conn_cur.execute("SELECT * FROM my_player;")
        results = self.conn_cur.fetchone()

        self.created = results[2]
        self.balance = results[3]
        self.fuel_reserve = results[4]
        self.password = results[5]
        self.error_channel = results[6]
        self.starting_fleet = results[7]
        self.symbol = results[8]
        self.rgb = results[9]

        super(MyPlayer, self).update()
