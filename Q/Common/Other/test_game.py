import unittest
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Map import *


class TestTile(unittest.TestCase):
    '''
    def test_color(self):
        tile_0 = Tile("green", "circle")
        self.assertEqual(tile_0.get_color, "green")


    def test_shape(self):
        tile_0 = Tile("red", "8star")
        self.assertEqual(tile_0.get_shape, "8star")
    '''
    
class TestMap(unittest.TestCase):
    '''
    def test_map_referee_tile(self):
        referee_tile_0 = Tile("blue", "diamond")
        game_map_0 = GameMap(referee_tile_0)
        self.assertEqual(list(game_map_0.get_tiles.keys())[0], (0, 0))
        self.assertEqual(list(game_map_0.get_tiles.values())[0]._color, referee_tile_0.get_color)
        self.assertEqual(list(game_map_0.get_tiles.values())[0]._shape, referee_tile_0.get_shape)

    def test_add_tile(self):
        referee_tile_0 = Tile("green", "circle")
        game_map_0 = GameMap(referee_tile_0)
        self.assertTrue(game_map_0.add_tile(Tile("green","star"), 0, 1))
        coordinates = list(game_map_0.get_tiles.keys())
        tiles = list(game_map_0.get_tiles.values())
        self.assertEqual(coordinates[0], (0, 0))
        self.assertEqual(coordinates[1], (0, 1))
        self.assertEqual(tiles[0].get_color, "green")
        self.assertEqual(tiles[0].get_shape, "circle")
        self.assertEqual(tiles[1].get_color, "green")
        self.assertEqual(tiles[1].get_shape, "star")

    def test_check_adjacent_tile(self):
        referee_tile_0 = Tile("green", "circle")
        game_map_0 = GameMap(referee_tile_0)
        self.assertFalse(game_map_0.check_adjacent_tile(0,0))
        self.assertTrue(game_map_0.check_adjacent_tile(-1,0))


    def test_get_possible_insertions(self):
        referee_tile_0 = Tile("green", "circle")
        game_map_0 = GameMap(referee_tile_0)
        tile_1 = Tile("blue", "star")
        insertions = game_map_0.get_possible_insertions(tile_1)
        self.assertEqual(len(insertions), 0) 

        referee_tile_0 = Tile("green", "circle")
        game_map_0 = GameMap(referee_tile_0)
        tile_1 = Tile("green", "star")
        insertions = game_map_0.get_possible_insertions(tile_1)
        self.assertEqual(len(insertions), 4) 
        self.assertTrue((0,1) in insertions)
        self.assertTrue((1, 0) in insertions)
        self.assertTrue((-1, 0) in insertions)
        self.assertTrue((0,-1) in insertions)
        '''
    '''
    def test_check_add_tiles_with_rules(self):
        referee_tile_0 = Tile("green", "circle")
        game_map_0 = GameMap(referee_tile_0)
        tile_1 = Tile("blue", "star")
        self.assertFalse(game_map_0.check_rules(Position(0, 1), tile_1))
        self.assertFalse(game_map_0.check_rules(Position(2, 2), tile_1))
        '''
    '''
    def test_get_neighbors(self):
        referee_tile_0 = Tile("green", "circle")
        game_map_0 = GameMap(referee_tile_0)
        neighbors = game_map_0.get_neighbors(2, 2)
        self.assertTrue((2, 1) in neighbors)
        self.assertTrue((1, 2) in neighbors)
        self.assertTrue((2, 3) in neighbors)
        self.assertTrue((3, 2) in neighbors)
    '''
    def test_render_board(self):
        referee_tile_0 = Tile("red", "circle")
        game_map_0 = GameMap(referee_tile_0, None)
        self.assertTrue(game_map_0.add_tile(Position(-1, 0), Tile("red","diamond")))
        game_map_0.add_tile(Position(-2, 0), Tile("red", "8star"), )
        game_map_0.add_tile(Position(-3, 0), Tile("red", "star"))
        game_map_0.add_tile(Position(-4, 0), Tile("red", "square"))
        game_map_0.add_tile(Position(0, 1), Tile("green", "circle"))
        game_map_0.add_tile(Position(0, 2), Tile("purple", "circle"))
        game_map_0.add_tile(Position(1, 2), Tile("blue", "circle"))
        game_map_0.add_tile(Position(0, 3), Tile("purple", "star"))
        game_map_0.add_tile(Position(0, -1), Tile("orange", "circle"))
        game_map_0.add_tile(Position(0, -2), Tile("green", "star"))
        game_map_0.add_tile(Position(0, -3), Tile("green", "square"))
        game_map_0.add_tile(Position(0, -4), Tile("blue", "clover"))
        game_map_0.add_tile(Position(1, -4), Tile("green", "clover"))
        game_map_0.add_tile(Position(2, -4), Tile("orange", "clover"))
        im = game_map_0.render_board()
        im.show()


if __name__ == '__main__':
    unittest.main()
    
