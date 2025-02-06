import random
from map import Color, Shape, GameMap, Tile, Position, render_tile, render_4star, render_8star, render_circle, render_clover, render_coordinates, render_diamond, render_square, render_star, generate_each_tile_type
import copy
from action import Action
from PIL import Image, ImageDraw, ImageColor, ImageFont

NUM_EACH_TILE = 30
HAND_SIZE = 6

''' 
Represents the data structure a player receives on its turn. This contains all information a player needs to make its
turn which includes the current map, the score of every player where the first item in the list is the active player's
score, the tiles in the active player's hand, and the number of tiles the referee has left.
'''
class PublicState():
    def __init__(self, map, scores, tile_bag, referee_tiles):
        self.map = map
        self.scores = scores
        self.tile_bag = tile_bag
        self.referee_tiles = referee_tiles
    def apply_action(self, action):
        self.map.add_tile(action[0], action[1])
        self.tile_bag.remove(action[1])

"""Represents a player's information."""
class PlayerInfo:
    id = 0

    def __init__(self, player, score=0, tile_bag: list = None):
        self.remote_player = player
        self.has_exchanged_or_passed = False
        self._score = score
        if tile_bag is None:
            self._tile_bag = []
        else:
            self._tile_bag = tile_bag

        self.id = copy.deepcopy(PlayerInfo.id)
        PlayerInfo.id += 1

    @property
    def get_tile_bag(self) -> list:
        return self._tile_bag

    @property
    def get_score(self):
        return self._score
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __hash__(self):
        return self.id.__hash__()
    
    def __str__(self):
        return self.remote_player.name


    """
    Adds all tiles in given list to the player's tiles bag.
    """
    def add_tiles(self, tiles) -> None:
        
        for tile in tiles: 
            self._tile_bag.append(tile)

    """
    Remove every tile in the given list from the player's tiles bag.
    """
    def remove_tiles(self, tiles) -> None:
        
        for tile in tiles: 
            if tile in self._tile_bag:
                self._tile_bag.remove(tile)

    '''
    Replaces the player's hand with the given set of tiles
    '''
    def replace_tiles(self, tiles):
        self._tile_bag = tiles

    '''
    Adds the given score to the player's current score
    '''
    def add_score(self, add_score):
        self._score += add_score

    def get_player(self):
        return self.remote_player
    
    def __str__(self):
        return str(self.remote_player.name())
    
    def render_tile_bag(self, x, y, draw, shape_size):
        self.render_name(x, y, draw, shape_size)
        for tile in self._tile_bag:
            render_tile(draw, tile, x, y, shape_size, ImageColor.getrgb(tile._color.value))
            x = x + shape_size

    def render_name(self, x, y, draw, shape_size):
        len(self._tile_bag) / 2 * shape_size
        font_size = int(shape_size / 2)
        font = ImageFont.truetype("/Q/Common/Other/Arial.ttf", font_size)
        draw.text((x + len(self._tile_bag) / 2 * shape_size - (shape_size / 2), y - 18),
                   (self.remote_player.name() + ': ' + str(self._score)), fill='black', font=font)

def generate_each_tile():
    """Generate one tile of each type (based on combinations of colors and shapes).
    """
    return generate_each_tile_type()




