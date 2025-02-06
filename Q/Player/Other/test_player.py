import unittest
import sys, os
#sys.path.append(os.path.join(os.path.dirname(__file__), '...'))
import sys
from pathlib import Path
sys.path.insert(0, os.path.abspath('../../Common'))
from Map import GameMap, Tile, Position, ActivePlayerKnowledge
from action import Place, Exchange
sys.path.insert(0, os.path.abspath('../'))
from strategy import Dag, Ldasg
from player import Player

class TestPlayer(unittest.Testcase):

    def test_name(self):
        player1 = Player("Tester", 25, Dag())
        
        self.assertEqual(player1.name(), "Tester")
        player1._name = "Tester2"
        self.assertEqual(player1.name(), "Tester2")

    def test_take_turn(self):
        player1 = Player("Tester", 25, Dag())
        gamemap = GameMap({Position(0,0):Tile("blue", "diamond")})
        player1_knowledge = ActivePlayerKnowledge(gamemap, [0], [Tile("orange", "square"), Tile("yellow", "8star")] ,12)
        player1_knowledge = ActivePlayerKnowledge(gamemap, [0], [Tile("blue", "square"), Tile("yellow", "8star")] ,12)

        self.assertEqual(player1.takeTurn(player1_knowledge), Exchange())
        self.assertEqual(player1.takeTurn(player1_knowledge), Place(Position(-1, 0), Tile("blue", "square")))
        

    def test_newTiles(self):
        player1 = Player("Tester", 25, Dag())
        new_tiles_1 = [Tile("blue", "square"), Tile("yellow", "8star")]
        new_tiles_2 = []

        player1.newTiles(new_tiles_1)
        self.assertEqual(player1._tiles, new_tiles_1)
        player1.newTiles(new_tiles_2)
        self.assertEqual(player1._tiles, [])

    def test_win(self):
        pass # unnecessary test?

if __name__ == '__main__':
    unittest.main()