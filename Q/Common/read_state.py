import sys, os
import json
from Map import Tile, Position, Color, Shape
from map_builder import MapBuilder
from game_state import PlayerInfo, State

def parse_jmap(jmap, map_builder):
    for row in jmap:
        row_index = row[0] 
        for j_cell in row[1:]:
            col_index = j_cell[0]
            jtile = j_cell[1]
            map_builder.add_tile(Position(row_index , col_index), Tile(jtile['color'], jtile['shape']))
    return map_builder

def parse_jplayer(jplayer, playerinfo_builder):
    player_score = jplayer['score'] 
    for jtile in jplayer['tile*']:
       playerinfo_builder.add_tile(Tile(jtile['color'], jtile['shape']))
    return playerinfo_builder
        

    
class PlayerInfoBuilder:
    def __init__(self):
        self.tiles = []

    def build(self):
        return PlayerInfo(id=0, age=0, score=0, tile_bag=self.tiles)

    def add_tile(self, tile):
        self.tiles.append(tile)


# Converts the dictionary of placments {"coordinate" : JCoordinate, "1tile": tile}
# to a list of tuples (Position, tile)
def parse_jplacements(jplacements):
    placements = []

    for jplacement in jplacements:
        jcoor = jplacement["coordinate"]
        jtile = jplacement["1tile"]
        position = Position(jcoor["row"], jcoor["column"])
        tile = Tile(jtile["color"], jtile["shape"])
        placements.append((position, tile))
        
    return placements

def parse_jpub(jpub):
    map = parse_jmap(jpub['map'], MapBuilder())
    player = parse_jplayer(jpub['players'][0], PlayerInfoBuilder())
    return map, player

def construct_jmap(map):
    cells_dict = map._tiles # dictionary of {Position: tile} 
    rowIndexes = set()

    for posn_key in cells_dict:
        rowIndexes.add(posn_key._x)
    rowIndexesList = []
    for index in rowIndexes:
        rowIndexesList.append(index)
    rowIndexesList.sort()

    jmap = [] # all rows.
    for row in rowIndexesList:
        jmap.append([])
    indexDelta = rowIndexesList[0] #  used for aligning jmap index with row index prior to inserting row index (done to allow cell sorting)

    for posn_key in cells_dict:
        row = posn_key._x
        column = posn_key._y
        jtile = {"color": cells_dict[posn_key]._color, "shape": cells_dict[posn_key]._shape}
        jmap[row - indexDelta].append([column, jtile])

    for row in jmap:
        row.sort(key=lambda jcell: jcell[0])
    for i in range(0, len(jmap)):
        jmap[i].insert(0, rowIndexesList[i])
        
    return jmap


    
def main():
    # python3 read_input_4.py $(<Tests/0-in.json)    

    if len(sys.argv) != 3:
        sys.exit()

    jpub = json.loads(sys.argv[1])
    jplacements = json.loads(sys.argv[2])

    map, player = parse_jpub(jpub)
    placements = parse_jplacements(jplacements)

    map = map.build()
    player = player.build()

    state = State([player], map, [])
    if state.player_owns_tiles(placements) and state.check_proposed_placements(placements):
        state.place_turn(placements)
        jmap = construct_jmap(state._map)
        sys.stdout.write(json.dumps(jmap))
    else:
        sys.stdout.write(json.dumps(False))


if __name__ == '__main__':
    main()
