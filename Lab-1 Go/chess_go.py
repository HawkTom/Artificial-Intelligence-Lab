#
#                        _oo0oo_
#                       o8888888o
#                       88" . "88
#                       (| -_- |)
#                       0\  =  /0
#                     ___/`---'\___
#                   .' \\|     |// '.
#                  / \\|||  :  |||// \
#                 / _||||| -:- |||||- \
#                |   | \\\  -  /// |   |
#                | \_|  ''\---/''  |_/ |
#                \  .-\__  '-'  ___/-. /
#              ___'. .'  /--.--\  `. .'___
#           ."" '<  `.___\_<|>_/___.' >' "".
#          | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#          \  \ `_.   \_ __\ /__ _/   .-` /  /
#      =====`-.____`.___ \_____/___.-`___.-'=====
#                        `=---='
#
#
#      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                佛祖保佑         永无BUG
#
from tkinter import *
import numpy as np

UNCHECKED = 444
EMPTY = 0
UNEMPTY = 111
CHECKED = 333
WHITE = 1
BLACK = -1


def openFile(file):
    go_arr = np.zeros((9, 9))
    for line in open(file):
        line = line.strip()
        line = line.split()
        row = int(line[0])
        col = int(line[1])
        value = int(line[2])
        go_arr[row, col] = value
    return go_arr


def plot_chess(go_arr, txt="True"):
    root = Tk()
    cv = Canvas(root, width=10 * 50, height=10 * 50, bg='#F7DCB4')
    cv.create_text(250, 20, text='Chess Table => ' + txt, fill='blue')
    cv.pack()

    for i in range(9):
        cv.create_line(50 * (i + 1), 50, 50 * (i + 1), 450)
    for i in range(9):
        cv.create_line(50, 50 + 50 * i, 450, 50 + 50 * i)

    black_index = np.argwhere(go_arr == BLACK)
    white_index = np.argwhere(go_arr == WHITE)
    for index in black_index:
        row = (index[0] + 1) * 50
        col = (index[1] + 1) * 50
        cv.create_oval(col - 20, row - 20, col + 20, row + 20, fill='black')

    for index in white_index:
        row = (index[0] + 1) * 50
        col = (index[1] + 1) * 50
        cv.create_oval(col - 20, row - 20, col + 20, row +
                       20, fill='white', outline='white')

    root.mainloop()


chess_line = []
chess_color = BLACK


def is_alive(check_state, go_arr, i, j, color_type, play_order=WHITE):
    global chess_line, chess_color
    if i < 0 or i >= 9 or j < 0 or j >= 9:   # border bound judge
        return False
    if check_state[i, j] == CHECKED:
        return False
    if go_arr[i, j] == EMPTY:  # empty position means alive
        return True
    if go_arr[i, j] != color_type:  # different type means no liberty in one direction
        return False
    else:
        check_state[i, j] = CHECKED
        live0 = is_alive(check_state, go_arr, i - 1, j,
                         color_type)  # judge left position
        live1 = is_alive(check_state, go_arr, i + 1, j,
                         color_type)  # judge right position
        live2 = is_alive(check_state, go_arr, i, j - 1,
                         color_type)  # judge down position
        live3 = is_alive(check_state, go_arr, i, j + 1,
                         color_type)  # judge up position

    if not (live0 or live1 or live2 or live3):
        if color_type != play_order:
            chess_line.append([i, j])
        chess_color = color_type
        return False
    else:
        chess_line = []
        return True


def chess_check(go_arr, play_order=WHITE, question=1):
    global chess_line, chess_color
    check_state = np.zeros(go_arr.shape)
    check_state[:] = EMPTY
    check_state[np.where(go_arr != EMPTY)] = UNCHECKED

    for i in range(9):
        for j in range(9):
            if check_state[i, j] == UNCHECKED:
                live = is_alive(check_state, go_arr, i, j, go_arr[i, j])
                if live != True:
                    if question == 1:
                        return False
                    elif chess_color != play_order:
                        return False
                    else:
                        pass
    return True


def next_eat(go_arr):
    place_position = []
    eat_position = []
    global chess_line
    check_empty = np.zeros(go_arr.shape)
    check_empty[:] = UNEMPTY
    check_empty[np.where(go_arr == 0)] = EMPTY

    for i in range(9):
        for j in range(9):
            if check_empty[i, j] == EMPTY:
                go_tmp = np.copy(go_arr)
                go_tmp[i, j] = WHITE
                if not chess_check(go_tmp, question=2):
                    place_position.append([i, j])
                    eat_position.append(chess_line)
    print(place_position)
    for index in place_position:
        go_arr[index[0], index[1]] = WHITE
    for position in eat_position:
        for index in position:
            go_arr[index[0], index[1]] = EMPTY
    return go_arr


def next_impossible(go_arr):
    global chess_color
    next_possible = []
    check_empty = np.zeros(go_arr.shape)
    check_empty[:] = UNEMPTY
    check_empty[np.where(go_arr == 0)] = EMPTY
    for i in range(9):  # find all positions not break rules
        for j in range(9):
            if check_empty[i, j] == EMPTY:
                go_tmp = np.copy(go_arr)
                go_tmp[i, j] = WHITE
                if chess_check(go_tmp, question=1):
                    next_possible.append([i, j])

    for i in range(9):  # find all positions that could eat black chess
        for j in range(9):
            if check_empty[i, j] == EMPTY:
                go_tmp = np.copy(go_arr)
                go_tmp[i, j] = WHITE
                if not chess_check(go_tmp, question=2):
                    next_possible.append([i, j])
    return next_possible


if __name__ == '__main__':
    # The Data File Path
    file_fix = r"test_"
    question = input("Please input the question_number (end with Enter) = ")
    print('\n')
    if question == "1":
        for i in range(7):
            file = file_fix + str(i) + '.txt'
            go_arr = openFile(file)
            plot_chess(go_arr, str(chess_check(go_arr)) + '  train' + str(i))
    elif question == "2":
        for i in range(8):
            file = file_fix + str(i) + '.txt'
            print(file)
            go_arr = openFile(file)
            states = chess_check(go_arr)
            plot_chess(go_arr, str(states) + ' train' + str(i))
            if states:
                plot_chess(next_eat(go_arr), 'eat_after,' + ' train' + str(i))
            else:
                print('train_' + str(i) + ": the chess is against rule !!!")
    elif question == "3":
        for i in range(0, 7):
            file = file_fix + str(i) + '.txt'
            go_arr = openFile(file)
            states = chess_check(go_arr)
            plot_chess(go_arr, str(states))
            if not states:
                print('train_' + str(i) + ": the chess is against rule !!!")
            else:
                ans = next_impossible(go_arr)
                print('train_' + str(i) + ': ', ans)
                ### you can write the ans into a file
