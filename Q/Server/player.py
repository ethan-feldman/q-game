import os, sys
import json
sys.path.insert(1, os.path.abspath('../Player'))
from player import Player
sys.path.insert(1, os.path.abspath('../Common'))
import encoder
import verifier
import decoder

# Represents a class for the proxy player. Acts as a middle man between the Referee and the Proxy Referee. This takes
# method requests from the referee and coverts it into JSON. It then sends it across the wire and sends back to the referee and 
# response it gets. 
class ProxyPlayer(Player):
    def __init__(self, connection) -> None:
        self.connection = connection
    
    def setup(self, publicState, tiles):
        json_request = json.dumps(["setup", [encoder.serialize_jpub(publicState), encoder.serialize_tile_bag(tiles)]])
        self.connection.sendall(json_request)
        self.verify_response(self.wait_for_response())
        return 


    # Returns the action of a move that the player would like to make
    def takeTurn(self, publicState):
        json_request = json.dumps([["take-turn"], encoder.serialize_jpub(publicState)])
        self.connection.sendall(json_request)
        response = self.wait_for_response()
        if self.verify_response(response):
            if self.is_void(response):
                raise RuntimeError()
            else:
                return decoder.deserialize_jaction(response)
        else:
            raise RuntimeError()
    
    # Sets the player's hand of tiles to the given set of tiles
    def newTiles(self, tiles):
        json_request = json.dumps(['new-tiles', [encoder.serialize_tile_bag(tiles)]])
        self.connection.sendall(json_request)
        self.verify_response(self.wait_for_response())

    # If the given boolean is true, this player has won.
    def win(self, w: bool):
        json_request = json.dumps(['win', [w]])
        self.connection.sendall(json_request)
        self.verify_response(self.wait_for_response())

    def _byte_list_to_string(bytes):
        return (b''.join(bytes)).decode()

    def _is_void(self, response):
        return response != "void"

    def verify_response(self, response):
        if self._is_void(response):
            if not verifier.verify_jaction(response):
                raise RuntimeError()

    def wait_for_response(self):
        total = []
        while True:
            bytes = self.connection.recv(1024)
            if len(bytes) == 0:
                break
            total.append(bytes)
        return self._byte_list_to_string(total)
