import asyncio
import referee
import sys, os
import json
import socket 
import referee
sys.path.insert(1, os.path.abspath('../Common'))
import decoder 
import time




'''
Represents the client in the server-client architecture. Creats the initial connection
and hands it off to the Proxy Referee who will call the player. 
'''
class Client():
    def __init__(self, config, player):
        self._config = config
        self._player = player
    
    # following this configuration creates a connection and links it to a proxy which runs through a game
    def run(self):
            connection = self.create_socket()
            self.send_name(connection)
            self.create_proxy(connection, self._player)


    # creates a socket with configuration information, will continue to retry connecting in the event
    # that the server has not been created yet. 
    def create_socket(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                client_socket.connect(self._config.host, self._config.port)
                break
            except ConnectionRefusedError:
                if not self._config.debug_mode:
                    print("unable to connect to server.")
                continue
                
        return client_socket

    # sends this player's name to the server.
    def send_name(self, client_socket):
        name = self._player.name()
        client_socket.sendall(name.encode())
    
    # creates a proxy referee which will respond to requests it receives
    # from across the TCP/IP connection.
    def create_proxy(self, connection, player):
        pr = referee.ProxyReferee(connection, player)
