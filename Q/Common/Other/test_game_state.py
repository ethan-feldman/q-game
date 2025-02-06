import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from game_state import State, generate_each_tile_type, PlayerInfo
from Map import Tile, Color, Shape, Position


class TestGameFunctions(unittest.TestCase):

    def test_generate_each_tile_type(self):
        tiles = generate_each_tile_type()
        self.assertEqual(len(tiles), len(Color) * len(Shape))

    def test_eliminate_player(self):
        state = State(Tile(Color.RED, Shape.CIRCLE))
        player1 = PlayerInfo(1, [])
        player2 = PlayerInfo(2, [])
        state.players = [player1, player2]
        state.scores = [10,5]

        state.eliminate_player(1)
        self.assertNotIn(player1, state.players)
        self.assertNotIn(1, state.scores)

    def test_get_active_player(self):
        state = State(Tile(Color.RED, Shape.CIRCLE))
        player1 = PlayerInfo(1, [])
        player2 = PlayerInfo(2, [])
        state.players = [player1, player2]

        self.assertEqual(state.get_active_player(), player1)

        state.current_turn = 1
        self.assertEqual(state.get_active_player(), player2)

    def test_complete_turn(self):
        state = State(Tile(Color.RED, Shape.CIRCLE))
        player1 = PlayerInfo(1, [])
        player2 = PlayerInfo(2, [])
        state.players = [player1, player2]
        state.current_turn = 0

        state.complete_turn()
        self.assertEqual(state.current_turn, 1)

        state.complete_turn()
        self.assertEqual(state.current_turn, 0)

    def test_exchange_tiles(self):
        state = State(Tile(Color.RED, Shape.CIRCLE))
        player1 = PlayerInfo(1, [Tile(Color.RED, Shape.CIRCLE)])
        state.players = [player1]
        state.referee_tiles = [Tile(Color.BLUE, Shape.SQUARE), Tile(Color.GREEN, Shape.STAR)]

        state.exchange_tiles(0)

        self.assertIn(Tile(Color.RED, Shape.CIRCLE), state.referee_tiles)
        self.assertNotIn(Tile(Color.RED, Shape.CIRCLE), player1._tiles_bag)
        self.assertEqual(len(player1._tiles_bag), 1)

    def test_get_tile_from_referee(self):
        state = State(Tile(Color.RED, Shape.CIRCLE))
        state.referee_tiles = [Tile(Color.RED, Shape.CIRCLE)]

        tile = state.get_tile_from_referee()
        self.assertEqual(tile, Tile(Color.RED, Shape.CIRCLE))
        self.assertEqual(len(state.referee_tiles), 0)

        with self.assertRaises(Exception):
            state.get_tile_from_referee()

    def test_give_tile_from_referee(self):
        state = State(Tile(Color.RED, Shape.CIRCLE))
        player1 = PlayerInfo(1, [])
        state.players = [player1]
        state.referee_tiles = [Tile(Color.RED, Shape.CIRCLE)]

        state.give_tile_from_referee(0)

        self.assertIn(Tile(Color.RED, Shape.CIRCLE), player1._tiles_bag)
        self.assertEqual(len(state.referee_tiles), 0)

    def test_pop_1st_color_and_shape_in_player(self):
        state = State(Tile(Color.RED, Shape.CIRCLE))
        player1 = PlayerInfo(1, [Tile(Color.RED, Shape.CIRCLE), Tile(Color.BLUE, Shape.SQUARE)])
        state.players = [player1]

        popped_tile = state.pop_1st_color_and_shape_in_player(0, Color.RED, Shape.CIRCLE)
        self.assertEqual(popped_tile, Tile(Color.RED, Shape.CIRCLE))
        self.assertNotIn(popped_tile, player1._tiles_bag)

        
        with self.assertRaises(Exception):
            state.pop_1st_color_and_shape_in_player(0, Color.YELLOW, Shape.STAR)

    def test_check_proposed_placements(self):
        state = State(Tile(Color.RED, Shape.CIRCLE))
        placements = [(Position(0, 1), Tile(Color.RED, Shape.CIRCLE)), (Position(0,2), Tile(Color.RED, Shape.SQUARE))]
        self.assertTrue(state.check_proposed_placements(placements))

        placements = [(Position(1, 2), Tile(Color.RED, Shape.CIRCLE)), (Position(2, 3), Tile(Color.BLUE, Shape.SQUARE))]
        self.assertFalse(state.check_proposed_placements(placements))

    def test_check_tiles_same_row_or_col(self):
        state = State(Tile(Color.RED, Shape.CIRCLE))
        placements = [(Position(1, 2), Tile(Color.RED, Shape.CIRCLE)), (Position(1, 3), Tile(Color.BLUE, Shape.SQUARE))]
        self.assertTrue(state.check_tiles_same_row_or_col(placements))

        placements = [(Position(1, 2), Tile(Color.RED, Shape.CIRCLE)), (Position(2, 3), Tile(Color.BLUE, Shape.SQUARE))]
        self.assertFalse(state.check_tiles_same_row_or_col(placements))


if __name__ == "__main__":
    unittest.main()