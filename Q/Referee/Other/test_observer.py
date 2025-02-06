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
from observer import Observer, Renderer
from PySide6 import QtCore, QtWidgets, QtGui

class TestObserver(unittest.TestCase):
    def testobserver(self):
        app = QtWidgets.QApplication(sys.argv)
        observer = Observer()

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
        Referee(game_state=gamestate_0, observers=[observer]).run_game()

        window = observer.renderer
        window.show()
        app.exec()



if __name__ == '__main__':
    unittest.main()
    
