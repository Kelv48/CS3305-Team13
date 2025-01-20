    
#This is for the message headers between client and server 
class Protocols:
    class Response:
        AUTHENTICATION_VALID = 'protocol.valid_authentication'     #Used to responded with authentication credentials 
        AUTHENTICATION_INVALID = 'protocol.invalid_authentication' #Used to reject client login
        PLAYER_CARDS = 'protocol.player_card'                      #Used to assign players hand 
        START = 'protocol.start'                                   #Used to tell client that its there turn 
        OPPONENT = 'protocol.opponent'                             #Used to update other clients of an opponents move
        WINNER = 'protocol.winner'                                 #Used to reveal the winner of the round 
        OPPONENT_LEFT = 'protocol.opponent_left'                   #Used to tell client that another player has left the game

    class Request:
        RAISE = 'protocol.raise'                                #Used by client to send request to raise the pot
        CHECK = 'protocol.check'
        FOLD = 'protocol.fold'
        CALL = 'protocol.call'
        CREATE_GAME = 'protocol.request_create_game'
        JOIN_GAME = 'protocol_request_join_game'
        AUTHENTICATION = 'protocol.request_authentication'      #Used to request of auth when client logs in 
        LEAVE = 'protocol.leave'                                #Used to send request to leave game 