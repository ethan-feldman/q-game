import sys, os
import json
import decoder
sys.path.insert(1, os.path.abspath('../Q/Referee'))
import referee 
import observer
from PySide6 import QtCore, QtWidgets, QtGui
import cProfile
import time
from threading import Thread
sys.path.insert(1, os.path.abspath('../Client'))
import client
import sys

# reads one JSON object from stdin. 
def read_stdin_json():
    raw_input = ""
    while True:
        raw_input += input()
        try:
            json_input = json.loads(raw_input)
            return json_input
        except:
            pass

# combines the calls of creating a client and running the client code. 
def create_and_run_client(config, player):
    current_client = client.Client(config, player)
    current_client.run()

# reads the client configuration from stdin, CHANGES the port number to be read from 
# the command line.
def create_configuration():
    client_config_json = read_stdin_json() 
    config = decoder.deserialize_client_config(client_config_json)
    config.port_number = int(sys.argv[1])
    return config

# constructs multiple clients each in their own thread before waiting for the threads to complete
def create_clients(config):
    threads = []
    for player in config.players: 
        thread = Thread(target=create_and_run_client, args=(config, player))
        threads.append(thread)
        thread.start()
        time.sleep(config.wait)
    for thread in threads:
        thread.join()
        
# reads in the configuration and starts the clients.
def main():
    config = create_configuration()
    create_clients(config)
    

if __name__ == '__main__':
    main()