import numpy as np
import Tkinter
from Tkinter import *
import tkMessageBox

# tags for file
file_tag='train' #train/test

# The board size of go game
BOARD_SIZE = 9
COLOR_BLACK=-1
COLOR_WHITE=1
COLOR_NONE=0
POINT_STATE_CHECKED=100
POINT_STATE_UNCHECKED=101
POINT_STATE_NOT_ALIVE=102
POINT_STATE_ALIVE=103
POINT_STATE_EMPYT=104

def read_go(file_name):
  # read from txt file and save as a matrix
  go_arr = np.zeros((BOARD_SIZE, BOARD_SIZE))
  for line in open(file_name):
    line = line.strip()
    lst = line.split()
    row = int(lst[0])
    col = int(lst[1])
    val = int(lst[2])
    go_arr[row, col] = val
  return go_arr


def plot_go(go_arr, txt='Default'):
  # Visualization of a go matrix
  # First draw a canvas with 9*9 grid
  root = Tk()
  cv = Canvas(root, width=50*(BOARD_SIZE+1), height=50*(BOARD_SIZE+1), bg='#F7DCB4')
  cv.create_text(250,10,text=txt,fill='blue')
  cv.pack(side=LEFT)
  size = 50
  for x in range(BOARD_SIZE):
    cv.create_line(size+x*size, size, size+x*size, size+(BOARD_SIZE-1)*size)
  for y in range(BOARD_SIZE):
    cv.create_line(size, size+y*size, size+(BOARD_SIZE-1)*size, size+size*y)
  # Second draw white and black circles on cross points
  offset = 20
  idx_black = np.argwhere(go_arr == COLOR_BLACK)
  idx_white = np.argwhere(go_arr == COLOR_WHITE)
  len_black = idx_black.shape[0]
  len_white = idx_white.shape[0]
  for i in range(len_black):
    if idx_black[i,0] >= BOARD_SIZE or idx_black[i,1] >= BOARD_SIZE:
      print 'IndexError: index out of range'
      sys.exit(0)
    else:
      new_x = 50*(idx_black[i,1]+1)
      new_y = 50*(idx_black[i,0]+1)
      cv.create_oval(new_x-offset, new_y-offset, new_x+offset, new_y+offset, width=1, fill='black', outline='black')
  for i in range(len_white):
    if idx_white[i,0] >= BOARD_SIZE or idx_white[i,1] >= BOARD_SIZE:
      print 'IndexError: index out of range'
      sys.exit(0)
    else:
      new_x = 50*(idx_white[i,1]+1)
      new_y = 50*(idx_white[i,0]+1)
      cv.create_oval(new_x-offset, new_y-offset, new_x+offset, new_y+offset, width=1, fill='white', outline='white')
  root.mainloop()

#-------------------------------------------------------
# Rule judgement
#-------------------------------------------------------
def is_alive(check_state, go_arr, i, j, color_type):
  '''
  This function checks whether the point (i,j) and its connected points with the same color are alive, it can only be used for white/black chess only
  Depth-first searching.
  :param check_state: The guard array to verify whether a point is checked
  :param go_arr: chess board
  :param i: x-index of the start point of searching
  :param j: y-index of the start point of searching
  :return: POINT_STATE_CHECKED/POINT_STATE_ALIVE/POINT_STATE_NOT_ALIVE, POINT_STATE_CHECKED=> the start point (i,j) is checked, POINT_STATE_ALIVE=> the point and its linked points with the same color are alive, POINT_STATE_NOT_ALIVE=>the point and its linked points with the same color are dead
  '''
  # whether the chess is inside the board
  if i <0 or i >= check_state.shape[0]:
    return POINT_STATE_NOT_ALIVE
  if j <0 or j >= check_state.shape[0]:
    return POINT_STATE_NOT_ALIVE
  # wheteher the chess is checked
  if check_state[i, j] == POINT_STATE_CHECKED:
    if go_arr[i,j] == color_type:
      return POINT_STATE_CHECKED
    else:
      return POINT_STATE_NOT_ALIVE
  if check_state[i,j] == POINT_STATE_EMPYT:
    return POINT_STATE_ALIVE

  live_state = POINT_STATE_ALIVE
  point_color_type = go_arr[i,j]
  if point_color_type != color_type:
    live_state = POINT_STATE_NOT_ALIVE
  elif point_color_type == color_type:
    check_state[i, j] = POINT_STATE_CHECKED
    live1=is_alive(check_state,go_arr,i,j-1,color_type)==POINT_STATE_ALIVE
    live2=is_alive(check_state,go_arr,i,j+1,color_type)==POINT_STATE_ALIVE
    live3=is_alive(check_state,go_arr,i-1,j,color_type)==POINT_STATE_ALIVE
    live4=is_alive(check_state,go_arr,i+1,j,color_type)==POINT_STATE_ALIVE
    if live1 or live2 or live3 or live4:
      live_state = POINT_STATE_ALIVE
    else:
      live_state = POINT_STATE_NOT_ALIVE
  return live_state

