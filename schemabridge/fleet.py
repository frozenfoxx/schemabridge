""" A fleet """

import psycopg2
from psycopg2.extras import DictCursor

class Fleet(object):
    """ An automatic scripting unit """

    def __init__(self, conn_cur, fleet_id, player_id, name, script, script_declarations, last_script_update_tic, enabled, runtime):
        self.conn_cur = conn_cur
        self.fleet_id = fleet_id
        self.player_id = player_id
        self.name = name
        self.script = script
        self.script_delcarations = script_declarations
        self.last_script_update_tic = last_script_update_tic
        self.enabled = enabled
        self.runtime = runtime