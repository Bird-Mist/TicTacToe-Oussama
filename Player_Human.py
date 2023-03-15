import pygame
import numpy as np

class Player_Human():

    def __init__(self, player_char):
        self.player_char = player_char
        self.is_myturn = 0
        self.possible_states = np.array(['empty', 'X', 'O'])

    def play_move(self, board):
        if self.is_myturn:
            rewards = {'O': 0, 'X':0}
            done = False
            action = False
            played_move = False
            while not played_move:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_KP7:
                            rewards, done = board.play_move(self.player_char, (0,0 ))
                            action = 0
                            played_move = True
                        if event.key == pygame.K_KP8:
                            rewards, done = board.play_move(self.player_char, (0,1 ))
                            action = 1
                            played_move = True
                        if event.key == pygame.K_KP9:
                            rewards, done = board.play_move(self.player_char, (0,2 ))
                            action = 2
                            played_move = True
                        if event.key == pygame.K_KP4:
                            rewards, done = board.play_move(self.player_char, (1,0 ))
                            action = 3
                            played_move = True
                        if event.key == pygame.K_KP5:
                            rewards, done = board.play_move(self.player_char, (1,1 ))
                            action = 4
                            played_move = True
                        if event.key == pygame.K_KP6:
                            rewards, done = board.play_move(self.player_char, (1,2 ))
                            action = 5
                            played_move = True
                        if event.key == pygame.K_KP1:
                            rewards, done = board.play_move(self.player_char, (2,0 ))
                            action = 6
                            played_move = True
                        if event.key == pygame.K_KP2:
                            rewards, done = board.play_move(self.player_char, (2,1 ))
                            action = 7
                            played_move = True
                        if event.key == pygame.K_KP3:
                            rewards, done = board.play_move(self.player_char, (2,2 ))
                            action = 8
                            played_move = True

            return rewards, done, action

        else:
            return False, False, False

    def get_state_position(self, board):

        positions = []

        # convert grid into array of dimension access
        for x in range(board.nbrCells):
            for y in range(board.nbrCells):
                positions.append(np.where(self.possible_states == board.grid[x][y])[0][0])

        return positions

    def update_Q_table_last_action(self, board,rewards,previous_state):
        # dummy function
        ...

    def save_Q_table(self, filename):
        #dummy function
        ...