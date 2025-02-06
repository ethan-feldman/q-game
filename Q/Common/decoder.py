from map import Tile, Position, GameMap, GameMapBuilder, Shape, Color
from game_state import GameStateBuilder, PlayerInfoBuilder
from action import Action, Pass, Exchange, Place
import sys, os
import configurations 
sys.path.insert(1, os.path.abspath('../Q/Player'))
from player import PlayerBuilder, ExceptionPlayerBuilder, DosPlayerBuilder
from strategy import Strategy, Dag, Ldasg

def deserialize_jmap(jmap):
    builder = GameMapBuilder()
    for jrow in jmap:
        row = deserialize_jrow(jrow)
        for position, tile in row:
            builder.add_tile(position, tile)
    return builder.build()

def deserialize_jrow(jrow):
    row_index = jrow[0]
    row = []
    for jcell in jrow[1:]:
        row.append(deserialize_jcell(row_index, jcell))
    return row

def deserialize_jcell(row_index, jcell):
    col_index = jcell[0]
    tile = deserialize_jtile(jcell[1])
    return (Position(col_index, row_index), tile)

def deserialize_jtile(jtile):
    color = jtile['color']
    shape = jtile['shape']
    return Tile(Color(color), Shape(shape))

def deserialize_jpub(jpub):
    map = deserialize_jmap(jpub['map'])
    num_ref_tiles = jpub['tile*']
    player = deserialize_jplayer(jpub['players'][0])
    return map, num_ref_tiles, player

def deserialize_jplayer(jplayer):
    builder = PlayerInfoBuilder().set_score(jplayer['score'])
    for jtile in jplayer['tile*']:
       builder.add_tile(deserialize_jtile(jtile))
    return builder.build()

def deserialize_jplacements(jplacements):
    placements = []
    for one_placement in jplacements:
        placements.append(deserialize_one_placement(one_placement))
    return placements

def deserialize_one_placement(one_placement):
    position = deserialize_jcoordinate(one_placement["coordinate"])
    tile = deserialize_jtile(one_placement["1tile"])
    return (position, tile)

def deserialize_jcoordinate(jcoordinate):
    return Position(jcoordinate["column"], jcoordinate["row"])

def deserialize_jstrategy(jstrategy):
    if jstrategy == 'dag':
        return Dag()
    elif jstrategy == 'ldasg':
        return Ldasg()

def deserialize_jaction(jaction):
    if jaction == 'pass':
        return Pass()
    elif jaction == 'exchange':
        return Exchange()
    else:
        return Place([deserialize_one_placement(jaction)])

def deserialize_jstate(jstate): 
    builder = GameStateBuilder()
    builder.set_map(deserialize_jmap(jstate['map']))
    builder.set_referee_tiles(deserialize_referee_tile_bag(jstate['tile*']))
    builder.set_players(deserialize_jplayers(jstate['players']))
    return builder.build()

def deserialize_jplayers(jplayers):
    players = []
    for jplayer in jplayers:
        players.append(deserialize_jplayer(jplayer))
    return players 

def deserialize_referee_tile_bag(jtile_bag):
    tiles = []
    for jtile in jtile_bag:
        tiles.append(deserialize_jtile(jtile))
    return tiles 

def deserialize_jactors(jactors):
    actors = []
    for jactorspec in jactors:
        actors.append(deserialize_jactorspec(jactorspec))
    return actors

def deserialize_jactorspec(jactorspec):
    if(len(jactorspec) == 2):
        return PlayerBuilder().set_name(jactorspec[0]).set_strat(deserialize_jstrategy(jactorspec[1])).build()
    elif(len(jactorspec) == 3):
        return ExceptionPlayerBuilder().set_name(jactorspec[0]).set_strat(
            deserialize_jstrategy(jactorspec[1])).set_exn(jactorspec[2]).build()
    else:
        if jactorspec[2] == 'a cheat':
            return PlayerBuilder().set_name(jactorspec[0]).set_strat(deserialize_jstrategy(jactorspec[1])).set_cheat(jactorspec[3]).build()
        else:
            return DosPlayerBuilder().set_name(jactorspec[0]).set_strat(
                deserialize_jstrategy(jactorspec[1])).set_exn(jactorspec[2]).set_count(int(jactorspec[3])).build()

def deserialize_client_config(port, clientConfig):
    port = port
    unused = clientConfig["port"]
    host = clientConfig["host"]
    wait = clientConfig["wait"]
    quiet = clientConfig["quiet"]
    players = deserialize_jactors(clientConfig["players"])
    return configurations.ClientConfiguration(port, host, wait, quiet, players)

def deserialize_server_config(port, serverConfig):
    port = port
    unused = serverConfig["port"]
    server_tries = serverConfig["server-tries"]
    server_wait = serverConfig["server-wait"]
    wait_for_signup = serverConfig["wait-for-signup"]
    quiet = serverConfig["quiet"]
    ref_config = deserialize_referee_config(serverConfig["ref_spec"])
    #(port, rounds, signup_period_wait_time, name_wait_time, referee_config)
    return configurations.ServerConfiguration(port, server_tries, server_wait, wait_for_signup, quiet, ref_config)

def deserialize_referee_config(refereeConfig):
    state_0 = refereeConfig["state0"]
    quiet = refereeConfig["quiet"]
    config_rs = deserialize_referee_state_config(refereeConfig["config-s"])
    per_turn = refereeConfig["per-turn"]
    observe = refereeConfig["observe"]
    return configurations.RefereeConfiguration(state_0, quiet, config_rs[0], config_rs[1], per_turn, observe)

def deserialize_referee_state_config(refereeStateConfig):
    qbo = refereeStateConfig["qbo"]
    fbo = refereeStateConfig["fbo"]
    return (qbo, fbo)

'''
    builder = PlayerBuilder() 
    if len(jactorspec) == 3:
        builder = ExceptionPlayerBuilder() # need to build a player
        builder.set_exn(jactorspec[2])
    if len(jactorspec) == 4:
        if jactorspec[2] == 'a cheat':
            builder.set_cheat(jactorspec[3])
        else:
            builder = ExceptionPlayerBuilder() # need to build a player
            builder.set_exn(jactorspec[2]).set_count(jactorspec[3])
            builder.set_count(jactorspec[3])
            '''


def deserialize_function_call(function):
    pass