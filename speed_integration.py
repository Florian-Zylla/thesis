from animalai.envs.environment import UnityEnvironment
from animalai.envs.arena_config import ArenaConfig
import matplotlib
import random
import pygame
import numpy as np
import time
import math
import compass as c
import display as d





# initial settings of the environment
env = UnityEnvironment(
    n_arenas=1,
    file_name='../AnimalAI-Olympics/env/AnimalAI',
    worker_id=random.randint(1, 100),
    seed=0,
    docker_training=False,
    inference=True,
    # resolution=512,
    # play=True,
)

# configuration of objects inside the environment
print("Start")
arena_config_in = ArenaConfig('../thesis/test_configs/acceleration_speed_test.yaml')
env_info = env.reset(arenas_configurations=arena_config_in)



display = d.Display()
compass = c.Compass()
x = 0
y = 0
z = 0
theta = 0
step = 0.0595

l_turn = 0
l_forward = 0

# the agent will take 20 time steps as an example
for i in range(81):

    # velocity
    speed = env_info['Learner'].vector_observations
    print(speed.shape)
    #print("speed: ", speed)


    if l_turn !=  0:
        if l_turn == 1:
            theta = compass.get() + 3
        else:
            theta = compass.get() - 3
    else:
        theta = compass.get()

    x += speed[0,2] * math.cos((theta / 180) * math.pi) * step
    y += speed[0,2] * math.sin((theta / 180) * math.pi) * step

    print("position: ",(theta,x,y) )









    # camera input
    observation = env_info['Learner'].visual_observations[0]
    display.update(observation, compass)





    hsv_img = matplotlib.colors.rgb_to_hsv((observation[0, :, :, :]).astype(np.float))
    if i % 5 == 0:
        l_forward = random.randint(0,2)

    if i%10 == 0:
        l_turn = random.randint(0, 2)
    env_info = env.step([l_forward, l_turn])
    if l_turn == 2:
        compass.step_left()
    if l_turn == 1:
        compass.step_right()
time.sleep(30)

pygame.quit()

env.close()