import random
import numpy as np

print("オセロゲームを実装したコード\n")

class Othello():
    def __init__(self):
        self.b_size = 8
        self.init_cell = '□'
        self.boad = [[self.init_cell for i in range(self.b_size)] for j in range(self.b_size)]
        self.colors = ['●', '▲']
        random.shuffle(self.colors)
        self.player_1 = self.colors.pop()
        self.player_2 = self.colors.pop()
        self.new_cell = {'x': None, 'y': None, 'color': None, 'check': True}
        self.end = True
        self.now_player = self.player_1
        self.reverse_list = None
        self.p1_num = 0
        self.p2_num = 0

    def init_boad(self):
        self.boad[3][3] = self.player_1
        self.boad[4][4] = self.player_1
        self.boad[3][4] = self.player_2
        self.boad[4][3] = self.player_2
        self.calc_each_numbers()


    def print_boad(self):
        print('', end='\t')
        [print(i, end='\t') for i in range(len(self.boad))]
        print('\n\t', '-\t'*8)
        for i, b in enumerate(self.boad):
            print(i, "|", end="\t")
            for j, v in enumerate(b):
                print(v, end="\t")
            print("\n")
        print('\t', '-\t'*8, '\n')
        print("Player1 {}: {} - Player2 {}: {}".format(self.player_1, self.p1_num, self.player_2, self.p2_num))

    def init_new_cell(self):
        self.new_cell = {'x': None, 'y': None, 'color': None, 'check': True}
        self.reverse_list = None
        self.p1_num = 0
        self.p2_num = 0

    def change_player(self):
        if self.now_player == self.player_1:
            self.now_player = self.player_2
        else:
            self.now_player = self.player_1

    def ask_cell(self):
        while self.new_cell['check']:
            print(self.now_player, "を置く位置を選んでください。(Choose the place of", self.now_player, ")")
            print("たての座標を選んでください。(Choose the colum.)")
            cell_y = int(input())
            print("横の座標を選んでください。(Choose the row.)")
            cell_x = int(input())
            if 0 <= cell_y < self.b_size and 0 <= cell_x < self.b_size and self.check_put_cell(cell_y, cell_x):
                self.new_cell = {'y': cell_y, 'x': cell_x, 'color': self.now_player, 'check': False}
            #self.new_cell = {'x': cell_x, 'y': cell_y, 'color': self.now_player, 'check': False} //debug
            else:
                print("----- 指定された場所には置けません。(It doesn't work.)-----")

    def put_cell(self):
        self.boad[self.new_cell['y']][self.new_cell['x']] = self.new_cell['color']
        self.reverse_cells()
        self.calc_each_numbers()
        self.print_boad()
        self.init_new_cell()
        self.change_player()
        return 0

    def reverse_cells(self):
        for ch in self.reverse_list:
            self.boad[ch[0]][ch[1]] = self.new_cell['color']

    def check_put_cell(self, y, x):
        if self.boad[y][x] != self.init_cell:
            print("何も置いていない場所を選択してください。(Choose the empty place.)")
            return False
        elif self.check_reverse(y, x) == []:
            print("1つ以上ひっくり返せる場所を選択してください。(Choose the place you can reverse stones more than one.)")
            return False
        else:
            return True

    def check_reverse(self, y, x):
        """
        """
        reverse_list = []
        boad = self.boad
        boad[y][x] = self.now_player
        check_list = [-1, 0, 1]
        for i in check_list:
            for j in check_list:
                if j == 0 and i == 0:
                    pass
                elif 0 <= y + i < self.b_size and 0 <= x + j < self.b_size:
                    if (boad[y + i][x + j] != boad[y][x]) and (boad[y + i][x + j] != self.init_cell):
                        temp_list = []
                        for k in range(1, self.b_size):
                            temp_y = i * k
                            temp_x = j * k
                            if 0 <= x + temp_x < self.b_size and 0 <= y + temp_y < self.b_size:
                                if boad[y + temp_y][x + temp_x] != boad[y][x] and boad[y + temp_y][x + temp_x] != self.init_cell:
                                    temp_list.append([y + temp_y, x + temp_x])
                                elif boad[y + temp_y][x + temp_x] == boad[y][x]:
                                    for tl in temp_list:
                                        reverse_list.append(tl)

        self.reverse_list = reverse_list
        return reverse_list

    def check_end(self):
        if any(list(map(lambda x: self.init_cell in x, self.boad))):
            pass
        elif self.recursive_check_reverse():
            pass
        else:
            self.end = False

    def recursive_check_reverse(self):
        for i in range(self.b_size):
            for j in range(self.b_size):
                if self.boad[i][j] == self.init_cell:
                    if self.check_reverse(i, j) == []:
                        pass
        end_flag = np.array([self.check_reverse(i, j) for i in range(self.b_size)\
                for j in range(self.b_size) if self.boad[i][j] == self.init_cell ]).size
        return end_flag != 0

    def calc_each_numbers(self):
        p1_num = 0
        p2_num = 0
        for i in range(self.b_size):
            for j in range(self.b_size):
                if self.boad[i][j] == self.player_1:
                    p1_num += 1
                elif self.boad[i][j] == self.player_2:
                    p2_num += 1
        self.p1_num = p1_num
        self.p2_num = p2_num

def main():
    othello = Othello()
    print("ゲームスタート(A Othello game starts.)\n")
    # othello.print_boad()
    othello.init_boad()
    othello.print_boad()

    while othello.end:
        othello.ask_cell()
        othello.put_cell()
        othello.check_end()
    print("It's done.")
if __name__ == '__main__':
    main()