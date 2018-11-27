# -*- coding: utf-8 -*-

import random
import copy

from func import calc_linescores, calc_totalboad_scores

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
                chosen_cell = self.random_ai_answer(boad)
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

    def random_ai_answer(self, boad):
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


class StaticAIPlayer(Player):
    def __init__(self, mode, order, init_cell, opposite_order, level='all', search_depth=3):
        super().__init__(mode, order, init_cell, opposite_order)
        self.level = level
        self.search_depth = search_depth
        self.calc_score = calc_totalboad_scores if self.level == 'all'\
                            else ( calc_linescores if self.level == 'comb' else None)

    def ask_cell(self, boad):
        if self.recursive_check_reverse(boad) and any(list(map(lambda x: self.init_cell in x, boad))):
            if self.mode == 'cpu':
                if self.level == 'random':
                    chosen_cell = self.random_ai_answer(boad)
                elif self.level == 'all' or self.level == 'comb':
                    chosen_cell = self.static_ai_answer(boad)
                else:
                    #exit()
                    print("hogeeee")
            else:
                chosen_cell = self.ask_human(boad)
        else:
            print("Skip Player[", self.order+1, "].")
            chosen_cell = {'order': self.order, 'pass': True}
        return chosen_cell

    def static_ai_answer(self, boad):
        node = False # if node == False, the node means MAX-node.
        chosen_cell = self.calc_minmax(copy.deepcopy(boad), node, self.search_depth)
        #chosen_cell = self.calc_minmax(boad, node, self.search_depth) #except deepcopy
        return chosen_cell

    def calc_minmax(self, boad, node, itr):
        if itr == 0:
            return self.calc_score(boad, self.order, self._order)

        if node:
            # 最小化する場合の分岐
            local_order = self._order
            _local_order = self.order
            best_value = 1e+4
        else:
            # 最大化する場合の分岐
            local_order = self.order
            _local_order = self._order
            best_value = -1e+4

        for rvs in self.get_recursive_reverse(boad):
            _boad = copy.deepcopy(boad)
            # 試しに1つ置いてみる.
            _boad[rvs['y']][rvs['x']] = local_order
            for cell in rvs['reverses']:
                _boad[cell['y']][cell['x']] = local_order
            prev_value = self.calc_minmax(_boad, not(node), itr - 1)

            if node:
                if prev_value < best_value:
                    best_value = prev_value
                    best_y = rvs['y']
                    best_x = rvs['x']
            else:
                if prev_value > best_value:
                    best_value = prev_value
                    best_y = rvs['y']
                    best_x = rvs['x']

        if itr == self.search_depth:
            reverses = self.check_reverse(best_y, best_x, boad)
            new_cell = {'y': best_y, 'x': best_x, 'order': self.order, 'reverses': reverses, 'pass': False}
            return new_cell
        else:
            return best_value

    def get_recursive_reverse(self, boad):
        boad_size = len(boad)
        candidates = []
        for y in range(boad_size):
            for x in range(boad_size):
                if boad[y][x] == self.init_cell:
                    reverses = self.check_reverse(y, x, boad)
                    if reverses != []:
                        candidates.append({'y': y, 'x': x, 'reverses': reverses})
        return candidates