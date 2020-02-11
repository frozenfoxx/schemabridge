""" A ship """

import psycopg2
from psycopg2.extras import DictCursor

class Ship(object):
    """ A single ship """

    def __init__(self, conn_cur, attrs):

        self.conn_cur = conn_cur
        self.ship_id = attrs[0]
        self.fleet_id = attrs[1]
        self.player_id = attrs[2]
        self.name = attrs[3]
        self.last_action_tic = attrs[4]
        self.last_move_tic = attrs[5]
        self.last_living_tic = attrs[6]
        self.current_health = attrs[7]
        self.max_health = attrs[8]
        self.current_fuel = attrs[9]
        self.max_fuel = attrs[10]
        self.max_speed = attrs[11]
        self.range = attrs[12]
        self.attack = attrs[13]
        self.defense = attrs[14]
        self.engineering = attrs[15]
        self.prospecting = attrs[16]
        self.location_x = attrs[17]
        self.location_y = attrs[18]
        self.direction = attrs[19]
        self.speed = attrs[20]
        self.destination_x = attrs[21]
        self.destination_y = attrs[22]
        self.repair_priority = attrs[23]
        self.action = attrs[24]
        self.action_target_id = attrs[25]
        self.location = attrs[26]
        self.destination = attrs[27]
        self.target_speed = attrs[28]
        self.target_direction = attrs[29]

    def update(self):
        """ Update attrs for a ship """

        query_string = "SELECT * FROM my_ships WHERE id = " + str(self.ship_id) + ";"
        self.conn_cur.execute(query_string)
        results = self.conn_cur.fetchone()

        self.fleet_id = results[1]
        self.player_id = results[2]
        self.name = results[3]
        self.last_action_tic = results[4]
        self.last_move_tic = results[5]
        self.last_living_tic = results[6]
        self.current_health = results[7]
        self.max_health = results[8]
        self.current_fuel = results[9]
        self.max_fuel = results[10]
        self.max_speed = results[11]
        self.range = results[12]
        self.attack = results[13]
        self.defense = results[14]
        self.engineering = results[15]
        self.prospecting = results[16]
        self.location_x = results[17]
        self.location_y = results[18]
        self.direction = results[19]
        self.speed = results[20]
        self.destination_x = results[21]
        self.destination_y = results[22]
        self.repair_priority = results[23]
        self.action = results[24]
        self.action_target_id = results[25]
        self.location = results[26]
        self.destination = results[27]
        self.target_speed = results[28]
        self.target_direction = results[29]

    def upgrade(self, attr_code, quantity):
        """ Upgrade an aspect of the ship """

        valid_codes = [
            'MAX_HEALTH',
            'MAX_FUEL',
            'MAX_SPEED',
            'RANGE',
            'ATTACK',
            'DEFENSE',
            'ENGINEERING',
            'PROSPECTING'
            ]

        if attr_code in valid_codes:
            upgrade_string = "SELECT UPGRADE(" + \
                str(self.ship_id) + ",'" + \
                str(attr_code) + "'," + \
                str(quantity) + ");"

        self.conn_cur.execute(upgrade_string)
        results = self.conn_cur.fetchone()

        return results[0]
