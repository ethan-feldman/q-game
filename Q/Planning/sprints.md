TO: Professor Matthias Felleisen\
FROM: Ethan Feldman and Moe Thu\
DATE: September 14th, 2023\
SUBJECT: Sprints



# Sprint 1: Base Game Setup

## Goal: 
Implement essential data representations, logic, and game initialization logic as a framework in which the game can run on.

### Details:
- Build out the essential data representation of the game including the board, tiles, and any other necessary objects for the game.
- The board will include the structure and layout of it, and the tile will have certain properties, types, and behaviors associated with it.
- Complete the player-referee interface, defining how to set up players, take turns, and signal that the game is ending.
- Implement game initialization logic, which will include initialization of the board and assigning the first turn.

# Sprint 2: Game Logic and Communication

## Goal: 
Add logic to the communication layer and add game logic for validation of moves and for end-state checking.

### Details:
- Add a communication layer. This will include a referee implementation that will check the player implementations moves to ensure they are legal, and take necessary actions if an illegal move is made.
- Build on the player-referee interface that was made in Sprint 1 to add player communication.
- Implement move logic to ensure players know how to make a move, including validation checks for a move type.
- Add logic for the 'state of the game', including determining when the game has ended and notifying the players when this occurs.

# Sprint 3: Robust Communication and Observers

## Goal: 
Make the communication layer more robust, add observers, and add a database component.

### Details:
- Enhance the communication layer, including checks for ill-formed JSON data, and gracefully handle failures of individual components to ensure the game either can continue or, if necessary, gracefully crash.
- Implement observers, which will include communication between the referee and observers.
- To support the tournament aspect, integrate a database to run many concurrent games.


