import sys, os
import json
from map import Tile, Position, Color, Shape
from game_state import PlayerInfo, State
from scoring import score_turn
import encoder, decoder 
import action




def read_stdin_json():
    raw_input = ""
    while True:
        raw_input += input()
        try:
            json_input = json.loads(raw_input)
            return json_input
        except:
            pass

def main():
    jmap = read_stdin_json()
    jplacements = read_stdin_json()

    map = decoder.deserialize_jmap(jmap)
    placements = decoder.deserialize_jplacements(jplacements)
    
    sys.stdout.write(json.dumps(score_turn(map, action.Place(placements), False)))

if __name__ == '__main__':
    main()
