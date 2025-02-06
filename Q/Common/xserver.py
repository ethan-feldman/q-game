import sys, os
import json
import map
import encoder, decoder
sys.path.insert(1, os.path.abspath('../Q/Referee'))
import referee 
import observer
from PySide6 import QtCore, QtWidgets, QtGui
sys.path.insert(1, os.path.abspath('../Server'))
import server


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

# reads and deserializes the server configuration from stdin and changes the port number to be the one from the command line.
# Creates a server and runs it. 
def main():
    server_config_json = read_stdin_json() 
    config = decoder.deserialize_server_config(server_config_json)
    config.port_number = int(sys.argv[1])
    serv = server.Server(config)
    winners, cheaters = serv.run()
    sys.stdout.write(json.dumps([winners, cheaters]))



if __name__ == '__main__':
    main()