def go_judege(go_arr):
  '''
  :param go_arr: the numpy array contains the chess board
  :return: whether this chess board fit the go rules in the document
           False => unfit rule
           True => ok
  '''
  is_fit_go_rule = True
  check_state = np.zeros(go_arr.shape)
  check_state[:] = POINT_STATE_EMPYT
  tmp_indx = np.where(go_arr != 0)
  check_state[tmp_indx] = POINT_STATE_UNCHECKED
  for i in range(go_arr.shape[0]):
    for j in range(go_arr.shape[1]):
      if check_state[i, j] == POINT_STATE_UNCHECKED:
        tmp_alive = is_alive(check_state, go_arr,i,j, go_arr[i,j])
        if tmp_alive == POINT_STATE_NOT_ALIVE: # once the go rule is broken, stop the searching and return the state
          is_fit_go_rule = False
          break
      else:
        pass # pass if the point and its lined points are checked
  return is_fit_go_rule

#-------------------------------------------------------
# User strategy
#-------------------------------------------------------
def life_count(check_state, go_arr, i, j, color_type):
  '''
  This function checks whether the point (i,j) and its connected points with the same color are alive, it can only be used for white/black chess only
  Depth-first searching.
  :param check_state: The guard array to verify whether a point is checked
  :param go_arr: chess board
  :param i: x-index of the start point of searching
  :param j: y-index of the start point of searching
  :return: POINT_STATE_CHECKED/POINT_STATE_ALIVE/POINT_STATE_NOT_ALIVE, POINT_STATE_CHECKED=> the start point (i,j) is checked, POINT_STATE_ALIVE=> the point and its linked points with the same color are alive, POINT_STATE_NOT_ALIVE=>the point and its linked points with the same color are dead
  '''
  # whether the chess is inside the board
  if i <0 or i >= check_state.shape[0]:
    return {'state':POINT_STATE_NOT_ALIVE, 'position':[], 'collection':set([])}
  if j <0 or j >= check_state.shape[0]:
    return {'state':POINT_STATE_NOT_ALIVE, 'position':[], 'collection':set([])}
  # wheteher the chess is checked
  if check_state[i, j] == POINT_STATE_CHECKED:
    if go_arr[i,j] == color_type:
      return {'state':POINT_STATE_CHECKED, 'position':[], 'collection':set([])}
    else:
      return {'state':POINT_STATE_NOT_ALIVE, 'position':[], 'collection':set([])}
  if check_state[i,j] == POINT_STATE_EMPYT:
    return {'state':POINT_STATE_ALIVE, 'position':[(i,j)], 'collection':set([])}

  live_state = {'state':POINT_STATE_NOT_ALIVE, 'position':[], 'collection':set([(i,j)])}
  point_color_type = go_arr[i,j]
  if point_color_type != color_type:
    live_state = {'state':POINT_STATE_NOT_ALIVE, 'position':[], 'collection':set([])}
  elif point_color_type == color_type:
    check_state[i, j] = POINT_STATE_CHECKED
    live1=life_count(check_state,go_arr,i,j-1,color_type)
    live2=life_count(check_state,go_arr,i,j+1,color_type)
    live3=life_count(check_state,go_arr,i-1,j,color_type)
    live4=life_count(check_state,go_arr,i+1,j,color_type)
    live_state['collection'] = live_state['collection'] | live1['collection'] | live2['collection'] | live3['collection'] | live4['collection']
    if live1['state']==POINT_STATE_ALIVE:
      live_state['state']=POINT_STATE_ALIVE
      live_state['position'].extend(live1['position'])
    if live2['state']==POINT_STATE_ALIVE:
      live_state['state']=POINT_STATE_ALIVE
      live_state['position'].extend(live2['position'])
    if live3['state']==POINT_STATE_ALIVE:
      live_state['state']=POINT_STATE_ALIVE
      live_state['position'].extend(live3['position'])
    if live4['state']==POINT_STATE_ALIVE:
      live_state['state']=POINT_STATE_ALIVE
      live_state['position'].extend(live4['position'])
  return live_state

