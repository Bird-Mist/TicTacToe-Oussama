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
        opponent_char = self.get_opponent_char(player_char)
        rewards = {player_char: 0, opponent_char: 0}

        if self.grid[position] != 'empty':
            rewards = {player_char: -99999999999999, opponent_char: 0 }
            return rewards, self.checkWinConditions()
        else:
            self.grid[position] = player_char

        winning_character = self.checkWinConditions()
        if winning_character:
            if winning_character == player_char:
                rewards = {player_char: 1, opponent_char: -1}
            else:
                rewards = {player_char: -1, opponent_char: 1}

        return rewards, winning_character

    def reset(self):
        for x in range( self.nbrCells ):
            for y in range( self.nbrCells ):
                self.grid[x][y] = 'empty'


    def get_opponent_char(self, player_char):
        if player_char == 'O':
            return 'X'
        else:
            return 'O'