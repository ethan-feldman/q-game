from abc import ABC, abstractmethod
import sys, copy, os
sys.path.insert(1, os.path.abspath('../../Common'))
from map import Position, Tile, generate_each_tile_type
from action import Pass, Exchange, Place
import random 
import itertools, functools

class Strategy(ABC):
    # Least to Most
    # Red, Green, Blue, Yellow, Orange, Purple
    # Star, 8star, Square, Circle, Clover, Diamond
    # Shape takes precedent over color

    @abstractmethod
    # determines the tile to be placed according to the
    # outline of the strategy. Returns false otherwise. 
    def next_tile(self, map, hand, prev_placements):
        pass

    # returns whether a player should replace its tiles or pass its turn in the event
    # no tiles can be placed
    def replace_or_pass(self, num_player_tiles, num_ref_tiles):
        if num_player_tiles <= num_ref_tiles:
            return Exchange()
        else:
            return Pass()

    def get_action(self, map, hand, num_player_tiles, num_ref_tiles):
        if self.next_tile(map, hand, []) != False:
            return Place([self.next_tile(map, hand, [])])
        else:
            return self.replace_or_pass(num_player_tiles, num_ref_tiles)

    # Composite method of a strategy, it will iterate over the desired strategy for each tile placement
    # returning either the longest list of placements or true (for exchange) or false (for pass)
    def iterate_strategy(self, public_state):
        hand = public_state.tile_bag
        map = public_state.map
        num_ref_tiles = public_state.referee_tiles
        moves = []
        tile_to_place = self.next_tile(map, hand, moves)
        while(tile_to_place):
            public_state.apply_action(tile_to_place)
            moves.append(tile_to_place)
            tile_to_place = self.next_tile(map, hand, moves)
        if (len(moves) > 0):
            return Place(moves)
        else:
            return self.replace_or_pass(len(hand), num_ref_tiles)


# Using the following lexicographic ordering of tiles: 
# Red, Green, Blue, Yellow, Orange, Purple
# Star, 8star, Square, Circle, Clover, Diamond
# where shape takes precedent over color, dag choses the player's smallest tile that can
# extend the map using row-column order for tiles
class Dag(Strategy):
    def next_tile(self, map, hand, prev_placements):
        hand.sort()
        for tile in hand:
            restricted = map.restrict_possible_insertions(tile, prev_placements)
            if (len(restricted) > 0):
                spots = list(restricted)
                spots.sort()
                spot = spots[0]
                return (spot, tile)
        return False 


# Using the following lexicographic ordering of tiles: 
# Red, Green, Blue, Yellow, Orange, Purple
# Star, 8star, Square, Circle, Clover, Diamond
# where shape takes precedent over color, ldasg choses the player's smallest tile that can
# extend the map. The tile that would have the most neighbors is selected in ties. 
# Row column ordering is used to break exisiting ties.
class Ldasg(Strategy):
    def next_tile(self, map, hand, prev_placements):
        hand.sort()
        for tile in hand:
            restricted = map.restrict_possible_insertions(tile, prev_placements)
            if (len(restricted) > 0):
                spots = list(restricted)
                spots.sort()
                spot = self.spot_with_most_neighbors(map._tiles, spots)
                return (spot, tile)
        return False

    #  Returns the position (spot) for the place that has the most neighbors
    #  If there is a tie, returns the lowest Position (row-column ordering)
    def spot_with_most_neighbors(self, tiles, spots):
        neighbors = 0
        position = Position(float('inf'), float('inf')) # row - column ordering
        for spot in spots:
            local_neighbors = 0
            for neighbor in spot.get_neighbors():
                if tiles.get(neighbor):
                    local_neighbors = local_neighbors + 1

            if (local_neighbors > neighbors):
                position = spot
                neighbors = local_neighbors

            elif (local_neighbors == neighbors and spot < position):
                position = spot
        return position


'''
Denotes a player that in response to being granted a turn,
requests the placement of a tile that is not adjacent to a placed tile.
'''
class NonAdjacentCoordinate(Strategy):
    def __init__(self, fallback_strategy):
        self._fallback = fallback_strategy

    # attempts to place a tile at a location not adjacent to any existing tiles
    def iterate_strategy(self, public_state):
        hand = public_state.hand
        map = copy.deepcopy(public_state.map)
        min_x, max_x, min_y, max_y = map.get_dimensions()
        pos = Position(max_x + 2, max_y + 2)
        return Place([(pos, hand[0])])

    #implement abstract method
    def next_tile(self, map, hand, prev_placements):
        return self._fallback.next_tile(map, hand, prev_placements)

'''
Denotes a player that in response to being granted a turn,
    requests the placement of a tile that it does not own.
'''
class TileNotOwned(Strategy):
    def __init__(self, fallback_strategy):
        self._fallback = fallback_strategy

    #get ways in which to cheat
    def _get_all_possible_cheats(self, map, hand):
        cheater_tiles = generate_each_tile_type()
        #if tiles cannot be in hand
        cheater_tiles = [tile for tile in cheater_tiles if tile not in hand]
        valid_cheater_tiles = []
        for tile in cheater_tiles:
            if len(map.get_possible_insertions(tile)) > 0:
                valid_cheater_tiles.append(tile)
        return valid_cheater_tiles

    # attempts to place a tile that is not in the player's hand
    def iterate_strategy(self, public_state):
        hand = public_state.hand
        map = copy.deepcopy(public_state.map)
        num_ref_tiles = public_state.num_ref_tiles
        if self._can_cheat(map, hand):
            return self._fallback.iterate_strategy(map, self._get_all_possible_cheats(map, hand)[0:len(hand)], num_ref_tiles)
        else:
            return self._fallback.iterate_strategy(map, hand, num_ref_tiles)

    #is it possibleto cheat
    def _can_cheat(self, map, hand):
        return len(self._get_all_possible_cheats(map, hand)) > 0

    #implement abstract method
    def next_tile(self, map, hand, prev_placements):
        return self._fallback.next_tile(map, hand, prev_placements)

