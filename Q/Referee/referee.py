import sys, os
sys.path.insert(1, os.path.abspath('../../Common'))
from map import GameMap, Tile, Position
from game_state import PlayerInfo, State
from scoring import score_turn
import copy
import signal 
# Represents the Referee compoonent. 
class Referee:
  def __init__(self, playerList, game_state=None, config=None) -> None:
    self.playerList = playerList
    if config: 
       self.game_state = config.initial_state
    if game_state == None:
        player_states = self.create_player_states(playerList)
        self.game_state = State(players=player_states, referee_tiles=None)
    else:
      self.game_state = game_state
    self.observers = []
    self.active_player_eliminated = False

  def attach(self, observer):
     self.observers.append(observer)

  #This function represents a referee. Given an input of players sorted by age in descending order,
  #the referee will start and run a game until a winner(s) is decided or the game otherwise ends.
  #Players are removed for breaking the game rules (a "business logic" bug).
  #raises an exception (a safety bug)
  def run_game_and_return_winners(self):
      self.set_up()
      self.run_game()
      self.notify_winners() 
      return self.game_state.winners(), self.game_state.cheaters()
        

  # Get the states for each player in this playerList
  def create_player_states(self, playerList):
    player_info_objects = []
    for player in playerList:
        player_info = PlayerInfo(player, 0, tile_bag=None)
        player_info_objects.append(player_info)
    return player_info_objects

  # Gives players the initial game map alongside their hand. Returns a dictionary of players with their names as values.
  def set_up(self):
      for player in self.game_state._players:
         self.call_player(player.remote_player.setup, (self.game_state._map, player._tile_bag), player.id)



  # Updates the obserevers with the given gamestate
  def update_observers(self):
    for observer in self.observers:
        observer.add_state(copy.deepcopy(self.game_state))
        if self.game_state.game_end():
          observer.no_more_states()

  # Runs the player interaction function on the arguments pack and eliminates player if there is an exception. 
  def call_player(self, fn, arg, player_id):
    def timeout_handler(num, stack):
      raise TimeoutError()
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(self.config.per_turn)
    try:
        result = fn(*arg)
        return result
    except Exception as exn: # either a TimeoutError or any type of exception thrown by the player. 
      self.game_state.eliminate_by_id(player_id)
      self.active_player_eliminated = True
    finally:
        signal.alarm(0) 
    




  # runs a players turn for a given gamestate
  def run_turn(self, active_info, active_player):
      active_info = self.game_state.extract_data_for_active_player()
      self.active_player_eliminated = False   
      self.update_observers()

      action = self.call_player(active_player.remote_player.takeTurn, [active_info], active_player.id)
      if not self.active_player_eliminated:
        if not self.game_state.check_if_action_is_legal(action):
          self.game_state.eliminate_active_player()

        else: 
          self.game_state.commit_action_to_state(action)
          score = score_turn(self.game_state._map, action, self.game_state.player_placed_all_tiles(), self.config.config_s)
          self.call_player(active_player.add_score, [score], active_player.id)

          if not self.active_player_eliminated:  
            if self.game_state.new_tiles_needed(action) and not self.game_state.game_end():
                self.call_player(active_player.remote_player.newTiles, [active_info.tile_bag], active_player.id)

      self.game_state.complete_turn(active_player)
      
  # Runs a round for a given gamestate
  def run_round(self):
    already_played = set()
    active_player = self.game_state.get_active_player()
    while active_player not in already_played and not self.game_state.game_end():
      active_info = self.game_state.extract_data_for_active_player()
      self.run_turn(active_info, active_player)
      already_played.add(active_player)
      if not self.game_state.game_end():
        active_player = self.game_state.get_active_player()
        

  # Runs a game from the current gamestate until the end of the game.
  def run_game(self):
    while(not self.game_state.game_end()):
        self.run_round()
    self.update_observers()


  # Notifies every player originally signed up (even if they were kicked) whether or not they won
  def notify_winners(self):
      winners = self.game_state.winners()
      for player in self.game_state._players:
          has_won = player.remote_player.name() in winners
          self.call_player(player.remote_player.win, [has_won], player.id)

            
        
  def connect_state_to_players(game_state, players):
      for i in range(len(players)):
          game_state.players[i].remote_player = players[i]
            
              


