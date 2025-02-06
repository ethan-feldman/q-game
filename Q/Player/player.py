from strategy import Dag, Ldasg, NonAdjacentCoordinate, NoFit, NotALine, TileNotOwned, BadAskForTiles

class Player:
    '''
    Creates a player of a given name and age -- name is assumed to be unique per specs
    Name is a string and age is a natural number
    '''
    def __init__(self, name: str, age: int, strategy):
        self._name = name
        self._age = age
        self._strategy = strategy
        self._map = None
        self._tiles = None

    '''
    returns the player name as a string.
    '''
    def name(self):
        return self._name
    
    def setup(self, map, tiles):
        self._map = map
        self._tiles = tiles

    '''
    Returns the action of a move that the player would like to make
    '''
    def takeTurn(self, publicState):
        return self._strategy.iterate_strategy(publicState)

    

    '''
    Sets the player's hand of tiles to the given set of tiles
    '''
    def newTiles(self, tile_set):
        self._tiles = tile_set

    '''
    If the given boolean is true, this player has won! 
    '''
    def win(self, w: bool):
        pass 

    ''' 
    Changes the strategy being utilized by the player.
    '''
    def change_strategy(self, strategy):
        self._strategy = strategy

    def __str__(self):
        return "Player name: " + str(self._name)
    

class PlayerBuilder:
    def __init__(self):
        self.name = None
        self.age = 0
        self.strat = None
        self.cheat = None


    def set_name(self, name):
        self.name = name
        return self

    def set_age(self, age):
        self.age = age
        return self
    
    def set_strat(self, strat):
        self.strat = strat
        return self 
    
    def set_cheat(self, cheat):
        self.cheat = cheat
        return self
    
    def build(self):
        if self.cheat == None:
            return Player(self.name, self.age, self.strat)
        else:
            if self.cheat == 'non-adjacent-coordinate':
                return Player(self.name, self.age, NonAdjacentCoordinate(self.strat))
            elif self.cheat == 'tile-not-owned':
                return Player(self.name, self.age, TileNotOwned(self.strat))
            elif self.cheat == 'not-a-line':
                return Player(self.name, self.age, NotALine(self.strat))
            elif self.cheat == 'bad-ask-for-tiles':
                return Player(self.name, self.age, BadAskForTiles(self.strat))
            else:
                return Player(self.name, self.age, NoFit(self.strat))
    
    

        
from strategy import Dag, Ldasg, NonAdjacentCoordinate, NoFit, NotALine, TileNotOwned, BadAskForTiles
import time

class DosPlayer(Player):
    '''
    Creates a player of a given name and age -- name is assumed to be unique per specs
    Name is a string and age is a natural number
    '''
    def __init__(self, name: str, age: int, strategy, exn: str, count: int):
        super().__init__(name, age, strategy)
        self._exn = exn
        self._count = count

    '''
    returns the player name as a string.
    '''
    def name(self):
        self.timeout_check('name')
        return super().name()
    
    def setup(self, map, tiles):
        self.timeout_check('setup')
        return super().setup(map, tiles)

    '''
    Returns the action of a move that the player would like to make
    '''
    def takeTurn(self, publicState):
        self.timeout_check('take-turn')
        return super().takeTurn(publicState)
    
    '''
    Sets the player's hand of tiles to the given set of tiles
    '''
    def newTiles(self, tile_set):
        self.timeout_check('new-tiles')
        return super().newTiles(tile_set)

    '''
    If the given boolean is true, this player has won! 
    '''
    def win(self, w: bool):
        self.timeout_check('win')
        return super().win(w)

    ''' 
    Changes the strategy being utilized by the player.
    '''
    def change_strategy(self, strategy):
        self._strategy = strategy
    
    def timeout_check(self, exn):
        if self._exn == exn:
            if self._count == 1:
                time.sleep(100)
            else:
                self._count = self._count - 1
            

    def __str__(self):
        return "Player name: " + str(self._name)
    
class DosPlayerBuilder():
    def __init__(self):
        self.name = None
        self.age = 0
        self.strat = None
        self.exn = None
        self.count = None

    def set_name(self, name):
        self.name = name
        return self

    def set_age(self, age):
        self.age = age
        return self
    
    def set_strat(self, strat):
        self.strat = strat
        return self 
    
    def set_exn(self, exn):
        self.exn = exn
        return self
    def set_count(self, count):
        self.count = count
        return self

    def build(self):
            return DosPlayer(self.name, self.age, self.strat, self.exn, self.count)


class ExceptionPlayer(Player):

    '''
    Creates a player of a given name and age -- name is assumed to be unique per specs
    Name is a string and age is a natural number
    '''
    def __init__(self, name: str, age: int, strategy, exn: str):
        super().__init__(name, age, strategy)
        self._map = None
        self._tiles = None
        self._exn = exn

    '''
    returns the player name as a string.
    '''
    def name(self):
        return super().name()
    
    def setup(self, map, tiles):
        self.should_throw_exception('setup')
        super().setup(map, tiles)

    '''
    Returns the action of a move that the player would like to make
    '''
    def takeTurn(self, publicState):
        self.should_throw_exception('take-turn')
        super().takeTurn(publicState)

    '''
    Sets the player's hand of tiles to the given set of tiles
    '''
    def newTiles(self, tile_set):
        self.should_throw_exception('new-tiles')
        super().newTiles(tile_set)

    '''
    If the given boolean is true, this player has won! 
    '''
    def win(self, w: bool):
        self.should_throw_exception('win')

    ''' 
    Changes the strategy being utilized by the player.
    '''
    def change_strategy(self, strategy):
        self._strategy = strategy

    def __str__(self):
        return "Player name: " + str(self._name)
    
    def should_throw_exception(self, exn):
        if self._exn == exn:
            raise Exception(self._exn)
    

class ExceptionPlayerBuilder:
    def __init__(self):
        self.name = None
        self.age = 0
        self.strat = None
        self.exn = None
        self.count = None

    def set_name(self, name):
        self.name = name
        return self

    def set_age(self, age):
        self.age = age
        return self
    
    def set_strat(self, strat):
        self.strat = strat
        return self 
    
    def set_exn(self, exn):
        self.exn = exn
        return self

    def build(self):
            return ExceptionPlayer(self.name, self.age, self.strat, self.exn)

        
        




        