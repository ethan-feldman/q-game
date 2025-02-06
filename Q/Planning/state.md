# Game State Design Memo

## Data Representation
To represent the game state, a GameState class will be created.
Some variables:

- map = map # Map from Map.py to represent the board
- players = [player] # players to reprent 
- turn_counter = 0 # turn counter to keep track of turns
- score = [int] # array of scores to represent the each score of the players
- referee_tiles = [] # starting array of tiles
- tile_bags = [[Tiles]] # array of array of tiles held by each player, based on index

Other methods
 
generate_random_tile_bag(): Generates 1080 valid tiles in a random order to be picked from.  Returns a list of Tiles

generate_random_tile_bag(seed): Generates 1080 valid tiles in a seeded-random way for testing purposes. Returns a list of Tiles

remove_tile(player, Tile): Remove a tile from the player's tile bag.

add_tile(player, Tile): Adds a tile to the player's tile bag.

append_tile(Tile): appends tiles to the referee's tile bag.

pop_tile(): remove tile from the front referee's randomly arranged tile bag. Returns the removed tile.

update_score(index, amount): Index is the player's ID to change score of by requested amount.

increment_turn(): adds one to turn. 
