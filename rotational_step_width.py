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


class GroundTruth:
    #class to extract an image of the arena from the unity environment topview, later detect the agent
    #and calculate its position
    gt_pos = (0, 0)
    edge_top_left = []
    edge_bottom_right = []
    agent = []
    w_TL, h_TL = (0, 0)
    w_BR, h_BR = (0, 0)
    w_AGENT, h_AGENT = (0, 0)
    TL = (0, 0)
    BR = (0, 0)
    agent_color_up = 225 / 2
    agent_color_low = 175 / 2
    relation = 40 / 512

    def __init__(self):

        self.edge_top_left = cv.imread("edge_top_left.png", 0)
        self.edge_bottom_right = cv.imread("edge_bottom_right.png", 0)
        self.agent = cv.imread("mask_agent.png", 0)
        self.w_TL, self.h_TL = self.edge_top_left.shape[::-1]
        self.w_BR, self.h_BR = self.edge_bottom_right.shape[::-1]
        self.w_AGENT, self.h_AGENT = self.agent.shape[::-1]





    def findArena(self):
        with mss.mss() as sct:
            img = cv.cvtColor(np.array(sct.grab(sct.monitors[0])), cv.COLOR_BGRA2BGR)
            if i == 1:
                screenshot = cv.cvtColor(np.array(img), cv.COLOR_BGR2GRAY)

                res_TL = cv.matchTemplate(screenshot, self.edge_top_left, method=cv.TM_SQDIFF)
                res_BR = cv.matchTemplate(screenshot, self.edge_bottom_right, method=cv.TM_SQDIFF)

                min_val1, max_val1, min_loc1, max_loc1 = cv.minMaxLoc(res_TL)
                min_val2, max_val2, min_loc2, max_loc2 = cv.minMaxLoc(res_BR)

                self.TL = (min_loc1[0] + self.w_TL, min_loc1[1] + self.h_TL)
                self.BR = min_loc2







    def update(self):
        with mss.mss() as sct:
            img = cv.cvtColor(np.array(sct.grab(sct.monitors[0])), cv.COLOR_BGRA2BGR)
            arena = img[self.TL[1] - 10:self.BR[1] + 12, self.TL[0] - 10:self.BR[0] + 12]

          
            hsv_arena = cv.cvtColor(arena, cv.COLOR_BGR2HSV)
            h_arena = hsv_arena[:, :, 0]
            mask = cv.inRange(h_arena, self.agent_color_low, self.agent_color_up)

            res = cv.matchTemplate(mask, self.agent, method=cv.TM_SQDIFF)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

            top_left = min_loc

            self.gt_pos = ((top_left[0] + self.w_AGENT / 2) * self.relation, (512 - (top_left[1] + self.h_AGENT / 2)) * self.relation)
            if min_val > 2500000:
                self.gt_pos = (-1, -1)

    def get(self):
        return self.gt_pos

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
#edge_top_left = cv.imread("edge_top_left.png", 0)
#edge_bottom_right = cv.imread("edge_bottom_right.png", 0)
#agent =cv.imread("mask_agent.png",0)
#w1, h1 = edge_top_left.shape[::-1]
#w2, h2 = edge_bottom_right.shape[::-1]
#w, h = agent.shape[::-1]
#agent_color_up = 225/2
#agent_color_low = 175/2
#relation = 40/512

gt = GroundTruth()
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
        if i ==1:
            gt.findArena()
        gt.update()
        print(gt.get())






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