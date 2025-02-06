import sys, os
import json
from Map import Tile, Position, Color, Shape
from map_builder import MapBuilder

def parse_jmap(jmap, map_builder):
    '''
        This function recursively processes the input JSON and returns a string representation of the JSON structure.

        Args:
            injson: The json object to be read.
        Returns:
            ", ".join(results): All json joined together.
    '''
    for row in jmap:
        row_index = row[0] 
        for j_cell in row[1:]:
            col_index = j_cell[0]
            jtile = j_cell[1]
            map_builder.add_tile(Position(row_index , col_index), Tile(jtile['color'], jtile['shape']))
    return map_builder

def get_positions(positions):
    positions = list(positions)
    positions.sort(key=lambda pos: (pos._x, pos._y))
    ret_list = []
    for position in positions:
        ret_list.append({'column' : position._y, 'row' : position._x})
    return ret_list
        

def main():
    if len(sys.argv) != 3:
        sys.exit()
    jmap = sys.argv[1]
    jtile = json.loads(sys.argv[2])
    tile = Tile(jtile['color'], jtile['shape'])
    map_builder = parse_jmap(json.loads(jmap), MapBuilder())
    map = map_builder.build()
    positions = map.get_possible_insertions(tile)
    sys.stdout.write(json.dumps(get_positions(positions)))
    

if __name__ == '__main__':
    main()