'''
Denotes a player that in response to being granted a turn,
requests placements that are not in one line (row, column).
'''
class NotALine(Strategy):
    def __init__(self, fallback_strategy):
        self._fallback = fallback_strategy

    #get possible ways to cheat
    def _get_all_possible_cheats(self, map, hand):
        accum = []
        for i, tile in enumerate(hand):
            possible_insertions = map.get_possible_insertions(tile)
            for also_tile in hand[i+1:]:
                other_possible_insertions = map.get_possible_insertions(also_tile)

                for p1 in possible_insertions:
                    for p2 in other_possible_insertions:
                        if not map.check_tiles_same_row_or_col([(p1,tile), (p2,also_tile)]):
                            accum.append([(p1, tile), (p2, also_tile)])
        return accum


    #is it possible to cheat
    def _can_cheat(self, map, hand):
        return len(self._get_all_possible_cheats(map, hand)) > 0

    #attempts to place tiles not in a line
    def iterate_strategy(self, public_state):
        hand = public_state.hand
        map = copy.deepcopy(public_state.map)
        num_ref_tiles = public_state.num_ref_tiles
        if self._can_cheat(map, hand):
            cheats = self._get_all_possible_cheats(map, hand)
            return Place(cheats[0])
        else:
            return self._fallback.iterate_strategy(map, hand, num_ref_tiles)

    #implement abstract method
    def next_tile(self, map, hand, prev_placements):
        return self._fallback.next_tile(map, hand, prev_placements)


'''
This strategy cheats by asking for tiles incorrectly when possible
'''
class BadAskForTiles(Strategy):
    def __init__(self, fallback_strategy):
        self._fallback = fallback_strategy

    #is it possible to cheat
    def _can_cheat(self, hand, num_ref_tiles):
        return len(hand) > num_ref_tiles

    #attempts to ask for tiles when the player has more than the referee
    def iterate_strategy(self, public_state):
        hand = public_state.hand
        map = copy.deepcopy(public_state.map)
        num_ref_tiles = public_state.num_ref_tiles
        if self._can_cheat(hand, num_ref_tiles):
            return Exchange()
        else:
            return self._fallback.iterate_strategy(map, hand, num_ref_tiles)

    #implement abstract method
    def next_tile(self, map, hand, prev_placements):
        return self._fallback.next_tile(map, hand, prev_placements)

'''
Denotes a player that in response to being granted a turn,
requests the placement of a tile that does not match its adjacent tiles.
'''
class NoFit(Strategy):
    def __init__(self, fallback_strategy):
        self._fallback = fallback_strategy

    #get possible ways to cheat
    def _get_all_possible_cheats(self, map, hand):
        all_possible_locations = set(itertools.chain(*[map.get_possible_insertions(x) for x in generate_each_tile_type()]))
        acc = []
        for tile in hand:
            possible_valid_insertions = set(map.get_possible_insertions(tile))
            locations_no_match = all_possible_locations.difference(possible_valid_insertions)
            if locations_no_match != set():
                acc.append((list(locations_no_match),tile))
        return acc

    #attempt to cheat using just tiles in hand
    def _hand_cheat(self, map, hand):
        for i, t1 in enumerate(hand):
            for t2 in hand[i:]:
                if t1._color != t2._color or t1._shape != t2._shape:
                    original_locs = map.get_possible_insertions(t1) 
                    extra_space_locs = [x for x in original_locs if len([y for y in x.get_neighbors() if y in map._tiles.keys()]) > 0]
                    if len(extra_space_locs) > 0:
                        map.add_tile(extra_space_locs[0], t1)
                        new_locs = map.get_possible_insertions(t1).difference(original_locs)
                        return (list(new_locs)[0], t2)
        return None

    #is it possible to cheat with just the tiles in the hand
    def _can_hand_cheat(self, map, hand):
        return self._hand_cheat(map, hand) != None

    #is is possible to cheat      
    def _can_cheat(self, map, hand):
        return len(self._get_all_possible_cheats(map, hand)) > 0 or self._can_hand_cheat(map, hand)

    #attempts to place a tile next to a tile that does not share a like color or shape
    def iterate_strategy(self, public_state):
        hand = public_state.hand
        map = copy.deepcopy(public_state.map)
        num_ref_tiles = public_state.num_ref_tiles
        m = copy.deepcopy(map)
        h = copy.deepcopy(hand)
        if self._can_cheat(m, h):
            if self._can_hand_cheat(m, h):
                return Place([self._hand_cheat(m, h)])
            positions, tile = self._get_all_possible_cheats(m, h)[0]
            return Place([(positions[0], tile)])
        else:
            return self._fallback.iterate_strategy(map, hand, num_ref_tiles)

    #implement abstract method
    def next_tile(self, map, hand, prev_placements):
        return self._fallback.next_tile(map, hand, prev_placements)

