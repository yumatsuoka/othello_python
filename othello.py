#from othello import Othello
import random
import copy
import numpy as np


class Player():
    def __init__(self, mode, order, init_cell, opposite_order):
        self.mode = mode
        self.order = order
        self.init_cell = init_cell
        self._order = opposite_order
        self.colors = ['●', '▲', '□']

    def ask_cell(self, boad):
        if self.recursive_check_reverse(boad) and any(list(map(lambda x: self.init_cell in x, boad))):
            if self.mode == 'cpu':
                chosen_cell = self.random_answer(boad)
            else:
                chosen_cell = self.ask_human(boad)
        else:
            print("Skip Player[", self.order+1, "].")
            chosen_cell = {'order': self.order, 'pass': True}
        return chosen_cell

    def ask_human(self, boad):
        boad_size = len(boad)
        cell_available = True
        while cell_available:
            print("Player[", self.order, "] choose the cell.")
            print("Choose the colum.")
            cell_y = int(input())
            print("Choose the row.")
            cell_x = int(input())

            if 0 <= cell_y < boad_size and 0 <= cell_x < boad_size:
                reverses = self.check_reverse(cell_y, cell_x, boad)
                if boad[cell_y][cell_x] != self.init_cell:
                    print("Choose the empty cells.")
                elif reverses == []:
                    print("Choose the place you can reverse stones more than one.")
                else:
                    new_cell = {'y': cell_y, 'x': cell_x, 'order': self.order, 'reverses': reverses, 'pass': False}
                    cell_available = False
            else:
                print("----- The choice doesn't work.-----")

        return new_cell

    def random_answer(self, boad):
        print("Player{} CPU puts a stone.".format(self.order+1))
        boad_size = len(boad)
        available_cells = []
        for y in range(boad_size):
            for x in range(boad_size):
                if boad[y][x] == self.init_cell:
                    reverses = self.check_reverse(y, x, boad)
                    if reverses != []:
                        available_cells.append({'y': y, 'x': x, 'order': self.order, 'reverses': reverses, 'pass': False})
        new_cell = random.choice(available_cells)
        return new_cell

    def check_reverse(self, y, x, _boad):
        boad = copy.deepcopy(_boad)
        boad_size = len(boad)
        reverse_list = []
        boad[y][x] = self.order
        check_list = [-1, 0, 1]
        for i in check_list:
            for j in check_list:
                if i == 0 and j == 0:
                    continue
                elif 0 <= y + i < boad_size and 0 <= x + j < boad_size:
                    if boad[y + i][x + j] == self._order:
                        temp_list = []
                        for k in range(1, boad_size):
                            temp_y = i * k
                            temp_x = j * k
                            if 0 <= y + temp_y < boad_size and 0 <= x + temp_x < boad_size:
                                if boad[y + temp_y][x + temp_x] == self._order:
                                    temp_list.append({'y': y + temp_y, 'x': x + temp_x})
                                elif boad[y + temp_y][x + temp_x] == self.order:
                                    for tl in temp_list:
                                        reverse_list.append(tl)
                                    temp_list = []
                                    break
                                elif boad[y + temp_y][x + temp_x] == self.init_cell:
                                    temp_list = []
                                    break
                                else:
                                    exit()
        return reverse_list

    def recursive_check_reverse(self, boad):
        boad_size = len(boad)
        end_flag = 0
        for y in range(boad_size):
            for x in range(boad_size):
                if boad[y][x] == self.init_cell:
                    if self.check_reverse(y, x, boad) == []:
                        pass
                    else:
                        end_flag += 1
        return end_flag


