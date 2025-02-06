TO: Professor Felleisen

FROM: Jacob Schissel, Ethan Feldman

DATE: 12 October, 2023

SUBJECT: Assignment 4 Design Task

## Player-Referee Protocol

The first interaction between a player and the referee would be the player reaching out to join the game. It would have a method call in a player class that sends relevant player information (age, connection/UID).

The referee would then add said player to the game. Once enough players have joined the game, the referee would start the game and send the player game state data to the first player (as it would be their turn).

In response, a player would have to receive the input, process it with whatever game strategy they may have, and then send a message to the referee describing the turn they would like to take.

When a referee receives this information, the move will be played if valid. Otherwise the player who sent the information will be removed from the game. Once the turn is played (or player removed), the game state will advance to the next turn and the referee will once again send player game state data to the player whose turn is next.

An exception to the above is in the event the game is ended. This is checked at the conclusion of each turn prior to advancing to the next. Once the game is ended, the referee would notify each player with their final placement.
