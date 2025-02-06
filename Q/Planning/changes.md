TO: Professor Felleisen\
FROM: Ethan Feldman, Jacob Schissel \
Subject: 7 – The Clean Up



## Changing bonus points and allowing additional players:

Difficulty: 1.

Changing bonus points would require an update to the static constant in our scoring file. Our implementation does not impose a restriction on the number of players participating and as such allowing more players would be trivial.


## Adding wildcard tiles: 

Difficulty: 3.

Adding wildcard tiles would require changes to the tile class. In our enumerations of shape and color we would need to add a ‘wildcard’. We also would need to change the comparison of tiles which is currently set to the lexicographic ordering described in the specs. The most difficult aspect would be addressing strategy and how it handles these tiles. Lastly, scoring may have to be changed specifically in how a Q is calculated if the wildcard remains ‘wild’ once it has been placed.


## Imposing restrictions that enforce Qwirkle rules instead of Q rules: 

Difficulty: 4. 

We would need to change the way in which we set up the ordering of players because it is specified by whichever player has the greatest number of tiles that share an attribute - in the case of a tie the older player starts. In addition, there must be an extra restriction set with the strategy that all tiles placed must share either shape or color from a player’s hand. Although this would be a less involved change, we would need to change the exchange function object so you can exchange only a portion of your hand. The placements would need to be changed in three ways. First, a line must conserve the same maintained attribute throughout. Secondly, a line cannot contain two of the same type of tile. Lastly, a line cannot exceed six tiles. 
