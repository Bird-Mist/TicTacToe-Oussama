import pygame
from Board import Board
from Player_AI import Player_AI
from Player_AI_Q_Learning import Player_AI_Q_Learning
from Player_Human import Player_Human
import time


pygame.init()


BLACK= (0,0,0)
WHITE= (255,255,255)

size= (700, 500)
screen=pygame.display.set_mode(size)
board=Board(screen,3)

episodes = 100
epsilon = 0
reduction = epsilon / episodes

player1 = Player_AI_Q_Learning(table='Q_table_X.npy', player_char='X', epsilon=epsilon, reduction=reduction)
player1.is_myturn = 1
player2 = Player_AI_Q_Learning(table='Q_table_O.npy', player_char='O', epsilon=epsilon, reduction=reduction)

#player1 = Player_Human(player_char='X')
player2 = Player_Human(player_char='O')

pygame.display.set_caption('Tic Tac Toe')
carryOn= True
clock= pygame.time.Clock()


episode = 0
score = {'O': 0, 'X':0}


while episode < episodes:

    print(episode)
    if episode % 1000 == 0:
        player1.save_Q_table('Q_table_X.npy')
        player2.save_Q_table('Q_table_O.npy')
        print('Model checkpoint saved')
    # -- game logic --

    # -- drawing logic --
    winner = 0
    while not board.checkWinConditions() and len(board.playable_Moves()) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carryOn = False
        screen.fill(WHITE)

        previous_state = player1.get_state_position(board)
        rewards, done, action = player1.play_move(board)


        if(action != False):
            player2.update_Q_table_last_action(board, rewards, previous_state)

        rewards, done, action = player2.play_move(board)

        if(action != False):
            player1.update_Q_table_last_action(board, rewards, previous_state)

        board.drawBoard()
        pygame.display.flip()

        # switch turns
        player1.is_myturn = not player1.is_myturn
        player2.is_myturn = not player2.is_myturn
        #time.sleep(0.6)
        clock.tick(60)



    winner = board.checkWinConditions()

    if winner:
        score[winner] += 1
    print(score)
    board.reset()
    episode+=1

print(score)


pygame.quit()

print('Agent win percentage: ',score['O']/episodes)
print('Percentage of ties: ',(episodes-score['O']-score['X'])/episodes)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print()
