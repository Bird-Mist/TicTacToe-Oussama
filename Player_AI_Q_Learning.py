import numpy as np
import random

class Player_AI_Q_Learning():

    def __init__(self, player_char, table=None, epsilon=0.9,min_epsilon = 0.2, reduction=0, discount_factor=0.01, learning_rate=0.2):
        self.player_char = player_char
        self.is_myturn=0
        self.epsilon = epsilon
        self.min_epsilon = min_epsilon
        self.reduction = reduction
        self.discount_factor = discount_factor
        self.learning_rate = learning_rate
        self.possible_states = np.array(['empty', 'X', 'O'])
        self.latest_action = None
        self.latest_state = [0,0,0,0,0,0,0,0,0]

        if table is None:
            self.Q_table= np.zeros((3,3,3,3,3,3,3,3,3,9))
        else:
            # code to load table from disk
            self.load_Q_table(table)

    def play_move(self, board):
        if self.is_myturn:
            previous_state = self.get_state_position(board)
            self.latest_state = previous_state
            if random.random() > self.epsilon:
                # greedy move (exploitation)

                move = np.argmax( self.Q_table[tuple(self.get_state_position(board))] )
                self.latest_action = move
                row = int(move / 3)
                column = move % 3
                rewards, done = board.play_move(self.player_char, (row,column))
                self.update_Q_table(board=board, action=move, rewards=rewards, previous_state=previous_state)
                return rewards, done, move

            else:
                # random move (exploration)
                playable_moves = board.playable_Moves()
                if len(playable_moves) > 0:
                    move = random.randint(0, len(playable_moves) - 1)
                    move_position = playable_moves[move]
                    self.latest_action = (move_position[0]*board.nbrCells) + move_position[1]
                    reward, done = board.play_move(self.player_char, move_position)
                    self.update_Q_table(board, (move_position[0]*board.nbrCells) + move_position[1], reward, previous_state)
                    return reward, done, (move_position[0]*board.nbrCells) + move_position[1]

            if self.epsilon > self.min_epsilon:
                self.epsilon -= self.reduction

        else:
            return None, None, None


    def get_state_position(self, board):

        positions = []

        # convert grid into array of dimension access
        for x in range(board.nbrCells):
            for y in range(board.nbrCells):
               positions.append(np.where( self.possible_states == board.grid[x][y] )[0][0])

        return positions

    def update_Q_table(self, board, action, rewards, previous_state):
        reward = rewards[self.player_char]
        character = self.player_char
        state_before = np.copy(self.Q_table[tuple(previous_state)])
        self.Q_table[tuple(previous_state)][action] += (self.learning_rate * (reward + (self.discount_factor * np.max(self.Q_table[tuple(self.get_state_position(board))])) - self.Q_table[tuple(previous_state)][action]))
        state_after = np.copy(self.Q_table[tuple(previous_state)])
        #print()
    def update_Q_table_last_action(self, board,rewards,previous_state):
        reward = rewards[self.player_char]
        state_before = np.copy(self.Q_table[tuple(previous_state)])
        #print()
        self.Q_table[tuple(self.latest_state)][self.latest_action] += (self.learning_rate * (
                    reward + (self.discount_factor * np.max(self.Q_table[tuple(self.get_state_position(board))])) -
                    self.Q_table[tuple(self.latest_state)][self.latest_action]))

        state_after = np.copy(self.Q_table[tuple(previous_state)])
        #print()
    def save_Q_table(self, filename):
        np.save(filename, self.Q_table)

    def load_Q_table(self, filename):
        self.Q_table = np.load(filename)