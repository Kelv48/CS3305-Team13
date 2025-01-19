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
    
class Protocols:
    class Response:
        NICKNAME = "protocol.request_nickname"
        QUESTIONS = "protocol.questions"
        START = "protocol.start"
        OPPONENT = "protocol.opponent"
        OPPONENT_ADVANCE = 'protocol.opponent_advance'
        ANSWER_VALID = "protocol.answer_valid"
        ANSWER_INVALID = 'protocol.answer_invalid'
        WINNER = "protocol.winner"
        OPPONENT_LEFT = "protocol.opponent_left"

    class Request:
        ANSWER = "protocol.answer"
        NICKNAME = "protocol.send_nickname"
        LEAVE = "protocol.leave"