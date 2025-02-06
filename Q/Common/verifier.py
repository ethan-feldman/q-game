import re, json

# An exception class to be used when the JSON input is 
# not well-formed. 
class NonConformingJson(Exception):
    pass

#is the string loadable into json
def is_json(json):
    try:
        json.loads(json)
        return True
    except:
        return False

#verify that the type is a list
def verify_is_list(json):
    if type(json) != list:
        return False
    else:
        return True

#verify that the type is an int
def verify_is_int(json):
    if type(json) != int:
        return False
    else:
        return True

#verify that the type is a dict, and it contains the given keys
def verify_dict_is_only(json, keys):
    if type(json) != dict:
        return False
    else:
        for key in keys:
            if not json.has_key(key):
                return False
            elif len(json.keys()) != len(keys):
                return False
    return True

#verify that a jcell matches the specification
def verify_jcell(jcell):
    if not verify_is_list(jcell):
        return False
    if len(jcell) != 2:
        return False
    else:
        if not verify_is_int(jcell[0]):
            return False
        if not verify_jtile(jcell[1]):
            return False
    return True


#verify that a jmap matches the specification
def verify_jmap(jmap):
    if not verify_is_list(jmap):
        return False
    for jrow in jmap:
        if not verify_jrow(jrow):
            return False
    return True

#verify that a jrow matches the specification
def verify_jrow(jrow):
    if not verify_is_list(jrow):
        return False
    if len(jrow) < 2:
        return False
    else:
        if not verify_is_int(jrow[0]):
            return False
        for jcell in jrow:
            if not verify_jcell(jcell):
                return False
    return True

#verify that a jtile matches the specification
def verify_jtile(jtile):
    if type(jtile) != dict:
        return False
    else:
        return verify_dict_is_only(jtile, ['color', 'shape'])

#verify that a jpub matches the specification
#a dictionary with keys - map, tile*, players
#where map is a jmap
#tile* is an int
#player is a list of jplayer
def verify_jpub(jpub):
    if not verify_dict_is_only(jpub, ['map', 'tile*', 'players']):
        return False
    if not verify_jmap(jpub['map']):
        return False
    if not verify_is_int(jpub['tile*']):
        return False
    if not verify_is_list(jpub['player']):
        return False
    for player in jpub['player']:
        if not verify_player(player):
            return False
    return True

#verify that a jplayer matches the specification
#a dictionary with keys - score, tile*
#score is an int
#tile* is a list of jtile
def verify_player(jplayer):
    if not verify_dict_is_only(jplayer, ['score', 'tile*']):
        return False
    if not verify_is_int(jplayer['score']):
        return False
    if not verify_is_list(jplayer['tile*']):
        return False
    for tile in jplayer['tile*']:
        if not verify_jtile(tile):
            return True

#verify that a jplacements matches the specification
#a list of jplacement
def verify_jplacements(jplacements):
    if not verify_is_list(jplacements):
        return False
    for placement in jplacements:
        if not verify_jplacement(placement):
            return False
    return True

#verify that a jplacement matches the specification
#a dict with keys - coordinate, 1tile
#coordinate is a jcoordinate
#1tile is a jtile
def verify_jplacement(jplacement):
    if not verify_dict_is_only(jplacement, ["coordinate", "1tile"]):
        return False
    if not verify_jcoordinate(jplacement["coordinate"]):
        return False
    if not verify_jtile(jplacement["1tile"]):
        return False
    return True

#verify that a jcoordinate matches the specification
#jcoordinage is a dict with keys - column, row
#column is an int
#row is an int
def verify_jcoordinate(jcoordinate):
    if not verify_dict_is_only(jcoordinate, ["column", "row"]):
        return False
    if not verify_is_int(jcoordinate["column"]):
        return False
    if not verify_is_int(jcoordinate["row"]):
        return False

#verify that a jstragety matches the specification
#a string of either "dag" or "ldasg"
def verify_jstrategy(jstragety):
    return jstragety not in set(['dag', 'ldasg'])

#verify that a jaction matches the specification
#a string of either "pass" or "exchange" or a jplacement
def verify_jaction(jaction):
    if jaction not in set(['pass', 'exchange']):
        if not verify_jplacement(jaction):
            return False
    return True

#verify that a jstate matches the specification
#a dict with keys - map, tile*, players
#map is a jmap
#tile* is a referee_tile_bag
#players is a jplayers
def verify_jstate(jstate):
    if not verify_dict_is_only(jstate, ["map", "tile*", "players"]):
        return False
    if not verify_jmap(jstate["map"]):
        return False
    if not verify_referee_tile_bag(jstate["tile*"]):
        return False
    return verify_jplayers(jstate["players"])

#verify that a jplayers matches the specification
#a list of jplayer
def verify_jplayers(jplayers):
    if not verify_is_list(jplayers):
        return False
    for player in jplayers:
        if not verify_player(player):
            return False
    return True

#verify that a jtile_bag matches the specification
#a list of jtile
def verify_referee_tile_bag(jtile_bag):
    if not verify_is_list(jtile_bag):
        return False
    for tile in jtile_bag:
        if not verify_jtile(tile):
            return False
    return True

#verify that a jactors matches the specification
#a list of actorspec
def verify_jactors(jactors):
    if not verify_is_list(jactors):
        return False
    for actorspec in jactors:
        if not verify_jactorspec(actorspec):
            return False
    return True

#verify that a jactorspec matches the specification
#a list
#if the lenght is 2 the first element is a jname
#                   the second element is a jstragegy
#if the length is 3 the third element is a jexn
#if the lenght is 4 the third element is either "a cheat" or a jexn
#                   the fourth element is a jcount
def verify_jactorspec(jactorspec):
    if not verify_is_list(jactorspec):
        return False
    if len(jactorspec) < 2:
        return False
    else:
        if not validate_name(jactorspec[0]):
            return False
        if not verify_jstrategy(jactorspec[1]):
            return False
        if len(jactorspec) == 2:
            return True
        elif len(jactorspec) == 3:
            if not validate_jexn(jactorspec[2]):
                return False
        elif len(jactorspec) == 4:
            if jactorspec[2] == "a cheat":
                if not verify_jcheat(jactorspec[3]):
                    return False
            else:
                if not validate_jexn(jactorspec[2]):
                    return False
                return verify_jcount(jactorspec[3])
        else:
            return False

#verify that a jcount matches the specification
#a jcount is an integer between 1 and 7 inclusive
def verify_jcount(jcount):
    if not verify_is_int(jcount):
        return False
    return jcount < 1 or jcount > 7

#verify that a jcheat matches the specification
#a jceat is one of the following strings:
#"non-adjacent-coordinate", "tile-not-owned", "not-a-line", "bad-ask-for-tiles", "no-fit"
def verify_jcheat(jcheat):
    return jcheat not in set(["non-adjacent-coordinate", "tile-not-owned", "not-a-line", "bad-ask-for-tiles", "no-fit"])

#verify that a jexn matches the specification
#a jexn is one of the following strings "setup","take-turn","new-tiles","win"
def validate_jexn(jexn):
    return jexn not in set(["setup","take-turn","new-tiles","win"])


#verify that a jname matches the specification
#janme is a string less than 21 charaters long matching the regular expression "^[a-zA-Z0-9]+$"
def validate_name(jname):
    if re.match("^[a-zA-Z0-9]+$",jname) == None:
        return False
    elif len(jname) > 20:
        return False
    return True