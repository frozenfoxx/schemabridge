""" The collection of ships for the player """

import psycopg2
from psycopg2.extras import DictCursor
from .ship import Ship

class Armada(object):
    """ All ships under a player's control """

    def __init__(self, conn_cur):
        """ Initialize the armada """

        self.conn_cur = conn_cur
        self.ships = []

    def attack(self, ship_id, target_id):
        """ Set a ship in our armada to attack a target ship """

        # Perfom attack
        attack_string = "SELECT ATTACK(" + str(ship_id) + "," + str(target_id) + ");"
        self.conn_cur.execute(attack_string)
        print("[>] Attack ordered")

    def attack_all(self):
        """ Order the armada to attack all ships in range """

        # Query databse
        query_string = "SELECT * from ships_in_range;"
        self.conn_cur.execute(query_string)
        results = self.conn_cur.fetchall()

        # Check ships in range
        for ship in results:
            self.attack(str(ship[0]), str(ship[1]))

    def create(self, name, stats, location):
        """ Create a ship """

        # Set insert_string based on location
        if location:
            insert_string = "INSERT INTO my_ships (name, attack, defense, engineering, prospecting, location) VALUES ('" + \
                            str(name) + "'," + \
                            str(stats[0]) + "," + \
                            str(stats[1]) + "," + \
                            str(stats[2]) + "," + \
                            str(stats[3]) + "," + \
                            "POINT(" + str(location) + "));"
        else:
            insert_string = "INSERT INTO my_ships (name, attack, defense, engineering, prospecting) VALUES ('" + \
                            str(name) + "'," + \
                            str(stats[0]) + "," + \
                            str(stats[1]) + "," + \
                            str(stats[2]) + "," + \
                            str(stats[3]) + ");"

        # Perfom insert
        self.conn_cur.execute(insert_string)
        print("[>] Ship created")

    def mine(self, ship_id, target_id):
        """ Set a ship in our armada to mine a planet """

        # Perfom mining
        mine_string = "SELECT MINE(" + str(ship_id) + "," + str(target_id) + ");"
        self.conn_cur.execute(mine_string)
        print("[>] Mining ordered")

    def mine_all(self):
        """ Order the armada to mine all planets in range """

        # Query databse
        query_string = "SELECT * from planets_in_range;"
        self.conn_cur.execute(query_string)
        results = self.conn_cur.fetchall()

        # Check planets in range
        for ship in results:
            self.mine(str(ship[0]), str(ship[1]))

    def move(self, ship_id, speed, location_x, location_y):
        """ Instructs a ship to move to coordinates at a given speed """

        if speed == 'max':
            speed_value = 'max_speed'
        elif speed == 'half':
            speed_value = 'current_fuel / 2'
        else:
            print("[-] Speed value incorrect!")
            return

        # Set speed and direction for named ships
        query_string = "SELECT SHIP_COURSE_CONTROL(id," + \
            str(speed_value) + "," + \
            "null" + "," + \
            "POINT(" + \
            str(location_x) + "," + \
            str(location_y) + ")) " + \
            "FROM my_ships WHERE " + \
            "id='" + str(ship_id) + "';"

        # Perform move
        self.conn_cur.execute(query_string)
        print("[>] Ship movement ordered")

    def planets_in_range(self):
        """ Updates the list of ships in range """

        query_string = "SELECT * from planets_in_range;"

        # Perform query
        self.conn_cur.execute(query_string)
        results = self.conn_cur.fetchall()

        # Build dictionary
        ranges = {}
        for row in results:
            ranges[row[0]] = row[1]

        return ranges

    def repair(self, ship_id, target_id):
        """ Set a ship in our armada to repair another ship """

        # Perfom repair
        repair_string = "SELECT REPAIR(" + str(ship_id) + "," + str(target_id) + ");"
        self.conn_cur.execute(repair_string)
        print("[>] Repair ordered")

    def ships_in_range(self):
        """ Updates the list of ships in range """

        query_string = "SELECT * from ships_in_range;"

        # Perform query
        self.conn_cur.execute(query_string)
        results = self.conn_cur.fetchall()

        # Build dictionary
        ranges = {}
        for row in results:
            ranges[row[0]] = row[1]

        return ranges

    def update(self):
        """ Update the armada """

        self.conn_cur.execute("SELECT * FROM my_ships;")
        results = self.conn_cur.fetchall()

        # Refresh the armada
        self.ships = []
        for row in results:
            attrs = []
            for column in row:
                attrs.append(column)
            self.ships.append(Ship(self.conn_cur, attrs))
