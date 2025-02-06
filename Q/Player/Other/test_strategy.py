
import unittest
import sys, os
#sys.path.append(os.path.join(os.path.dirname(__file__), '...'))
import sys
from pathlib import Path
sys.path.insert(0, os.path.abspath('../../Common'))
from Map import GameMap, Tile, Position
sys.path.insert(0, os.path.abspath('../'))
from strategy import Dag, Ldasg



class TestDag(unittest.TestCase):
    def test_tiles_to_place(self):
        tiles_0 = {Position(0, 0): Tile('green', 'star'), Position(0,1):Tile('blue', 'square'),
                        Position(0,2): Tile('green', 'square'), Position(0, 3): Tile('purple', 'diamond'), 
                        Position(0, -1):Tile('orange', 'square'),
                         Position(0, -2): Tile('orange', 'diamond')}
        tiles_1 = {Position(0, 0): Tile('blue', 'star'), Position(0,1):Tile('blue', 'square'),
                        Position(0,2): Tile('blue', 'square'), Position(0, 3): Tile('blue', 'diamond'), 
                        Position(0, -1):Tile('blue', 'square'),
                         Position(0, -2): Tile('blue', 'diamond')}
        
        hand_0 = [Tile('purple', '8star'), Tile('orange', '8star'), Tile('red', 'clover'), Tile('green', 'circle')]
    
        map_0 = GameMap(Tile('green', 'star'), tiles_0)
        map_1 =  GameMap(Tile('green', 'star'), tiles_1)
        
        self.assertEqual((Position(-1, -2), Tile('orange', '8star')), Dag().next_tile(map_0, hand_0)) # the lowest scored tile is selected (check for tie breaker)
        self.assertFalse(Dag().next_tile(map_1, hand_0)) # false is returned (no tile can be placed)
    def test_replace_or_pass(self):
        
        self.assertEqual(Dag().replace_or_pass(6, 10), True) # the player has tiles in its hand (return true [exchange])
        self.assertEqual(Dag().replace_or_pass(6, 3), False) # the player does not have tiles in its hand (return false [pass])

    def test_iterate_strategy(self):
        tiles_0 = {Position(0, 0): Tile('green', 'star'), Position(0,1):Tile('blue', 'square'),
                    Position(0,2): Tile('green', 'square'), Position(0, 3): Tile('purple', 'diamond'), 
                    Position(0, -1):Tile('orange', 'square'),Position(0, -2): Tile('orange', 'diamond')}
        tiles_1 = {Position(0, 0): Tile('blue', 'star'), Position(0,1):Tile('blue', 'square'),
                    Position(0,2): Tile('blue', 'square'), Position(0, 3): Tile('blue', 'diamond'), 
                    Position(0, -1):Tile('blue', 'square'), Position(0, -2): Tile('blue', 'diamond')}
        
        hand_0 = [Tile('purple', '8star'), Tile('orange', '8star'), Tile('red', 'clover'), Tile('green', 'circle')]
    
        map_0 = GameMap(Tile('green', 'star'), tiles_0)
        map_1 =  GameMap(Tile('green', 'star'), tiles_1)

        self.assertEqual([(Position(-1, -2), Tile('orange', '8star')), (Position(-2, -2), Tile('purple', '8star')), (Position(-1, 0), Tile('green', 'circle'))],Dag().iterate_strategy(map_0, hand_0, 10))
class TestLDasg(unittest.TestCase):
    
    def test_next_tile(self):

        tiles_0 = {Position(0, 0): Tile('green', 'star'), Position(0,1):Tile('green', 'square'),
                        Position(0,2): Tile('green', 'circle'), Position(0, -1):Tile('green', 'clover'),
                         Position(0, -2): Tile('green', 'diamond')}

        map_0 = GameMap(Tile('green', 'circle'), tiles_0)

        hand = [Tile('green', 'star'), Tile('purple', 'star'),
                        Tile('red', 'square'), Tile('red', 'circle'),
                         Tile('yellow', '8star')]

        hand2 = [Tile('yellow', '8star')]
        
        self.assertEqual(Ldasg().next_tile(map_0, hand), (Position(-1, -2), Tile('green', 'star'))) # the lowest scored tile is select (check for prior)
        self.assertFalse(Ldasg().next_tile(map_0, hand2)) # false is returned (no tile can be placed)

    def test_replace_or_pass(self):
        
        self.assertEqual(Ldasg().replace_or_pass(6, 10), True) # the player has tiles in its hand (return true [exchange])
        self.assertEqual(Ldasg().replace_or_pass(6, 3), False) # the player does not have tiles in its hand (return false [pass])

    def test_iterate_strategy(self):

        tiles_0 = {Position(0, 0): Tile('green', 'star'), Position(0,1):Tile('green', 'square'),
                        Position(0,2): Tile('green', 'circle'), Position(0, -1):Tile('green', 'clover'),
                         Position(0, -2): Tile('green', 'diamond')}
        map_0 = GameMap(Tile('green', '8star'), tiles_0)

        hand = [Tile('green', 'star'), Tile('purple', 'star'), Tile('red', 'square'), Tile('red', 'circle'), Tile('yellow', '8star')]
      
        hand2 = [Tile('yellow', '8star')]

        #map_0.render_board(map_0._tiles, True).show()
        
        self.assertEqual(Ldasg().iterate_strategy(map_0, hand, 15), [(Position(-1, -2), Tile('green', 'star')), (Position(-2, -2), Tile('purple', 'star')),
        (Position(-1, 1), Tile('red', 'square')), (Position(-1, 2), Tile('red', 'circle'))]) # list of tile placements
        self.assertTrue(Ldasg().iterate_strategy(map_0, hand2, 15)) # exchange (true)
        self.assertFalse(Ldasg().iterate_strategy(map_0, hand2, 0)) # pass (false)


if __name__ == '__main__':
    unittest.main()
    
