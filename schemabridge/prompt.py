""" Interactive Prompt """

if __package__:
    from .armada import Armada
    from .game import Game
    from .player import MyPlayer
else:
    from armada import Armada
    from game import Game
    from player import MyPlayer
import sys
from cmd import Cmd
import psycopg2
from psycopg2.extras import DictCursor

class Prompt(Cmd, object):
    """ Handle user input """

    def __init__(self, conn_string):
        super(Prompt, self).__init__()

        # Build database connection
        self.conn = psycopg2.connect(conn_string)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) #create database cursor. parameter grabs result as dict (which is not default)
        self.conn.autocommit = True #disable transactions (transactions left uncommitted will hang the game)

        self.myplayer = MyPlayer(self.cur)
        self.game = Game(self.cur)
        self.armada = Armada(self.cur)

    def do_run(self, args):
        """ Run the automated bot with or without a data seed """

        print("[+] Run not yet implemented")

    def do_attack_all(self, args):
        """ Order all ships in range of enemy ships to attack """

        # Order the attack
        self.armada.attack_all()
        print("[+] All ships in attack range ordered to attack")

    def do_mine_all(self, args):
        """ Order all ships in range of planets to mine """

        # Order the mine
        self.armada.mine_all()
        print("[+] All ships in mining range ordered to mine")

    def do_mystatus(self, args):
        """ Status of the player """

        self.myplayer.update()

        print("[+] User      | Balance | Fuel Reserve")
        print("[+] ----------------------------------")
        print("[+] " + str(self.myplayer.username) + " | " + \
            str(self.myplayer.balance) + " | " + \
            str(self.myplayer.fuel_reserve))

    def do_planets(self, args):
        """ Show the list of planets """

        # Check if table scan is necessary
        if self.game.count_planets() != len(self.game.planets):
            print("[+] Planet count off, initiating table scan")
            self.game.update_planets()
            print("[+] Done")

        print("[+] ID    | Name   | Mine Limit | Loc X | Loc Y | Conqueror")
        print("[+] -------------------------------------------------------")
        for i in self.game.planets:
            print("[+] " + str(i.planet_id) + " | " + \
                str(i.name) + " | " + \
                str(i.mine_limit) + " | " + \
                str(i.location_x) + " | " + \
                str(i.location_y) + " | " + \
                str(i.conqueror))

    def do_planets_in_range(self, args):
        """ Dump table of planets in range """

        planets = self.armada.planets_in_range()

        print("[+] Ship ID | Planet(s)")
        print("[+] -------------------")
        for p in planets:
            print("[+] " + str(p) + " | " + str(planets[p]))

    def do_planets_update(self, args):
        """ For an update for the planets """

        self.game.update_planets()
        print("[+] Planets updated")

    def do_players(self, args):
        """ Show all players """

        self.game.update_players()

        print("[+] ID | Username   | Damage Taken | Damage Done | Planets Conq | Planets Lost | Ships Built | Ships Lost | Ship Upgrades | Distance | Fuel Mined")
        print("[+] ---------------------------------------------------------------------------------------------------------------------------------------------")
        for i in self.game.players:
            print("[+] " + str(i.player_id) + " | " + \
                str(i.username) + " | " + \
                str(i.damage_taken) + " | " + \
                str(i.damage_done) + " | " + \
                str(i.planets_conquered) + " | " + \
                str(i.planets_lost) + " | " + \
                str(i.ships_built) + " | " + \
                str(i.ships_lost) + " | " + \
                str(i.ship_upgrades) + " | " + \
                str(i.distance_travelled) + " | " + \
                str(i.fuel_mined))

    def do_ship_attack(self, args):
        """ Attack a target ship with your own ships
            ship_attack [ship id] [target id] """

        # Check argument list
        if len(args) == 0:
            print("[-] Error: argument list cannot be empty")
        elif len(args.split()) != 2:
            print("[-] Error: argument list incorrect")
        else:
            arglist = args.split()
            self.armada.attack(arglist[0], arglist[1])
            print("[+] Ships with identifier " + str(arglist[0]) + " set to attack " + str(arglist[1]))

    def do_ship_create(self, args):
        """ Create a ship
            ship_create [name]
            ship_create [name] [attack] [defense] [engineering] [prospecting] [location] """

        if len(args) == 0:
            print("[-] Error: argument list cannot be empty")
        elif len(args) > 6:
            print("[-] Error: argument list too long")

        else:
            # Set ship name
            name = args.split(' ')[0]

            # Set ship attrs and location if offered
            stats = []
            if len(args.split(' ')) > 1:
                stats.append(args.split(' ')[1])
                stats.append(args.split(' ')[2])
                stats.append(args.split(' ')[3])
                stats.append(args.split(' ')[4])
                location = args.split(' ')[5]
                self.armada.create(name, stats, location)
            else:
                stats.append(5)
                stats.append(5)
                stats.append(5)
                stats.append(5)
                location = ""
                self.armada.create(name, stats, location)

    def do_ship_mine(self, args):
        """ Order a ship in range of a planet to mine
            ship_mine [ship id] [planet id] """

        # Check argument list
        if len(args) == 0:
            print("[-] Error: argument list cannot be empty")
        elif len(args.split()) != 2:
            print("[-] Error: argument list incorrect")
        else:
            arglist = args.split()
            self.armada.mine(arglist[0], arglist[1])
            print("[+] Ship with id " + str(arglist[0]) + " ordered to mine planet id " + str(arglist[1]))

    def do_ship_move(self, args):
        """ Move a ship at a speed towards a point
            ship_move [ship id] [max|half] [location_x] [location_y] """

        # Check argument list
        if len(args) == 0:
            print("[-] Error: argument list cannot be empty")
        elif len(args.split()) != 4:
            print("[-] Error: argument list incorrect")
        else:
            arglist = args.split()
            self.armada.move(arglist[0], arglist[1], arglist[2], arglist[3])
            print("[+] Ship with id " + str(arglist[0]) + " moved to POINT(" + str(arglist[2]) + "," + str(arglist[3]) + ")")

    def do_ship_repair(self, args):
        """ Order a ship in range of a target ship to repair
            ship_repair [source ship id] [target ship id] """

        # Check argument list
        if len(args) == 0:
            print("[-] Error: argument list cannot be empty")
        elif len(args.split()) != 2:
            print("[-] Error: argument list incorrect")
        else:
            arglist = args.split()
            self.armada.repair(arglist[0], arglist[1])
            print("[+] Ship with id " + str(arglist[0]) + " ordered to repair id " + str(arglist[1]))

    def do_ship_upgrade(self, args):
        """ Upgrade an attribute of a ship
            ship_upgrade [id] [attribute] [quantity]
            Attributes:
            MAX_HEALTH  MAX_FUEL  MAX_SPEED  RANGE
            ATTACK  DEFENSE  ENGINEERING PROSPECTING"""

        # Check argument list
        if len(args) == 0:
            print("[-] Error: argument list cannot be empty")
        elif len(args.split()) != 3:
            print("[-] Error: argument list incorrect")
        else:
            arglist = args.split()
            for ship in self.armada.ships:
                if ship.ship_id == int(arglist[0]):
                    ship.upgrade(arglist[1], arglist[2])
                    print("[+] Ship with id " + str(arglist[0]) + " upgraded")

    def do_ships(self, args):
        """ Show ships """

        self.armada.update()

        print("[+] id | fleet_id | player_id | name | last_action_tic | last_move_tic | last_living_tic | current_health | max_health | current_fuel | max_fuel | max_speed | range | attack | defense | engineering | prospecting | location_x | location_y | direction | speed | destination_x | destination_y | repair_priority | action | action_target_id |      location      | destination | target_speed | target_direction")
        print("[+] -------------------")
        for ship in self.armada.ships:
            print("[+] " + str(ship.ship_id) + " | " + \
                str(ship.fleet_id) + " | " + \
                str(ship.player_id) + " | " + \
                str(ship.name) + " | " + \
                str(ship.last_action_tic) + " | " + \
                str(ship.last_move_tic) + " | " + \
                str(ship.last_living_tic) + " | " + \
                str(ship.current_health) + " | " + \
                str(ship.max_health) + " | " + \
                str(ship.current_fuel) + " | " + \
                str(ship.max_fuel) + " | " + \
                str(ship.max_speed) + " | " + \
                str(ship.range) + " | " + \
                str(ship.attack) + " | " + \
                str(ship.defense) + " | " + \
                str(ship.engineering) + " | " + \
                str(ship.prospecting) + " | " + \
                str(ship.location_x) + " | " + \
                str(ship.location_y) + " | " + \
                str(ship.direction) + " | " + \
                str(ship.speed) + " | " + \
                str(ship.destination_x) + " | " + \
                str(ship.destination_y) + " | " + \
                str(ship.repair_priority) + " | " + \
                str(ship.action) + " | " + \
                str(ship.action_target_id) + " | " + \
                str(ship.location) + " | " + \
                str(ship.destination) + " | " + \
                str(ship.target_speed) + " | " + \
                str(ship.target_direction))

    def do_ships_in_range(self, args):
        """ Dump table of ships in range """

        ships = self.armada.ships_in_range()

        print("[+] Ship ID | Target Ship ID(s)")
        print("[+] ---------------------------")
        for s in ships:
            print("[+] " + str(s) + " | " + str(ships[s]))

    def do_tic(self, args):
        """ Get current server Tic """

        self.game.update_tic()
        print("[+] Current Tic: " + str(self.game.tic))

    def do_train(self, args):
        """ Train the automated player """

        print("[+] Training not yet implemented")

    def do_variables(self, args):
        """ Update and dump variables """

        self.game.update_variables()
        print("[+] Name | Value")
        print("[+] ------------")
        for key, value in self.game.variables.items():
            print("[+] " + str(key) + "|" + str(value))

    def do_quit(self, args):
        """ Quit the program """

        print("[+] Shutting down")

        # Close down database connection
        self.conn.commit()
        self.cur.close()
        self.conn.close()

        raise SystemExit
