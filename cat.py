import pygame
import random
import sys

from agent import Q_Learning_Agent
from environment import Game_Environment, Game_Maze
from network import Connection

LOCAL_HOST = "192.168.0.23"

display_width, display_height = 600, 700

display = pygame.display.set_mode((display_width,display_height))

game_maze = Game_Maze(rows=10, columns=10)
env = Game_Environment(display, game_maze)

#connect to other node
server = Connection()
server.connect((LOCAL_HOST, 8050))

clients = server.get_clients()
client = clients[0]

#initilaize agents
cat = Q_Learning_Agent(learning_rate = 1)

total_mouse_caught = 0
total_cheese_eaten = 0

epsilon, eps_decay, eps_min = .99, 0.99, 0.05
#number of episodes to train
num_episodes = 1000

# loop over episodes
for episode in range(1, num_episodes+1):
    #print(episode)
    # monitor progress
    if episode % 100 == 0:
        print("\rEpisode {}/{} \n".format(episode, num_episodes), end="")

        print("mouse eaten: ", total_mouse_caught)

        print("cheese eaten: ", total_cheese_eaten)

        print("current difference: ", total_mouse_caught - total_cheese_eaten)

        #print(cat.Q)
        sys.stdout.flush()

    epsilon = max(epsilon*eps_decay, eps_min)

    state = env.reset()

    action_mouse = int(server.recv_from(client))

    action_cat = cat.greedy_action(state['cat'], epsilon)
    server.send_data(str(action_cat), client)

    while True:

        nxt_state, reward, is_Game_Over, info = env.step(action_mouse, action_cat)

        #bellman equation
        cat.update_q_table(state['cat'], action_cat, reward['cat'], nxt_state['cat'])

        if is_Game_Over:
            if info['cheese_eaten']:
                total_cheese_eaten += 1

            if info['mouse_caught']:
                total_mouse_caught += 1
            #finish this episode
            break

        #update state and action
        state = nxt_state

        action_mouse = int(server.recv_from(client))

        action_cat = cat.greedy_action(state['cat'], epsilon)
        server.send_data(str(action_cat), client)



#INFERENCE
num_eps = 1
for i in range(num_eps):
    print("\n inference \n")
    state = env.inference()
    action_mouse = int(server.recv_from(client))

    action_cat = cat.greedy_action(state['cat'], 0)
    server.send_data(str(action_cat), client)

    while True:

        nxt_state, reward, is_Game_Over, info = env.step(action_mouse, action_cat)

        if is_Game_Over:
            if info['cheese_eaten']:
                total_cheese_eaten += 1
                print("MOUSE HAS WON FINALE")

            if info['mouse_caught']:
                total_mouse_caught += 1
                print("CAT HAS WON FINALE")

            break

        #update state and action
        state = nxt_state
        action_mouse = int(server.recv_from(client))

        action_cat = cat.greedy_action(state['cat'], 100)
        server.send_data(str(action_cat), client)


print("mouse eaten: ", total_mouse_caught)
print("cheese eaten: ", total_cheese_eaten)

#step penalty, for each step
#without cat and mouse seeing each other, just explore maze
#when they see each other, start tictactoe
#vision parameter determines how far the cat and mouse can see each other
#whereever the cheese is, set a 3x3 space for tictactoe
