import sys, os, time
import player
import socket
import select 
import datetime
import time
sys.path.insert(1, os.path.abspath('../../Spooky-mongooses/Q/Referee'))
import referee
sys.path.insert(1, os.path.abspath('../Common'))
import verifier 

WAIT_TIME = 20
MAX_DATA_BYTES = 1024
name_timeout = 3
MIN_NUM_PLAYERS = 2
MAX_NUM_PLAYERS = 4

MIN_PLAYERS = 2
MAX_PLAYERS = 4 



'''
Represents the server component in the client-server architecture. This class will listen for client connections and create
a proxy player for each one. Once a sufficient number of players have connected or the specified number of waiting periods has ended,
the server will return the result of the game.
'''
class Server:
    def __init__(self, config):
        self._config = config


    '''
    Composite function that runs tasks of:
    setting up the socket.
    running the signup rounds.
    running a game.
    returning the result
    '''
    def run(self):
        open_socket = self.setup_socket()
        proxy_players = self.run_signups(self._config.rounds, open_socket)
        winners, cheaters = self.run_game(proxy_players)
        return winners, cheaters


    '''
    Creates a socket server that clients can connect to from. Uses the configuration 
    port to bind the socket. 
    '''
    def setup_socket(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', self._config.port))
        server_socket.listen()
        return server_socket 

    # determines if the maximum number of players have been reached.
    def _maximum_players_reached(self, signups):
        return len(signups) >= MAX_PLAYERS

    # determines if the minimum nubmer of players have been reached.
    def _minimum_players_reached(self, signups):
        return len(signups) >= MIN_PLAYERS
    
    def _waiting_period_ended(self, start_time):
        return time.time() >= (start_time + self._config.signup_period_wait_time)


    '''
    runs a single sign up round
    '''
    def run_signup_round(self, server_socket, signups):
        start_time = time.time()
        self._config.signup_wait_time_seconds 
        while not self._waiting_period_ended(start_time) and self._maximum_players_reached(signups):
            conn, address = server_socket.accept()
            name = self.get_name_from_client(conn, start_time)
            if not verifier.validate_name(name):
                if self._config.debug_mode:
                    print("client sent at invalid name.")
                continue
            
            signups.append(player.ProxyPlayer(conn))
        return signups

    '''
    Retrieves the name from the player.
    '''
    def get_name_from_client(self, conn, start_time):
            max_time_remaining_to_get_name = max(self._config.name_wait_time, self._config.signup_period_wait_time - start_time)
            readable, _, _, = select.select(conn, [], [] , max_time_remaining_to_get_name) # max_remaining_wait_time
            return readable[0]

    '''
    Runs all signup rounds.
    '''
    def run_signups(self, rounds, server_socket):
        signups = []
        for i in range(0, rounds):
            self.run_signup_round(server_socket, signups)
            if self._minimum_players_reached(signups):
                break
        return signups

    '''
    Runs the game with the referee.
    '''
    def run_game(self, proxy_players):
        if len(proxy_players) == 1:
            return ([],[])
        ref = referee.Referee(proxy_players, self._config.referee_config)
        return ref.run_game_and_return_winners()
        