def user_step_eat(go_arr):
  step_points = set([])
  points_eaten = set([])
  check_state = np.zeros(go_arr.shape)
  check_state[:] = POINT_STATE_EMPYT
  tmp_indx = np.where(go_arr != 0)
  tmp_user_arr = np.copy(go_arr)
  check_state[tmp_indx] = POINT_STATE_UNCHECKED
  for i in range(go_arr.shape[0]):
    for j in range(go_arr.shape[1]):
      if check_state[i, j] == POINT_STATE_UNCHECKED and go_arr[i,j]==COLOR_BLACK:
        tmp_alive = life_count(check_state, go_arr, i, j, go_arr[i, j])
        if tmp_alive['state'] == POINT_STATE_ALIVE:  # once the go rule is broken, stop the searching and return the state
          if len(set(tmp_alive['position']))==1:
              step_points = step_points | set(tmp_alive['position'])
              points_eaten = points_eaten | tmp_alive['collection']
      else:
        pass  # pass if the point and its lined points are checked
  # set user arr
  for itme in step_points:
      i=itme[0]
      j=itme[1]
      tmp_user_arr[i,j]=COLOR_WHITE
  for itme in points_eaten:
      i=itme[0]
      j=itme[1]
      tmp_user_arr[i,j]=COLOR_NONE
  return [i for i in step_points], tmp_user_arr

def user_setp_possible(go_arr):
  tmp_position=[]
  tmp_user_arr = np.copy(go_arr)
  for i in range(tmp_user_arr.shape[0]):
    for j in range(tmp_user_arr.shape[1]):
      if tmp_user_arr[i,j] == COLOR_NONE:
        tmp_user_arr[i,j] = COLOR_WHITE
        if go_judege(tmp_user_arr):
          tmp_position.append((i,j))
        tmp_user_arr[i, j] = COLOR_NONE
  return tmp_position

if __name__ == "__main__":
  chess_rule_monitor = True
  problem_tag="Default"

  # The first problem: rule checking
  problem_tag = "[{}]Problem 0: rule checking".format(file_tag)
  go_arr = read_go('{}_0.txt'.format(file_tag))
  plot_go(go_arr, problem_tag)
  chess_rule_monitor=go_judege(go_arr)
  print "{}:{}".format(problem_tag, chess_rule_monitor)
  plot_go(go_arr, '{}=>{}'.format(problem_tag, chess_rule_monitor))

  problem_tag = "[{}]Problem 00: rule checking".format(file_tag)
  go_arr = read_go('{}_00.txt'.format(file_tag))
  plot_go(go_arr, problem_tag)
  chess_rule_monitor = go_judege(go_arr)
  print "{}:{}".format(problem_tag, chess_rule_monitor)
  plot_go(go_arr, '{}=>{}'.format(problem_tag, chess_rule_monitor))

  # The second~fifth prolbem: forward one step and eat the adverse points on the chessboard
  for i in range(1,5):
    problem_tag = "[{}]Problem {}: forward on step".format(file_tag,i)
    go_arr = read_go('{}_{}.txt'.format(file_tag, i))
    plot_go(go_arr, problem_tag)
    chess_rule_monitor = go_judege(go_arr)
    ans, user_arr = user_step_eat(go_arr)
    print "{}:{}".format(problem_tag, ans)
    plot_go(user_arr, '{}=>{}'.format(problem_tag, chess_rule_monitor))

  # The sixth problem: find all the postion which can place a white chess pieces
  problem_tag = "[{}]Problem {}: all possible position".format(file_tag,5)
  go_arr = read_go('{}_{}.txt'.format(file_tag,5))
  plot_go(go_arr, problem_tag)
  chess_rule_monitor = go_judege(go_arr)
  ans1,_ = user_step_eat(go_arr)
  ans = user_setp_possible(go_arr)
  ans.extend(ans1)
  print "{}:{}".format(problem_tag, ans)
  plot_go(go_arr, '{}=>{}'.format(problem_tag, chess_rule_monitor))