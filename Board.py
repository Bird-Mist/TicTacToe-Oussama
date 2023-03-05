import pygame
import random
import numpy as np
from itertools import product
BLACK= (0,0,0)
WHITE= (255,255,255)

class Board:
    def __init__(self,screen, nbrCells):
        self.nbrCells = nbrCells
        ##self.grid= [['empty'] * nbrCells] * nbrCells
        self.grid = []
        self.turn = round(random.randint(0,1))
        self.over = 0
        self.screen= screen

        for y in range(self.nbrCells):
            self.grid.append([])
            for x in range(self.nbrCells):
                self.grid[y].append('empty')

        self.grid= np.array(self.grid)
        self.gridWidth = 360 / nbrCells
        self.gridHeight = 360 / nbrCells

    def drawCells(self):
        for y in range(self.nbrCells):
            for x in range(self.nbrCells):
                if (self.grid[y][x] == 'O'):
                    pygame.draw.circle(self.screen, BLACK, ( (x * self.gridWidth) + self.gridWidth / 2, (y * self.gridHeight) + self.gridHeight / 2),
                           radius=int(0.3 * self.gridHeight), width=1 )
                if (self.grid[y][x] == 'X'):

                    pygame.draw.line(self.screen, BLACK, ((x * self.gridWidth) + int(0.2 * self.gridWidth),
                         (y * self.gridHeight) + 0.2 * self.gridHeight), (((x + 1) * self.gridWidth) - 0.2 * self.gridWidth,
                         ((y + 1) * self.gridHeight) - 0.2 * self.gridHeight), width=1)

                    pygame.draw.line(self.screen, BLACK, ((x * self.gridWidth) + int(0.2 * self.gridWidth),
                         ((y + 1) * self.gridHeight) - 0.2 * self.gridHeight), (((x + 1) * self.gridWidth) - 0.2 * self.gridWidth,
                         (y * self.gridHeight) + 0.2 * self.gridHeight) , width=1)

    def checkWinConditions(self):
        # rows
        if self.grid[0][0] == self.grid[0][1] == self.grid[0][2] != 'empty':
            self.over = 1
            return self.grid[0][0]
        if self.grid[1][0] == self.grid[1][1] == self.grid[1][2] != 'empty':
            self.over = 1
            return self.grid[1][0]
        if self.grid[2][0] == self.grid[2][1] == self.grid[2][2] != 'empty':
            self.over = 1
            return self.grid[2][0]

        # diagonal
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != 'empty':
            self.over = 1
            return self.grid[0][0]

        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != 'empty':
            self.over = 1
            return self.grid[0][2]

        # columns
        if self.grid[0][0] == self.grid[1][0] == self.grid[2][0] != 'empty':
            self.over = 1
            return self.grid[0][0]
        if self.grid[0][1] == self.grid[1][1] == self.grid[2][1] != 'empty':
            self.over = 1
            return self.grid[0][1]
        if self.grid[0][2] == self.grid[1][2] == self.grid[2][2] != 'empty':
            self.over = 1
            return self.grid[0][2]

        return False

    def drawBoard(self):
        for y in range(self.nbrCells):
            for x in range(self.nbrCells):
                pygame.draw.rect(self.screen, BLACK,pygame.Rect(x * self.gridWidth, y * self.gridHeight, self.gridWidth, self.gridHeight) , width=1)

        self.drawCells()


    def playable_Moves(self):

        # list of tuples indicating the playable moves
        playable_moves=[]
        for index, cell_value in np.ndenumerate(self.grid):
            if cell_value == 'empty':
                playable_moves.append(index)

        return playable_moves


    def play_move(self, player_char, position):
        reward = 0

        winning_character = self.checkWinConditions()
        if winning_character:
            if winning_character == player_char:
                reward = 1
            else:
                reward = -1

        if self.grid[position] != 'empty':
            reward = -9999
        else:
            self.grid[position] = player_char

        return reward, winning_character

    def reset(self):
        for x in range( self.nbrCells ):
            for y in range( self.nbrCells ):
                self.grid[x][y] = 'empty'

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
                reward, done = board.play_move(self.player_char, move_position)
                return reward, done

class Player_AI_Q_Learning():

    def __init__(self, player_char, table=None, epsilon=0.9, reduction=0, discount_factor=1, learning_rate=0.3):
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
            # TODO code to load table from disk here
            self.load_Q_table(table)

    def play_move(self, board):
        if self.is_myturn:
            previous_state = self.get_state_position(board)
            if random.random() > self.epsilon:
                # greedy move (exploitation)
                move = np.argmax( self.Q_table[tuple(self.get_state_position(board))] )
                row = int(move / 3)
                column = move % 3
                reward, done = board.play_move(self.player_char, (row,column))
                self.update_Q_table(board, move, reward, previous_state)
                return reward, done

            else:
                # random move (exploration)
                playable_moves = board.playable_Moves()
                if len(playable_moves) > 0:
                    move = random.randint(0, len(playable_moves) - 1)
                    move_position = playable_moves[move]
                    reward, done = board.play_move(self.player_char, move_position)
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