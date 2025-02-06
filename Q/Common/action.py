from abc import ABC, abstractmethod

'''
Represents an action that a player may take on its turn. As such, an action can be either a pass, an exchange, or
a place. An extends also includes a set of placements which is a list of tuples (Position, Tile) where the first 
item in the list is the first tile to be placed.
'''

class Action(ABC):
    def __init__(self) -> None:
        pass 
    '''
    Returns a list where the first element contains a string of the class type
    and the second element includes any relevant information for making said action
    '''
    @abstractmethod
    def action(self):
        pass


class Pass(Action):
    def __init__(self) -> None:
        super().__init__()
        self.actionString = 'pass'
    def action(self):
        pass

class Exchange(Action):
    def __init__(self) -> None:
        super().__init__()
        self.actionString = 'exchange'
    def action(self):
        pass

class Place(Action):
    def __init__(self, placements) -> None:
        super().__init__()
        self.placements = placements
        self.actionString = 'place'
        
    def action(self):
        return self.placements

    def __str__(self):
        return str(self.placements)