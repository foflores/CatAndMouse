# Q Agent
# Thomas Laurel
# May 25 2021
from collections import defaultdict
import sys
import numpy as np
import random

class Q_Learning_Agent:

    def __init__(self, learning_rate, discount_factor=.9):
        self.discount_factor = discount_factor
        self.learning_rate = learning_rate
        #initalize q table with 4 possible values for each coordinate pair
        self.Q = defaultdict( lambda: np.zeros(4))  #The Q-TABLE

    #testing function
    def Q_print(self):
        print("state", self.Q[state])
        print("state action pair", self.Q[state][action])


#---------------------------epsilon greedy algorithm----------------------------------------------------#

    def greedy_action(self, state, epsilon):

        if random.random() > epsilon:
            return np.argmax(self.Q[state])
        else:
            return np.random.choice(np.arange(4))


#---------------------------update q table----------------------------------------------------#

    def update_q_table(self, state, action, reward, next_state):
        self.Q[state][action] += self.learning_rate*(reward + self.discount_factor*np.max(self.Q[next_state]) - self.Q[state][action])
