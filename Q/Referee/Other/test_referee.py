import unittest
 
import sys, os
sys.path.insert(0, os.path.abspath('..'))
from referee import Referee
sys.path.insert(0, os.path.abspath('../Player'))
from player import Player
from strategy import Dag, Ldasg
sys.path.insert(0, os.path.abspath('../../Common'))
import game_state
import map

class TestReferee(unittest.TestCase):
    '''
    def testReferee(self):
        player_0 = Player("john", 20, Dag())
        player_1 = Player("alice", 9, Dag())
        player_list = [player_0, player_1]
        # create players and pass to referee
        referee(player_list)

        # need to manufacture gamestate (with seed) for testing
        seed = 10
        gamestate_0 = game_state.State(player_list, None, 10)
    

    
    def test_set_player_states(self):
        pass


    # no longer works due to changes in gamestate initialization
    def test_set_up(self):
        player_0 = Player("john", 20, Dag())
        player_1 = Player("alice", 9, Dag())
        player_list = [player_0, player_1]

        ref_tiles = [map.Tile(map.Color.ORANGE, map.Shape.SQUARE), map.Tile(map.Color.YELLOW, map.Shape.EIGHT_STAR),
            map.Tile(map.Color.ORANGE, map.Shape.DIAMOND), map.Tile(map.Color.RED, map.Shape.DIAMOND),
            map.Tile(map.Color.BLUE, map.Shape.CIRCLE), map.Tile(map.Color.PURPLE, map.Shape.CLOVER),
            map.Tile(map.Color.RED, map.Shape.SQUARE), map.Tile(map.Color.RED, map.Shape.CLOVER),
            map.Tile(map.Color.RED, map.Shape.SQUARE), map.Tile(map.Color.GREEN, map.Shape.CLOVER),
            map.Tile(map.Color.GREEN, map.Shape.EIGHT_STAR), map.Tile(map.Color.PURPLE, map.Shape.EIGHT_STAR),
            map.Tile(map.Color.ORANGE, map.Shape.STAR), map.Tile(map.Color.ORANGE, map.Shape.CIRCLE)]
        
        # pass in specific referee tiles (need at least (6 * num players) + 1)
        # when does generate player tiles get called (currently wrong regardless?)
        # players have hands, ref has 1 tile, orange star at 0,0
        gamestate_0 = game_state.State(set_player_states(player_list), ref_tiles)
        set_up(player_list, gamestate_0)

        self.assertEqual(player_0._tiles, [map.Tile(map.Color.ORANGE, map.Shape.SQUARE), map.Tile(map.Color.YELLOW, map.Shape.EIGHT_STAR),
            map.Tile(map.Color.ORANGE, map.Shape.DIAMOND), map.Tile(map.Color.RED, map.Shape.DIAMOND),
            map.Tile(map.Color.BLUE, map.Shape.CIRCLE), map.Tile(map.Color.PURPLE, map.Shape.CLOVER)])
        self.assertEqual(player_1._tiles, [map.Tile(map.olor.RED, map.Shape.SQUARE), map.Tile(map.Color.RED, map.Shape.CLOVER),
            map.Tile(map.Color.RED, map.Shape.SQUARE), map.Tile(map.Color.GREEN, map.Shape.CLOVER),
            map.Tile(map.Color.GREEN, map.Shape.EIGHT_STAR), map.Tile(map.Color.PURPLE, map.Shape.EIGHT_STAR)])

        '''
        

    def test_referee_with_gamestate(self):
        # gamestate one turn from end
        # gamestate further from end
        # test end game conditions b/c wasn't tested earlier?

        #--------------------------------------------------
        player_0 = Player("john", 20, Dag())
        player_1 = Player("alice", 9, Dag())
        player_list = [player_0, player_1]

        ref_tiles = [map.Tile(map.Color.ORANGE, map.Shape.CIRCLE)]


        ref_tile = map.Tile(map.Color.ORANGE, map.Shape.SQUARE)
        map_0 = map.GameMap(referee_tile=ref_tile)
        player_0 = game_state.PlayerInfo(Player("john", 20, Dag()), 0, [map.Tile(map.Color.YELLOW, map.Shape.EIGHT_STAR),
            map.Tile(map.Color.ORANGE, map.Shape.DIAMOND), map.Tile(map.Color.RED, map.Shape.DIAMOND),
            map.Tile(map.Color.BLUE, map.Shape.CIRCLE), map.Tile(map.Color.PURPLE, map.Shape.CLOVER),
            map.Tile(map.Color.RED, map.Shape.SQUARE)])
        player_1 = game_state.PlayerInfo(Player("alice", 9, Dag()), 0, [map.Tile(map.Color.RED, map.Shape.CLOVER),
            map.Tile(map.Color.RED, map.Shape.SQUARE), map.Tile(map.Color.GREEN, map.Shape.STAR),
            map.Tile(map.Color.GREEN, map.Shape.EIGHT_STAR), map.Tile(map.Color.PURPLE, map.Shape.EIGHT_STAR),
            map.Tile(map.Color.ORANGE, map.Shape.STAR)])
        
        gamestate_0 = game_state.State([player_0, player_1], ref_tiles, map=map_0)

        referee = Referee(game_state=gamestate_0)
        referee.set_up()
        referee.run_game()


        self.assertEqual(gamestate_0._players[0].get_score, 15)
        self.assertEqual(gamestate_0._players[1].get_score, 23)

    def test_notify_winners(self):
        # how to test given that there is no return
        # currently does nothing in Player class - could have it return the given boolean for testing
        # but seems unnecessary
        pass


if __name__ == '__main__':
    unittest.main()
    
