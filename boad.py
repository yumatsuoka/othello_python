# -*- coding: utf-8 -*-

import copy

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