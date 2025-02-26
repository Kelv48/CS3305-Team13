    
#This is for the message headers between client and server 
class Protocols:
    class Response:
        AUTHENTICATION_VALID = 'protocol.valid_authentication'     #Used to responded with authentication credentials 
        AUTHENTICATION_INVALID = 'protocol.invalid_authentication' #Used to reject client login
        PLAYER_CARDS = 'protocol.player_card'                      #Used to assign players hand 
        START = 'protocol.start'                                   #Used to tell client that its there turn 
        TURN = 'protocol.turn'
        OPPONENT = 'protocol.opponent'                             #Used to update other clients of an opponents move
        WINNER = 'protocol.winner'                                 #Used to reveal the winner of the round 
        OPPONENT_LEFT = 'protocol.opponent_left'                   #Used to tell client that another player has left the game 
        REDIRECT = 'protocol.redirect'                             #Used to tell client to connect to a different port
        SESSION_ID = 'protocol.sessionID'                          #Used to assign client a new sessionID for their game given to the client that created the game 
        FORCE_START = 'protocol.forceStart'                        #Used to alert clients of a change in the force start vote
        LOBBY_UPDATE = 'protocol.lobbyUpdate'                      #Used to update client with new info about the amount of players in lobby
        ERROR = 'protocol.error'                                   #Used to tell client that an error has occurred 
        PLAYER_ID = 'protocol.playerID'                            #Used to assign an id to client to track what player they are i.e. 1 → player 1



    class Request:
        RAISE = 'protocol.raise'                                        #Used by client to send request to raise the pot
        CHECK = 'protocol.check'
        FOLD = 'protocol.fold'
        CALL = 'protocol.call'
        CREATE_GAME = 'protocol.request_create_game'                    #Used by client to join a game
        JOIN_GAME = 'protocol.request_join_game'                        #Used by client to create a game 
        START_GAME_EARLY_VOTE = 'protocol.request_start_game_early'
        AUTHENTICATION = 'protocol.request_authentication'              #Used to request of auth when client logs in 
        CREATE_ACCOUNT = 'protocol.request_create_account'              #Used to create an account, which is stored in DB 
        LOGOUT = 'protocol.request_logout'                              #Used by client to log out
        LEAVE = 'protocol.request_leave'                                #Used to send request to leave game 
        LIST_OF_GAMES = 'protocol.request_list_of_games'                #Used to request for a list of games
        INITIALISE = 'protocol.initialise'                               
        

