from map import Tile, Position, GameMap, GameMapBuilder, Shape, Color
from game_state import GameStateBuilder, PlayerInfoBuilder
from action import Action, Pass, Exchange, Place
import sys, os
sys.path.insert(1, os.path.abspath('../Q/Player'))
from player import PlayerBuilder, ExceptionPlayerBuilder
from strategy import Strategy, Dag, Ldasg




''' SERIALIZATION METHODS '''

'''
def serialize_jmap(map: GameMap):
    jmap = []
    dict_placements = map._tiles # {Position:Tile}
    positions = dict_placements.keys()
    row_set = set()
    for position in positions:
        row_set = row_set.union(set([position._x])) # again row = x
    row_set = sorted(row_set)
    for row in row_set:
        jmap.append(serialize_jrow(row, dict_placements))
    return jmap

def serialize_jrow(row_index, placements):
    jrow = [row_index]

    for placement, value in placements.items():
        if placement._y == row_index:
            jrow.append(serialize_jcell(placement._x, value))
    
    return jrow
'''

def serialize_jmap(map: GameMap):
    jmap = []
    dict_placements = map._tiles # {Position:Tile}
    positions = dict_placements.keys()
    row_set = set()

    for position in positions:
        row_set = row_set.union({position._y}) # again row = x

    row_set = sorted(row_set)

    for row in row_set:
        jmap.append(serialize_jrow(row, dict_placements))
    
    return jmap

def serialize_jrow(row_index, placements):
    jrow = []

    for position, tile in placements.items():
        if position._y == row_index:
            jrow.append(serialize_jcell(position._x, tile))
    
    jrow.sort(key=lambda jcell : jcell[0])
    jrow.insert(0, row_index)
    return jrow

def serialize_jcell(col_index, tile):
    return [col_index, serialize_jtile(tile)]

def serialize_jtile(tile):
    return {"color": tile._color.value,"shape":tile._shape.value}

def serialize_jcoordinate(position):
    return {"row":position._y,"column":position._x}

def serialize_jpub(game_state):
    return {"map":serialize_jmap(game_state._map),"tile*":len(game_state._referee_tiles),
        "players":serialize_jplayers_public(game_state._players)}
        
def serialize_jplayers_public(players):
    jplayers = []
    jplayers.append(serialize_jplayer(players[0]))
    for playerinfo in players[1:]:
        jplayers.append(playerinfo._score)
    return jplayers
    
def serialize_jplayer(playerinfo):
    return {"score":playerinfo._score,"tile*":serialize_tile_bag(playerinfo._tile_bag)}

def serialize_jplacements(placements):
    jplacements = []
    for placement in placements:
        jplacements.append(serialize_one_placement(placement))
    
    return jplacements

def serialize_one_placement(placement):
    return {"coordinate": serialize_jcoordinate(placement[0]),
            "1tile": serialize_jtile(placement[1])}

def serialize_jstrategy(strategy):
    if (type(strategy) == Dag()):
        return "dag"
    elif (type(strategy) == Ldasg()):
        return "ldasg"

def serialize_jaction(action: Action):
    if action.actionString == 'pass':
        return "pass"
    elif action.actionString == 'exchange':
        return "exchange"
    else:
        placements = action.action()
        position, tile = placements[0]
        return {"1tile":{"color":tile._color.value,"shape":tile._shape.value},
                "coordinate":{"row":position._x,"column":position._y}}

    
def serialize_jstate(gamestate):
    return {"map":serialize_jmap(gamestate._map),"tile*":serialize_tile_bag(gamestate._referee_tiles),
            "players":serialize_jplayers(gamestate._players)}

def serialize_jplayers(players):
    jplayers = []
    for playerinfo in players:
        jplayers.append(serialize_jplayer(playerinfo))
    
    return jplayers

def serialize_tile_bag(tile_bag):
    tiles = []
    for tile in tile_bag:
        tiles.append(serialize_jtile(tile))
    return tiles

def serialize_jactors(players): # players is a list of players not a list of playerinfos
    jactors = []

    for player in players:
        jactors.append(serialize_jactorspec(player))

    return jactors

def serialize_jactorspec(player): # return to when exceptions are addressed
    return [player.name(),serialize_jstrategy(player._strategy)]







