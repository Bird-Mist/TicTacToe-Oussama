import pygame
from Board import Board
from Board import Player_AI
from Board import Player_AI_Q_Learning
import time


pygame.init()


BLACK= (0,0,0)
WHITE= (255,255,255)

size= (700, 500)
screen=pygame.display.set_mode(size)
board=Board(screen,3)

episodes = 100
epsilon = 0.9
reduction = epsilon / 1000

player1=Player_AI(player_char='X')
player1.is_myturn = 1
player2=Player_AI_Q_Learning(table='Q_Table.npy',player_char='O', epsilon=epsilon, reduction=reduction)

pygame.display.set_caption('Tic Tac Toe')
carryOn= True
clock= pygame.time.Clock()


episode = 0
score = {'O': 0, 'X':0}

while episode < episodes:
    print(episode)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn= False

    # -- game logic --

    # -- drawing logic --
    winner = 0
    while not board.checkWinConditions() and len(board.playable_Moves()) > 0:
        screen.fill(WHITE)
        player1.play_move(board)
        player2.play_move(board)
        board.drawBoard()
        pygame.display.flip()

        # switch turns
        player1.is_myturn = not player1.is_myturn
        player2.is_myturn = not player2.is_myturn

        clock.tick(60)

    winner = board.checkWinConditions()

    if winner:
        score[winner] += 1
    print(score)
    board.reset()
    episode+=1

print(score)
#player2.save_Q_table('Q_table.npy')
pygame.quit()

print('Agent win percentage: ',score['O']/episodes)
print('Percentage of ties: ',(episodes-score['O']-score['X'])/episodes)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print()
