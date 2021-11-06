# Environment
# Thomas Laurel
# May 25 2021
import numpy as np
import random
from collections import deque

class Game_Environment():

    def __init__(self, gameDisplay, game_matrix):

        #check game maze at end of file
        self.HEIGHT = game_matrix.ROWS  #environemnt height
        self.WIDTH = game_matrix.COLUMNS   #environment width

        display_width, display_height = gameDisplay.get_size()
        display_height -= 100   #since we need some space to show important data.

        self.BLOCK_WIDTH = int(display_width/self.WIDTH)
        self.BLOCK_HEIGHT = int(display_height/self.HEIGHT)

        self.MOVES = {'mouse':150,'cat':150}


        self.OBSTACLES = game_matrix.OBSTACLES

#---------------------------------------------returns current board state----------------------------------#

    def get_current_state(self):

        self.STATE = {'mouse':(self.MOUSE_X - self.CAT_X, self.MOUSE_Y - self.CAT_Y,self.MOUSE_X - self.CHEESE_X,self.MOUSE_Y -  self.CHEESE_Y),
                        'cat':(self.CAT_X - self.MOUSE_X, self.CAT_Y - self.MOUSE_Y)}

        return self.STATE

#--------------------------------------------RESET TO NEW POSITIONS--------------------------------------------------#

    def reset(self):
        self.MOUSE_X, self.MOUSE_Y = (0,0)
        self.CAT_X, self.CAT_Y = (0, self.HEIGHT -1)
        self.CHEESE_X, self.CHEESE_Y = (3,3)

        #check if cheese is obstructed lol thomas rocks
        for check_space in self.OBSTACLES:
            if self.CHEESE_X == check_space[0] and self.CHEESE_Y == check_space[1]:
                #IF IT IS THEN SHIFT IT UP
                    self.CHEESE_Y -= 1

        self.MOVES['cat'] = 100
        self.MOVES['mouse'] = 100

        return self.get_current_state()

#--------------------------------------------FINAL RESET------------------------------------#

    def inference(self):
        self.MOUSE_X, self.MOUSE_Y = (0,0)
        self.CAT_X, self.CAT_Y = (0, self.HEIGHT -1)
        self.CHEESE_X, self.CHEESE_Y = (3,3)

        #CHECK IF CHEESE IS OBSTRUCTED
        for check_space in self.OBSTACLES:
            if self.CHEESE_X == check_space[0] and self.CHEESE_Y == check_space[1]:
                #then shift it up
                    self.CHEESE_Y -= 1

        self.MOVES['cat'] = 1000
        self.MOVES['mouse'] = 1000

        return self.get_current_state()



#--------------------------------------AGENTS MOVES------------------------------------#

    def step(self,mouse_move, cat_move):

        reward = {'mouse':-1, 'cat':-1}
        is_Game_Over = False
        info = {
            'cheese_eaten': False,
            'mouse_caught': False,
            'x': -1, 'y': -1,
            'width':self.BLOCK_WIDTH,
            'height':self.BLOCK_HEIGHT
        }


        #the cat and mouse have a limited number of moves, if the move counter reaches zero then a training episode terminates
        self.MOVES['cat'] -= 1
        self.MOVES['mouse'] -= 1
        #moves = 0 then finish
        if self.MOVES['cat'] == 0 or self.MOVES['mouse'] == 0:
            is_Game_Over = True

        self.update_positions(mouse_move, cat_move)

        #if the mouse is on top of the cheese it is a mouse win
        if self.MOUSE_X == self.CHEESE_X and self.MOUSE_Y == self.CHEESE_Y:
            is_Game_Over = True
            reward['mouse'] = 100
            #reward['cat'] = -100
            info['cheese_eaten'], info['x'], info['y'] = True,  self.MOUSE_X, self.MOUSE_Y

        #if the cat is on top of the mouse, it is a cat win
        if self.CAT_X == self.MOUSE_X and self.CAT_Y == self.MOUSE_Y:
            is_Game_Over = True
            reward['cat'] = 100
            reward['mouse'] = -100
            info['mouse_caught'], info['x'], info['y'] = True,  self.MOUSE_X, self.MOUSE_Y

        for check_space in self.OBSTACLES:
            if self.MOUSE_X == check_space[0] and self.MOUSE_Y == check_space[1]:
                reward['mouse'] = -20
                self.MOUSE_X, self.MOUSE_Y = (0,0)

            if self.CAT_X == check_space[0] and self.CAT_Y == check_space[1]:
                reward['cat'] = -20
                self.CAT_X, self.CAT_Y = (0, self.HEIGHT -1)

        return self.get_current_state(), reward, is_Game_Over, info



#-------------------------------MOVE THE AGENT ON THE X OR Y AXIS--------------#


    def decide_action(self, action):
        x_change = 0
        y_change = 0

        #move left
        if action == 0:
            x_change = -1

        #move right
        elif action == 1:
            x_change = 1

        #move up
        elif action == 2:
            y_change = -1

        #move down
        elif action ==3:
            y_change = 1


        return x_change, y_change

#-----------------------------AFTER THE AGENTS HAVE MOVED YOU NEED TO UPDATE THEIR INFORMATION-------------------------------------#

    def update_positions(self, mouse_move, cat_move):
        x_change_mouse, y_change_mouse = self.decide_action(mouse_move)
        x_change_cat, y_change_cat = self.decide_action(cat_move)

        self.MOUSE_X += x_change_mouse
        self.MOUSE_Y += y_change_mouse

        self.CAT_X += x_change_cat
        self.CAT_Y += y_change_cat

        if self.MOUSE_X < 0:
            self.MOUSE_X = 0

        elif self.MOUSE_X > self.WIDTH-1:
            self.MOUSE_X = self.WIDTH-1

        if self.MOUSE_Y < 0:
            self.MOUSE_Y= 0

        elif self.MOUSE_Y > self.HEIGHT -1:
            self.MOUSE_Y = self.HEIGHT -1

        if self.CAT_X < 0:
            self.CAT_X = 0

        elif self.CAT_X > self.WIDTH-1:
            self.CAT_X = self.WIDTH-1

        if self.CAT_Y < 0:
            self.CAT_Y= 0

        elif self.CAT_Y > self.HEIGHT -1:
            self.CAT_Y = self.HEIGHT -1

#---- HELP CREATE A UNIQUE GAME ENVIRONMNET -------------------#


class Game_Maze:

	def __init__(self, rows, columns):
		self.ROWS = rows
		self.COLUMNS = columns
		self.OBSTACLES = [[3,2], [3,7], [8,2], [8,7], [6,6]]
        #self.OBSTACLES = [[2,2], [2,3], [2,4], [2,5], [2,7], [7,2], [6,2], [5,2], [4,2], [7,7], [6,7], [5,7], [5,5], [5,6]]
        #[3,2], [3,7], [8,2], [8,7], [6,6]
