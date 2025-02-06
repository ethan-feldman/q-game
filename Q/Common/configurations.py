# Contains the bonus for completing a 'Q' and the bonus for placing all tiles.
class ScoringConfiguration:
    def __init__(self, q_bonus, finish_bonus):
        self.q_bonus = q_bonus
        self.finish_bonus = finish_bonus 


# Contains the port number (unused), the host_name to connect to, the time wait before 
# connecting to the server, a quiet flag for debugging, and the remote player.
class ClientConfiguration():
    def __init__(self, port, host, wait, quiet, players) -> None:
        self.port_number = port 
        self.host_name = host 
        self.wait = wait
        self.quiet = quiet 
        self.players = players 

# Contains the initial state of the game, a quiet flag for debugging, config_s as the scoring configuration,
# the wait time for clients to respond in per turn, and a boolean to attach an observer.
class RefereeConfiguration():
       def __init__(self, state0, quiet, config_s, per_turn, observe) -> None:
           self.inital_state = state0 
           self.debug_mode = quiet 
           self.config_s = config_s
           self.per_turn = per_turn 
           self.use_observers = observe

# Contains the port number (unused), the number of times the server should wait for, the 
# amount of time the server waits for in each waiting period, a quiet flag for debugging, 
# and a referee configuration. 
class ServerConfiguration:
    def __init__(self, port, server_tries, server_wait, wait_for_signup, quiet, ref_config):
        self.port_number = port 
        self.rounds_waiting = server_tries
        self.signup_period_wait_time = server_wait 
        self.name_wait_time_seconds = wait_for_signup 
        self.debug_mode = quiet
        self.referee_config = ref_config