class Othello_Boad():
    def __init__(self, player1, player2, init_cell):
        self.b_size = 8
        self.init_cell = init_cell
        self.boad = [[self.init_cell for y in range(self.b_size)] for x in range(self.b_size)]
        self.colors = ['●', '▲', '□']
        self.end = True
        self.player1 = player1
        self.player2 = player2
        self.p1_num = 0
        self.p2_num = 0

    def init_boad(self):
        self.boad[3][3] = self.player1
        self.boad[4][4] = self.player1
        self.boad[3][4] = self.player2
        self.boad[4][3] = self.player2
        self.calc_each_numbers()

    def get_boad(self):
        return self.boad

    def print_boad(self):
        print('', end='\t')
        [print(i, end='\t') for i in range(len(self.boad))]
        print('\n\t', '-\t'*8)
        for i, b in enumerate(self.boad):
            print(i, "|", end="\t")
            for v in b:
                print(self.colors[v], end="\t")
            print("\n")
        print('\t', '-\t'*8, '\n')
        print("Player1 {}: {} - Player2 {}: {}".format(self.colors[self.player1], self.p1_num, self.colors[self.player2], self.p2_num))

    def set_cell(self, chosen_cell):
        if chosen_cell['pass']:
            print("Don't put any stones@Boad_class")
            pass
        else:
            self.boad[chosen_cell['y']][chosen_cell['x']] = chosen_cell['order']
            for cell in chosen_cell['reverses']:
                self.boad[cell['y']][cell['x']] = chosen_cell['order']
            self.calc_each_numbers()
            self.print_boad()

    def check_reverse(self, y, x, order):
        reverse_list = []
        # 関数への引数は参照渡しなので、deepcopu()をしないと思ってない処理が起きる。
        boad = copy.deepcopy(self.boad)
        boad[y][x] = order
        check_list = [-1, 0, 1]
        for i in check_list:
            for j in check_list:
                if j == 0 and i == 0:
                    continue
                elif 0 <= y + i < self.b_size and 0 <= x + j < self.b_size:
                    if (boad[y + i][x + j] != boad[y][x]) and (boad[y + i][x + j] != self.init_cell):
                        temp_list = []
                        for k in range(1, self.b_size):
                            temp_y = i * k
                            temp_x = j * k
                            if 0 <= x + temp_x < self.b_size and 0 <= y + temp_y < self.b_size:
                                if boad[y + temp_y][x + temp_x] != boad[y][x] and boad[y + temp_y][x + temp_x] != self.init_cell:
                                    temp_list.append({'y': y + temp_y, 'x': x + temp_x})
                                elif boad[y + temp_y][x + temp_x] == boad[y][x]:
                                    for tl in temp_list:
                                        reverse_list.append(tl)
                                    break
                                elif boad[y + temp_y][x + temp_x] == self.init_cell:
                                    temp_list = []
                                    break
                                else:
                                    exit()

        return reverse_list

    def check_end(self):
        if any(list(map(lambda x: self.init_cell in x, self.boad))) and self.recursive_check_reverse():
                pass
        else:
            self.end = False
            print("The game is over.")
            print("Score of Player1: {} \t Sore of Player2: {}".format(self.p1_num, self.p2_num))
            if self.p2_num < self.p1_num:
                print("Player1 win!")
            elif self.p1_num < self.p2_num:
                print("Player2 win!")
            else:
                print("Draw!")

    def recursive_check_reverse(self):
        end_flag = 0
        for y in range(self.b_size):
            for x in range(self.b_size):
                if self.boad[y][x] == self.init_cell:
                    if self.check_reverse(y, x, self.player2) == []:
                        pass
                    else:
                        end_flag += 1
        return end_flag

    def calc_each_numbers(self):
        p1_num = 0
        p2_num = 0
        for y in range(self.b_size):
            for x in range(self.b_size):
                if self.boad[y][x] == self.player1:
                    p1_num += 1
                elif self.boad[y][x] == self.player2:
                    p2_num += 1

        self.p1_num = p1_num
        self.p2_num = p2_num

def main():
    #### Params ####
    order1 = 0
    order2 = 1
    init_cell = 2
    print("Player1: Choose you or CPU.[you or cpu]")
    mode1 = input()
    print("Player2: Choose you or CPU.[you or cpu]")
    mode2 = input()
    ################

    othello = Othello_Boad(player1=order1, player2=order2, init_cell=init_cell)
    player1 = Player(mode=mode1, order=order1, init_cell=init_cell, opposite_order=order2)
    player2 = Player(mode=mode2, order=order2, init_cell=init_cell, opposite_order=order1)
    print("A Othello game starts.\n")
    othello.init_boad()
    othello.print_boad()

    while othello.end:
        chosen_cell1 = player1.ask_cell(othello.get_boad())
        othello.set_cell(chosen_cell1)
        #othello.check_end(chosen_cell1)

        chosen_cell2 = player2.ask_cell(othello.get_boad())
        othello.set_cell(chosen_cell2)
        othello.check_end()

if __name__ == '__main__':
    main()