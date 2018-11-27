# -*- coding: utf-8 -*-

def calc_each_numbers(boad, order):
    p1_num = 0
    boad_size = len(boad)
    for y in range(boad_size):
        for x in range(boad_size):
            if boad[y][x] == order:
                p1_num += 1
    return p1_num

def _calc_totalboad_scores(boad, order):
    score = 0
    return score
def _calc_linescores(boad, order):
    score = 0
    return score

def calc_totalboad_scores(boad, order, _order):
    cell_value= [
            [120, -20, 20,  5,  5, 20, -20, 120],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [ 20,  -5, 15,  3,  3, 15,  -5,  20],
            [  5,  -5,  3,  3,  3,  3,  -5,   5],
            [  5,  -5,  3,  3,  3,  3,  -5,   5],
            [ 20,  -5, 15,  3,  3, 15,  -5,  20],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [120, -20, 20,  5,  5, 20, -20, 120],
            ]

    score = 0
    b_size = len(cell_value)
    for y in range(b_size):
        for x in range(b_size):
            if boad[y][x] == order:
                score += cell_value[y][x]
            elif boad[y][x] == _order:
                score -= cell_value[y][x]
    return score

def calc_linescores(boad, order, _order):
    score = 0
    score_pattern = [100, 100, 100, 100, 10, 0, -50, -50]
    line_pattern = [[order, order, order], [None, order, order], [None, None, order], [order, None, order],\
                        [order, None, None], [None, None, None], [order, order, None], [None, order, None]]
    for sp in range(len(score_pattern)):
        # 左上から右に
        if [boad[0][0], boad[0][1], boad[0][2]] == list(reversed(line_pattern[sp])):
            score += score_pattern[sp]
        # 左上から下に
        if [boad[0][0], boad[1][0], boad[2][0]] == list(reversed(line_pattern[sp])):
            score += score_pattern[sp]
        # 左上から斜めに
        if [boad[0][0], boad[1][1], boad[2][2]] == list(reversed(line_pattern[sp])):
            score += score_pattern[sp]
        # 右上から右に
        if [boad[0][-3], boad[0][-2], boad[0][-1]] == line_pattern[sp]:
            score += score_pattern[sp]
        # 右上から下に
        if [boad[2][-1], boad[1][-1], boad[0][-1]] == line_pattern[sp]:
            score += score_pattern[sp]
        # 右上から斜めに
        if [boad[3][-3], boad[2][-2], boad[1][-1]] == line_pattern[sp]:
            score += score_pattern[sp]
        # 左下から右に
        if [boad[-1][0], boad[-1][1], boad[-1][2]] == list(reversed(line_pattern[sp])):
            score += score_pattern[sp]
        # 左下から上に
        if [boad[-1][0], boad[-2][0], boad[-3][0]] == list(reversed(line_pattern[sp])):
            score += score_pattern[sp]
        # 左下から斜めに
        if [boad[-1][0], boad[-2][1], boad[-3][2]] == list(reversed(line_pattern[sp])):
            score += score_pattern[sp]
        # 右下から右に
        if [boad[-1][-3], boad[-1][-2], boad[-1][-1]] == line_pattern[sp]:
            score += score_pattern[sp]
        # 右下から下にに
        if [boad[-3][-1], boad[-2][-1], boad[-1][-1]] == line_pattern[sp]:
            score += score_pattern[sp]
        # 右下から斜めに
        if [boad[-3][-3], boad[-2][-2], boad[-1][-1]] == line_pattern[sp]:
            score += score_pattern[sp]
    return score