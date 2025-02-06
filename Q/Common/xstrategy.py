import sys, os
import json
from map import Tile, Position, Color, Shape
from game_state import PlayerInfo
import decoder, encoder 
sys.path.insert(0, os.path.abspath('../Player'))
from strategy import Dag, Ldasg
from action import Action


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

    jstrategy = read_stdin_json()
    jpub = read_stdin_json()

    strategy = decoder.deserialize_jstrategy(jstrategy)
    map, num_ref_tiles, player = decoder.deserialize_jpub(jpub)

    if strategy == "dag":
        action = Dag().get_action(map, player.get_tile_bag, len(player.get_tile_bag), num_ref_tiles)
    else:
        action = Ldasg().get_action(map, player.get_tile_bag, len(player.get_tile_bag), num_ref_tiles)
    
    output = json.dumps(encoder.serialize_jaction(action))
    sys.stdout.write(output)

if __name__ == '__main__':
    main()