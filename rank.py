from enum import Enum

class Rank(Enum):
    ACE = 14
    KING = 13
    QUEEN = 12
    JACK = 11
    TEN = 10
    NINE = 9 
    EIGHT = 8
    SEVEN = 7
    SIX = 6
    FIVE = 5 
    FOUR = 4
    THREE = 3
    TWO = 2
    
    #This is for the message headers between client and server 
class Protocols:
    class Response:
        AUTHENTICATION_VALID = "protocol.valid_authentication"     #Used to responded with authentication credentials 
        AUTHENTICATION_INVALID = "protocol.invalid_authentication" #Used to reject client login
        QUESTIONS = "protocol.questions"
        START = "protocol.start"
        OPPONENT = "protocol.opponent"
        OPPONENT_ADVANCE = 'protocol.opponent_advance'
        ANSWER_VALID = "protocol.answer_valid"
        ANSWER_INVALID = 'protocol.answer_invalid'
        WINNER = "protocol.winner"
        OPPONENT_LEFT = "protocol.opponent_left"

    class Request:
        RAISE = "protocol.raise"                                #Used by client to send request to raise the pot
        AUTHENTICATION = "protocol.request_authentication"     #Used to request of auth when client logs in 
        LEAVE = "protocol.leave"                                #Used to send request to leave game 