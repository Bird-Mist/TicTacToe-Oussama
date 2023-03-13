import random

class Player_AI():
    def __init__(self, player_char):
        self.player_char = player_char
        self.is_myturn=0

    def play_move(self, board):
        if self.is_myturn:
            playable_moves = board.playable_Moves()
            if len(playable_moves) > 0:
                move = random.randint( 0 , len(playable_moves)-1 )
                move_position = playable_moves[ move ]
                rewards, done = board.play_move(self.player_char, move_position)
                return rewards, done, (move_position[0]*board.nbrCells) + move_position[1]
        else:
            return False, False, False
