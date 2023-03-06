import numpy as np
import random

class Player_AI_Q_Learning():

    def __init__(self, player_char, table=None, epsilon=0.9, reduction=0, discount_factor=1, learning_rate=0.4):
        self.player_char = player_char
        self.is_myturn=0
        self.epsilon = epsilon
        self.reduction = reduction
        self.discount_factor = discount_factor
        self.learning_rate = learning_rate
        self.possible_states = np.array(['empty', 'X', 'O'])

        if table is None:
            self.Q_table= np.zeros((3,3,3,3,3,3,3,3,3,9))
        else:
            # code to load table from disk
            self.load_Q_table(table)

    def play_move(self, board):
        if self.is_myturn:
            previous_state = self.get_state_position(board)
            if random.random() > self.epsilon:
                # greedy move (exploitation)
                move = np.argmax( self.Q_table[tuple(self.get_state_position(board))] )
                row = int(move / 3)
                column = move % 3
                reward, done = board.play_move(self.player_char, (row,column), agent_char=self.player_char)
                self.update_Q_table(board, move, reward, previous_state)
                return reward, done

            else:
                # random move (exploration)
                playable_moves = board.playable_Moves()
                if len(playable_moves) > 0:
                    move = random.randint(0, len(playable_moves) - 1)
                    move_position = playable_moves[move]
                    reward, done = board.play_move(self.player_char, move_position, agent_char=self.player_char)
                    self.update_Q_table(board, move, reward, previous_state)
                    return reward, done

            self.epsilon -= self.reduction


    """
    def play_move(self, board):
        if self.is_myturn:
            playable_moves = board.playable_Moves()
            if len(playable_moves) > 0:
                move = random.randint( 0 , len(playable_moves)-1 )
                move_position = playable_moves[ move ]
                reward, done = board.play_move(self.player_char, move_position)
                return reward, done
        print(self.get_state_position(board))
    """

    def get_state_position(self, board):

        positions = []

        # convert grid into array of dimension access
        for x in range(board.nbrCells):
            for y in range(board.nbrCells):
               positions.append(np.where( self.possible_states == board.grid[x][y] )[0][0])

        return positions

    def update_Q_table(self, board, action, reward, previous_state):

        self.Q_table[tuple(previous_state)][action] += self.learning_rate * (reward + (self.discount_factor *
                                                 ( np.max(self.Q_table[tuple(self.get_state_position(board))])
                                                   - self.Q_table[tuple(previous_state)][action]) ) )


    def save_Q_table(self, filename):
        np.save(filename, self.Q_table)

    def load_Q_table(self, filename):
        self.Q_table = np.load(filename)