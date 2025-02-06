import unittest
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Map import GameMap, Tile, Position
from scoring import score_turn, score_number_tiles, score_complete_q, possible_q_tiles, get_connected_tiles, score_extend, score_place_all_tiles, score_extend_helper, match_color_or_shape



class TestRules(unittest.TestCase):
    def test_score_turn(self):
        tiles = {Position(0,0): Tile('green', '8star'), Position(0, 1): Tile('blue', '8star'),
                  Position(0, 2): Tile('blue', 'circle'), Position(1, 2): Tile('red', 'circle'),
                    Position(2,2): Tile('green', 'circle')}
        map = GameMap(Tile("red", "circle"),tiles=tiles)
        placements = [(Position(2, 2), Tile('green', 'circle'))]
        self.assertEqual(4, score_turn(map, placements, 3))
        
    def test_score_number_tiles(self):
        placements_0 = [(Position(2, 2), Tile('green', 'circle'))]
        placements_1 = [(Position(2, 2), Tile('green', 'circle')), (Position(2, 2), Tile('green', 'circle')),
                         (Position(2, 2), Tile('green', 'circle')),(Position(2, 2), Tile('green', 'circle')),
                         (Position(2, 2), Tile('green', 'circle')), (Position(2, 2), Tile('green', 'circle'))]
        
        self.assertEqual(1, score_number_tiles(placements_0))
        self.assertEqual(6, score_number_tiles(placements_1))
    
    def test_score_complete_q(self):
        tiles_one_q = {Position(0, 0): Tile('green', 'star'), Position(0,1):Tile('green', 'square'),
                        Position(0,2): Tile('green', 'circle'), Position(0, -1):Tile('green', 'clover'),
                         Position(0, -2): Tile('green', 'diamond'), Position(0, 3): Tile('green', '8star')}



        tiles_two_q = {Position(0,0): Tile('green', 'star'), Position(0,1): Tile('green', 'square'),
                        Position(0,2): Tile('green', 'circle'), Position(0, -1): Tile('green', 'clover'),
                          Position(0, -2): Tile('green', 'diamond'), Position(0, 3): Tile('green', '8star'), Position(-2,0): Tile('blue', 'star'), Position(-1,0): Tile('red', 'star'),
                            Position(1, 0): Tile('purple', 'star'), Position(2, 0): Tile('yellow', 'star'),
                              Position(3, 0): Tile('orange', 'star')}

        tiles_no_q = {Position(0,0): Tile('green', 'star'), Position(0,1): Tile('green', 'square'),
                       Position(0,2): Tile('yellow', 'square'), Position(0, -1): Tile('green', 'diamond'),
                         Position(0, -2): Tile('blue', 'star'), Position(0, 3): Tile('yellow', 'star')}
        
        placements = [(Position(0,0), Tile('green', 'star')), (Position(0,1), Tile('green', 'square'))]

  
        map1 = GameMap(Tile('green', 'star'), tiles_one_q)

        #map2 = GameMap(Tile('green', 'star'), tiles_two_q)
        #map3 = GameMap(Tile('green', 'star'), tiles_no_q)
        self.assertEqual(score_complete_q(tiles_one_q, placements), 6)
        self.assertEqual(score_complete_q(tiles_two_q, placements), 12)
        self.assertEqual(score_complete_q(tiles_no_q, placements), 0)
        

    def test_match_color_or_shape(self):
        tiles_q = {Position(0,0):Tile('green', 'star'), Position(0,1):Tile('green', 'square'),
                    Position(0,2):Tile('green', 'circle'), Position(0, -1):Tile('green', 'clover'),
                      Position(0, -2):Tile('green', 'diamond'), Position(0, 3):Tile('green', '8star')}

        tiles_no_q = {Position(0,0):Tile('green', 'star'), Position(0,1): Tile('green', 'square'),
                       Position(0,2):Tile('blue', 'square'), Position(0, -1):Tile('green', 'diamond'),
                         Position(0, -2): Tile('blue', 'star'), Position(0, 3): Tile('yellow', 'star')}
        
        positions = {Position(0, -2), Position(0, -1), Position(0, 0), Position(0, 1), Position(0, 2), Position(0, 3)}

        self.assertEqual(match_color_or_shape(tiles_q, positions), 6)
        self.assertEqual(match_color_or_shape(tiles_no_q, positions), 0)

    
    def test_is_q_possible(self):
        tiles_vertical_q = {Position(0,0):Tile('green', 'star'), Position(0,1):Tile('green', 'square'),
                             Position(0,2): Tile('blue', 'square'), Position(0, -1): Tile('green', 'diamond'),
                               Position(0, -2): Tile('blue', 'star'),
                                 Position(0, 3): Tile('yellow', 'star')}
        placement = (Position(0, 0), Tile('green', 'star'))
        
        tiles_no_q = {Position(0,0): Tile('green', 'star'), Position(0, 1): Tile('green', 'square'), Position(0,2): Tile('blue', 'square'),
        Position(0, -1): Tile('green', 'diamond'), Position(0, -2): Tile('blue', 'star'), Position(0, 4): Tile('yellow', 'star')}
        placement = (Position(0, 0), Tile('green', 'star'))

        self.assertEqual(possible_q_tiles(tiles_vertical_q, placement, Position(1,0)), set())
        self.assertEqual(possible_q_tiles(tiles_vertical_q, placement, Position(0,1)),
         {Position(0, -2), Position(0, -1), Position(0, 0), Position(0, 1), Position(0, 2), Position(0, 3)})
        self.assertEqual(possible_q_tiles(tiles_no_q, placement, Position(0,1)), set())
        
    def test_get_connected_tiles(self):
        # test (1, 0) & (0, 1) axis
        tiles = {Position(0,0):Tile('green', 'star'), Position(0,1):Tile('green', 'square'), 
        Position(-1, 0):Tile('green', 'diamond'), Position(-1, 0):Tile('blue', 'star'), Position(1, 0): Tile('yellow', 'star')}
        placement = (Position(0, 0), Tile('green', 'star'))

        self.assertEqual(get_connected_tiles(tiles, placement, Position(1,0)), {Position(-1, 0), Position(0, 0), Position(1, 0)})
        self.assertEqual(get_connected_tiles(tiles, placement, Position(0,1)), {Position(0, 0), Position(0, 1)})
        
    def test_score_extend(self):
        tiles = {Position(0,0): Tile('green', 'star'), Position(-1,0): Tile('red', 'star'), 
                 Position(1, 0): Tile('blue', 'star'),
                 Position(0, -1): Tile('green', 'clover'), 
                 Position(0, 1): Tile('blue', 'circle')}
        map = GameMap(Tile('green', 'clover'), tiles=tiles) 
        placements = [(Position(0, -1), Tile('green', 'clover')), (Position(0, 1), Tile('blue', 'circle'))]
        self.assertEqual(3, score_extend(tiles, placements))
    def test_score_extend_helper(self):
        tiles = {Position(0,0): Tile('green', 'star'), Position(-1,0): Tile('red', 'star'),
                Position(1, 0): Tile('blue', 'star'), 
                Position(0, -1): Tile("green", "clover")}
        
        placement_0 = (Position(0, -1), Tile('green', 'clover'))
        tuple = score_extend_helper(tiles, placement_0)  
        self.assertEqual(tuple[0], {Position(0, -1), Position(0, 0)})
    def test_score_place_all_tiles(self):
        placements = [(Position(0, -1), Tile('green', 'clover')), (Position(0, 1), Tile('blue', 'circle')), 
                                        (Position(0, -2), Tile('green', 'clover')), 
                                        (Position(0, 2), Tile('blue', 'circle'))]
        self.assertEqual(0, score_place_all_tiles(placements,6))
        self.assertEqual(6, score_place_all_tiles(placements,4))

if __name__ == '__main__':
    unittest.main()
    
