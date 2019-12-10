from animalai.envs.environment import UnityEnvironment
from animalai.envs.arena_config import ArenaConfig
import matplotlib
import random
import pygame
import numpy as np
import matplotlib.pyplot as plt

import time
import compass as c
import display as d

import pyscreenshot as imagegrab
import mss
import cv2 as cv

from PIL import Image
def rect_detect(array,c_min,c_max,start,end):
    for i in range(start[0],end[0]):
        for j in range(start[1],end[1]):
            if array[i,j,0]>c_min and array[i,j,0]<c_max:
                return True
    return False






# initial settings of the environment
env = UnityEnvironment(
    n_arenas=1,
    file_name='../AnimalAI-Olympics/env/AnimalAI',
    worker_id=random.randint(1, 100),
    seed=0,
    docker_training=False,
    inference=True,
    # resolution=512,
    # play=True,0
)

# configuration of objects inside the environment
#arena_config_in = ArenaConfig('../thesis/test_configs/ground_truth_test.yaml')
arena_config_in = ArenaConfig('../AnimalAI-Olympics/examples/configs/allObjectsRandom.yaml')
env_info = env.reset(arenas_configurations=arena_config_in)
edge_top_left = cv.imread("edge_top_left.png", 0)
edge_bottom_right = cv.imread("edge_bottom_right.png", 0)
agent =cv.imread("mask_agent.png",0)
w1, h1 = edge_top_left.shape[::-1]
w2, h2 = edge_bottom_right.shape[::-1]
w, h = agent.shape[::-1]
agent_color_up = 225/2
agent_color_low = 175/2
relation = 40/512

display = d.Display()
# initalisation
compass = c.Compass()



t_start = time.time()
# the agent will take 20 time steps as an example
for i in range(361):

    # velocity
    speed = env_info['Learner'].vector_observations
    #print("speed: ", speed)

    # camera input
    observation = env_info['Learner'].visual_observations[0]

    display.update(observation, compass)
    if not i == 0:
        with mss.mss() as sct:
            img = cv.cvtColor(np.array(sct.grab(sct.monitors[0])), cv.COLOR_BGRA2BGR)
            if i == 1:
                screenshot = cv.cvtColor(np.array(img), cv.COLOR_BGR2GRAY)

                res1= cv.matchTemplate(screenshot, edge_top_left, method=cv.TM_SQDIFF)
                res2 = cv.matchTemplate(screenshot, edge_bottom_right, method=cv.TM_SQDIFF)

                min_val1, max_val1, min_loc1, max_loc1 = cv.minMaxLoc(res1)
                min_val2, max_val2, min_loc2, max_loc2 = cv.minMaxLoc(res2)
                # min_val2, max_val3, min_loc3, max_loc3 = cv.minMaxLoc(res3)
                top_left1 = min_loc1
                top_left2 = min_loc2
                # top_left2 = min_loc3
                bottom_right1 = (top_left1[0] + w1, top_left1[1] + h1)
                bottom_right2 = (top_left2[0] + w2, top_left2[1] + h2)
                # bottom_right2 = (top_left3[0] + w3, top_left3[1] + h3)

            arena = img[bottom_right1[1] - 10:top_left2[1] + 12, bottom_right1[0] - 10:top_left2[0] + 12]

            #hsv_arena = matplotlib.colors.rgb_to_hsv((arena/255.0).astype(np.float))
            hsv_arena = cv.cvtColor(arena, cv.COLOR_BGR2HSV)
            h_arena = hsv_arena[:,:,0]
            mask = cv.inRange(h_arena, agent_color_low ,agent_color_up)

            res1 = cv.matchTemplate(mask, agent, method=cv.TM_SQDIFF)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res1)

            top_left = min_loc

            agent_position = ((top_left[0]+ w/2)*relation, (512-(top_left[1] + h/2)) * relation)
            if min_val > 2500000 :
                agent_position = (-1,-1)
            print("x,y = ", agent_position)






    hsv_img = cv.cvtColor((observation[0, :, :, :]*255).astype(np.uint8), cv.COLOR_RGB2HSV)

    env_info = env.step([0, 2])
    compass.step_left()

    # Then, finally you decide what action to take
    # I'm sending a forward action to the environment every time step here as an example.
    #if rect_detect(hsv_img,60/255,180/255,(30,36),(42,48)) and not rect_detect(hsv_img,60/255,180/255,(42,36),(54,48)) :
        #env_info = env.step([0, 0])
        #print("final result: ")
        #print(turn_steps)
        #turn_steps = 0
    #else:
        #env_info = env.step([0, 1])
        #turn_steps += 1
        #print(turn_steps)
    #print('turn step: ',turn_steps

print( time.time()-t_start)
time.sleep(10)

pygame.quit()

env.close()