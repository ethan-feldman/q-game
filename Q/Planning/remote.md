To: Professor Felleisen \
From: Ethan Carpenter, Ethan Feldman \
Subject: 8 -- The Observer Design Task 


Gathering Player Protocol:

Start:

    Players ask the referee to join the game: send a JRequestToJoin

Launch of a game (Remote-Proxy Design):

    Referee gives the players JSetupInfo (the players know the game has begun)

End of a game:

    The referee broadcasts to the players that the game has ended by sending a JEndOfGame object.

JSON Data Definition:

JRequestToJoin is an object with 1 field:

{    

“add-player” :     JName

}

    INTERPRETATION describes the player requesting to join the game

JSetupInfo is an object with two fields:

{    “map”    :    JMap

    “tile*”   :     [JTile, …, JTile]


                	}

    INTERPRETATION describes the initially available data to the player of the game. The beginning map as well as the player’s hand.

JEndOfGame is an object with one field:

{

    “won” :   	 “True”|”False”

}

    INTERPRETATION describes whether or not the player is among the winners. True means that the player has won and False means that the player has lost.

JTileBag is an object with one field:

{

    “tiles” :   	 [JTile, …, JTile]

}

    INTERPRETATION describes the tiles in a players hand.

Setting up A Game:

referee 			 ProxyPlayer    		 ProxyReferee   		 Player

 	|	setup(map, bagOfTiles)     	|         	JSetupInfo              	|setup(map, bagOfTiles) |

 	|  —--------------------------------->   | —--------------------------------->  | —--------------------------> |

 	|  				      	|                                            	|   			 	|

 	|  				      	|                                            	|   			 	|

 	|  				      	|                                            	|   			 	|

 	|  				      	|                                            	|   			 	|

Playing Turns:

referee 			 ProxyPlayer    		 ProxyReferee   		 Player

 	|	take-turn(publicState)        	|               	JPub                 	|  take-turn(publicState)   |

 	|  —--------------------------------->   | —--------------------------------->  | —-------------------------->  |

ACTION 1: Pass

 	|  		 Pass    		      	|              	JAction              	|   	 	Pass            	|

 	| ←—---------------------------------- | ←—--------------------------------- | ←—------------------------- |

 	|  				      	|                                            	|                                    	|

 	|  				      	|                                            	|                                        	|

ACTION 1: Replace

 	|  		 Replace   		      	|              	JAction              	|   	 	Replace      	|

 	| ←—---------------------------------- | ←—--------------------------------- | ←—------------------------- |

 	|  				      	|                                            	|                                    	|

 	|  				      	|                                            	|                                        	|

ACTION 1: Extension

 	|  	      	Extension    		      	|              	JAction              	|   	 Extension        	|

 	| ←—---------------------------------- | ←—--------------------------------- | ←—------------------------- |

 	|  				      	|                                            	|                                    	|

 	|  				      	|                                            	|                                        	|

IF: the player asks for REPLACE or EXTENSION, the referee completes the turn:

 	|   new_tiles(bagOfTiles)          	|                	JTileBag         	| new_tiles(bagOfTiles 	|

 	|  —--------------------------------->   | —--------------------------------->  | —-------------------------->  |

Ending the game:

referee 			 ProxyPlayer    		 ProxyReferee   		 Player

 	|        	win(boolean)             	|  	JEndOfGame                	|  win(boolean)            	|

 	|  —--------------------------------->  | —--------------------------------->  | —-------------------------->  |

