# -*- coding: utf-8 -*-

from player import Player
from player import StaticAIPlayer
from boad import Othello_Boad

def main():
    #### Params ####
    order1 = 0
    order2 = 1
    init_cell = 2
    print("Player1: Choose you or CPU.[you or cpu]")
    mode1 = input()
    if mode1 == "cpu":
        print("Choose the cpu mode.[random, all, comb]")
        level1 = input()
        if level1 == 'all' or level1 == 'comb':
            print("Choose the depth of search.")
            depth1 = int(input())
        else:
            depth1 = 0

    print("Player2: Choose you or CPU.[you or cpu]")
    mode2 = input()
    if mode2 == "cpu":
        print("Choose the cpu mode.[random, all, comb]")
        level2 = input()
        if level2 == 'all' or level2 == 'comb':
            print("Choose the depth of search.(recommend 3 < N < 6)")
            depth2 = int(input())
        else:
            depth2 = 0
    ################

    othello = Othello_Boad(player1=order1, player2=order2, init_cell=init_cell)
    #player1 = Player(mode=mode1, order=order1, init_cell=init_cell, opposite_order=order2)
    #player2 = Player(mode=mode2, order=order2, init_cell=init_cell, opposite_order=order1)
    player1 = StaticAIPlayer(mode=mode1, order=order1, init_cell=init_cell,\
                opposite_order=order2, level=level1, search_depth=depth1)
    player2 = StaticAIPlayer(mode=mode2, order=order2, init_cell=init_cell,\
                opposite_order=order1, level=level2, search_depth=depth2)
    print("A Othello game starts.\n")
    othello.init_boad()
    othello.print_boad()

    while othello.end:
        chosen_cell1 = player1.ask_cell(othello.get_boad())
        othello.set_cell(chosen_cell1)

        chosen_cell2 = player2.ask_cell(othello.get_boad())
        othello.set_cell(chosen_cell2)
        othello.check_end()

if __name__ == '__main__':
    main()