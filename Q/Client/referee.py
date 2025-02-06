'''
Player <-> ProxyReferee <-> client   <-network-> server <-> ProxyPlayer <-> referee
'''
import sys, os, asyncio, io
import json
sys.path.insert(1, os.path.abspath('../../Common'))
import verifier, encoder

'''
Represents the class for the Proxy Referee. This acts as a middle-man to the proxy player and the 
actual player. This class is responsible for coverting JSON method requests to calls that the client 
player will understand.
'''
class ProxyReferee:
    def __init__(self, player, connection) -> None:
        self._connection = connection
        self._player = player
        self.handle_data_received()

    '''
    Handles all function call requests received by the referee. Converts it into a function call and 
    calls the relevant method of the player.
    '''
    def handle_data_received(self):
        game_end = False
        
        player_functions = {
            "setup" : self._player.setup,
            "take-turn" : self.take_turn,
            "new-tiles" : self._player.new_tiles,
            "win" : self._player.win
        }

        while not game_end:
            raw = self.reader.read().decode()
            if verifier.is_json(raw):
                function_call = json.loads(raw)
                fn_name = function_call[0]
                fn_data = function_call[1]

                if fn_name in player_functions:
                    player_functions[fn_name](*fn_data)
                else:
                    pass
                if fn_name == "setup" or fn_name == "new-tiles":
                    self._connection.sendall("void".encode())
                if  fn_name == "win":
                    self._connection.sendall("void".encode())
                    game_end = True

    def take_turn(self, publicState):
        result = self._player.take_turn(publicState)
        jresult = encoder.serialize_jaction(result)
        self._connection.sendall(jresult.encode())