TO: Professor Matthias Felleisen\
FROM: Ethan Feldman and Moe Thu\
DATE: October 4th, 2023\
SUBJECT: player-interface design

## Player Interface Design

To allow each player to have an interface to play the game, a player interface class is created.
Some variables:

- player_id = String # the id of the player that is connected

other methods:

- is_connected(): Returns a boolean value based on whether the player is connected to the interface
- await_connection(int): Await player connection on specified port between 10000 and 60000. Will prompt player for user and password.
- authenticate_password(String): Checks against a SHA256 encrypted password with player username and password
- is_unique(): Raises an exception if player_id is already used in another player-interface class or else return True
- send_turn_information(JSON Object): Sends a JSON object through the TCP connection
- check_turn_information(JSON Object): Raises an exception if the received information is in wrong format
- recieve_turn_action(): Waits for a JSON Object to be streamed in through the TCP connection
- check_valid_turn(): Checks whether the specified action is in valid format, raise an exception if not
- send_to_referee(JSON Object): Sends a JSON object to the referee after validation of action
- disconnect(): disconnects the player
- send_error(String): sends a JSON string message to the player through the TCP connection
