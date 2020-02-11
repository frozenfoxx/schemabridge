""" Classes involving planets """

import psycopg2
from psycopg2.extras import DictCursor

class Planet(object):
    """ A single planet """

    def __init__(self, conn_cur, planet_id, name, mine_limit, location_x, location_y, conqueror):

        self.conn_cur = conn_cur
        self.planet_id = planet_id
        self.name = name
        self.mine_limit = mine_limit
        self.location_x = location_x
        self.location_y = location_y
        self.conqueror = conqueror

    def update(self):
        """ Update values for a planet """

        query_string = "SELECT id, name, mine_limit, location_x, location_y, conqueror_id FROM planets WHERE id = " + str(self.planet_id) + ";"
        self.conn_cur.execute(query_string)
        results = self.conn_cur.fetchone()

        self.planet_id = results[0]
        self.name = results[1]
        self.mine_limit = results[2]
        self.location_x = results[3]
        self.location_y = results[4]
        self.conqueror = results[5]

        return results