class State:
    def __init__(self, players, referee_tiles, map=None, seed=None):
        """
        Initializes a game state.
        """

        self._players = players
        self._seed = seed
        self._eliminated_players = []

        if referee_tiles != None:
            self._referee_tiles = referee_tiles
        else: 
            self._referee_tiles = self.generate_referee_tiles()
            self.shuffle_referee_tiles(self._seed)
            self.generate_player_tile_bags()

        if map == None:
            tile_0 = self._referee_tiles.pop(0)
            self._map = GameMap(referee_tile=tile_0)
        else:
            self._map = map
    
    def generate_player_tile_bags(self):
        for player in self._players:
            player._tile_bag = self._referee_tiles[:HAND_SIZE]
            self._referee_tiles = self._referee_tiles[HAND_SIZE:]

    def shuffle_referee_tiles(self, seed=None):
        """
        Shuffles the referee tiles. An optional seed can be provided for reproducibility.
        """
        if seed is not None:
            random.seed(seed)

        random.shuffle(self._referee_tiles)

    def generate_referee_tiles(self):
        """
        Generates a list of referee tiles using all possible color and shape combinations.
        """
        tiles = []
        for each_tile in range(NUM_EACH_TILE):
            tiles.extend(generate_each_tile_type())
        return tiles

    def get_active_player(self) -> PlayerInfo:
        """
        Fetches the current active player.
        """
        return self._players[0]

    def extract_data_for_active_player(self):
        """
        Extracts relevant game data for current activePlayer
        """
        return PublicState(copy.deepcopy(self._map),
                                      self.get_scores(),
                                        copy.deepcopy(self.get_active_player()._tile_bag),
                                          len(self._referee_tiles))
    
    
    def get_scores(self):
        scores = []
        for player in self._players:
            scores.append(player.get_score)
        return scores

    """
    Removes the active player from the game and adds player name to eliminated players.
    """
    def eliminate_active_player(self):
        self.eliminate_player(0)
        
    def eliminate_player(self, index):
        playerinfo = self._players.pop(index)
        self._eliminated_players.append(playerinfo.remote_player.name())

    def eliminate_by_id(self, id):
        player_info = [player for player in self._players if player.id == id][0]
        self._eliminated_players.append(player_info.remote_player.name())
        self._players = [player for player in self._players if player.id != id]

    def complete_turn(self, active_player):
        """
        Advances to the next turn. If a player was kicked this turn, the list is unchanged.
        """
        if len(self._players) > 0:
            if (active_player.remote_player.name() not in self._eliminated_players):
                last_player = self._players.pop(0)
                self._players.append(last_player)

    """
    Exchanges the tiles of a player with the referee tiles.
    """
    def exchange_tiles(self) -> None:
        
        player = self.get_active_player()
        player_tiles = player._tile_bag
        self._referee_tiles.extend(player_tiles)
        
        player.replace_tiles(self._referee_tiles[:(len(player_tiles))])

    """
    Returns the first tile from the referee's tile collection.
    """
    def get_tiles_from_referee(self, num_tiles):
        tiles_to_give = []
        for i in range(0, num_tiles):
            tiles_to_give.append(self._referee_tiles.pop(0))
        return tiles_to_give

    """
    Checks if the proposed list of (position, tiles) can be placed on the map.
    """
    def check_proposed_placements(self, placements):
        if not self._map.check_tiles_same_row_or_col(placements):
            return False

        placement_map = copy.deepcopy(self._map)
        for position, tile in placements:
            if placement_map.check_shares_side(position) and placement_map.check_rules(position,
                                                                                       tile) and position not in placement_map.get_tiles():
                placement_map.add_tile(position, tile)
            else:
                return False
        return True

    '''
    Checks if a player owns the tiles it has requested to place
    '''
    def player_owns_tiles(self, placements):
        active_player = self.get_active_player()
        player_tiles = active_player._tile_bag

        for position, tile in placements:
            if (tile not in player_tiles):
                return False
        return True

    def check_if_action_is_legal(self, action: Action):
        if action.actionString == 'pass':
            return True
        elif action.actionString == 'exchange':
            return self.is_exchange_action_valid()
        else:
            return self.is_place_action_valid(action.action())

    ''' 
    Handles the complete execution of a turn which can be one of three Actions (pass, exchange, place). Returns a boolean 
    if a player has been removed for this turn 
    '''
    def commit_action_to_state(self, action: Action):
        if action.actionString == 'pass':
            self.get_active_player().has_exchanged_or_passed = True
        elif action.actionString == 'exchange':
            self.exchange_turn()
            self.get_active_player().has_exchanged_or_passed = True
        else:
            placements = action.action()
            self.place_turn_workhorse(placements)
            self.get_active_player().has_exchanged_or_passed = False
     
     
    def is_place_action_valid(self, placements): 
        return self.player_owns_tiles(placements) and self.check_proposed_placements(placements)

    def place_turn_workhorse(self, placements):
        '''  Completes a turn where the player wants to place tile(s). This includes removing the tiles placed
        from the player's hand and replacing them with tiles from the ref if possible. 
        '''
        self.make_placements(placements)
        self.update_player_hand(placements)


    '''
    Removes the tiles a player has placed from its hand and refills the players hand with tiles from the referee up to the number of tiles that
    were placed.
    '''
    def update_player_hand(self, placements):
        active_player = self.get_active_player()
        self.remove_tiles_from_hand(active_player, placements)
        if not self.game_end():
            self.add_referee_tiles_to_hand(active_player, len(placements))

    

    
    def remove_tiles_from_hand(self, active_player, placements):
        tiles_placed = [x[1] for x in placements]

        active_player.remove_tiles(tiles_placed)

    def add_referee_tiles_to_hand(self, active_player, num_placements):
        num_tiles_to_add = min(num_placements, len(self._referee_tiles))
        tiles_to_add = self.get_tiles_from_referee(num_tiles_to_add)
        active_player.add_tiles(tiles_to_add)

    def make_placements(self, placements):
        for position, tile in placements:
            self._map.add_tile(position, tile)
    
    def is_exchange_action_valid(self):
        return len(self._referee_tiles) >= len(self.get_active_player().get_tile_bag)
    
    def exchange_turn(self):
        '''
        Completes an exchange turn. In order for the turn to be legal, the referee must have at least as many tiles
        as the player does in its hand.
        '''
        self.exchange_tiles()
    
    def new_tiles_needed(self, action):
        return action.actionString != 'pass' 
    

    def connect_remote_players(self, players):
      for i in range(len(players)):
          self._players[i].remote_player = players[i]


    '''
    Returns true if the game has ended.
    A game has ended if:
    1) There are no players remaining
    2) A full round has played where all players pass or exchange
    3) A player places all tiles in its hand in a turn
    '''
    def game_end(self):
        return (self.no_players_remaining() or 
                self.all_players_exchanged_or_passed() or 
                self.player_placed_all_tiles())

        
    def player_placed_all_tiles(self):
        return len([x for x in self._players if len(x._tile_bag)== 0]) > 0

    def no_players_remaining(self):
        return len(self._players) == 0

    def all_players_exchanged_or_passed(self):
            players_exchanged_or_pass = 0
            for player in self._players:
                if player.has_exchanged_or_passed == True:
                    players_exchanged_or_pass += 1

            if players_exchanged_or_pass == len(self._players):
                return True 
            else:
                return False
        
    ''' Determines which player has won the game. Returns a list of winners.
    '''
    def winners(self):
        winners =  []
        if (len(self._players) != 0):
            winning_score = self.winning_score()
            for player in self._players:
                if (player.get_score == winning_score):
                    winners.append(player.remote_player.name())
        return winners 


    '''
    Returns a list of players who have been eliminated from the game in order of which they were eliminated.
    '''
    def cheaters(self):
        return self._eliminated_players
    
    def winning_score(self):
        highest = self.get_active_player().get_score

        for player in self._players:
            if (player.get_score > highest):
                highest = player.get_score
        return highest
    
    def render_state(self):
        shape_size = 30
        im = Image.new("RGBA", (1200, 700))
        draw = ImageDraw.Draw(im)
        self._map.render(0, 250, draw, shape_size)
        self.render_player_hands(400, 39, draw, shape_size)
        self.render_referee_hand(400, 250, draw, shape_size)
        return im
    
    def render_referee_hand(self, x, y, draw, shape_size):
        for index, tile in enumerate(self._referee_tiles):
            y_up = index // 6 
            render_tile(draw, tile, x + (index % 6)*shape_size, y + y_up*shape_size, shape_size, ImageColor.getrgb(tile._color.value))


    
    def render_player_hands(self, x, y, draw, shape_size):
        for player in self._players:
            player.render_tile_bag(x, y, draw, shape_size)
            y = y + 50
        
    
class GameStateBuilder:
    def __init__(self):
        self.referee_tiles = []
        self.map = None
        self.players = []

    def set_referee_tiles(self, referee_tiles):
        self.referee_tiles = referee_tiles
        return self
    def set_map(self, map):
        self.map = map
        return self
    def set_players(self, players):
        self.players = players
        return self
    def build(self):
        return State(self.players, self.referee_tiles, self.map, None)
        

class PlayerInfoBuilder:
    def __init__(self):
        self.tile_bag = []
        self.player = None
        self.score = 0
        pass

    def set_score(self, score):
        self.score = score
        return self

    def add_tile(self, tile):
        self.tile_bag.append(tile)
        return self

    def assign_player(self, player):
        self.player = player
        return self

    def build(self):
        return PlayerInfo(self.player, self.score, self.tile_bag)
