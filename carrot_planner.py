from animalai.envs.environment import UnityEnvironment
from animalai.envs.arena_config import ArenaConfig
import matplotlib
import matplotlib.pyplot as plt
import random
import pygame
import numpy as np
import math
import time


import compass.compass as c
import display.display as d
import groundTruth.groundTruth as gt
import odometry.odometry as o
import log.log as l



# initial settings of the environment
env = UnityEnvironment(
    n_arenas=1,
    file_name='../AnimalAI-Olympics/env/AnimalAI',
    worker_id=random.randint(1, 100),
    seed=0,
    docker_training=False,
    inference=True

    # resolution=512,
    #play=True
)

# configuration of objects inside the environment
print("Start")
config = '../thesis/test_configs/carrot.yaml'
arena_config_in = ArenaConfig(config)
env_info = env.reset(arenas_configurations=arena_config_in)

display = d.Display()
compass = c.Compass()



gt = gt.GroundTruth()
odo = o.Odometry()
log = l.Log(config)

goal = (25,25)

l_turn = 1
l_forward = 0

env_info = env.step([0, 0])
gt.findArena()
gt.update()
odo.set_pose(gt.get())
# the agent will take 20 time steps as an example
for i in range(800):

    gt.update()
    # velocity
    speed = env_info['Learner'].vector_observations
    odo.update_pose(speed,compass)


    # camera input
    observation = env_info['Learner'].visual_observations[0]
    display.update(observation, compass, gt)
    log.update(i, speed, compass, odo, gt)


    hsv_img = matplotlib.colors.rgb_to_hsv((observation[0, :, :, :]).astype(np.float))

    #half speed
    if i%2:
        l_forward = 0
    else:
        l_forward = 1

    #rotation
    delta_x = goal[0] -odo.get_pose()[0]
    delta_z = goal[1] - odo.get_pose()[1]
    dist = math.sqrt(math.pow(delta_x,2)+ math.pow(delta_z,2))
    goal_theta = math.atan(delta_z/delta_x)

    diff_theta = math.degrees(goal_theta) - compass.get()
    print





    env_info = env.step([l_forward, l_turn])
    if l_turn == 2:
        compass.step_left()
    if l_turn == 1:
        compass.step_right()



log.save()

a = log.data

plt.figure(dpi=300)
a[0,:]  = a[1,:]

plt.plot(a[:,5],a[:,6],marker='o',linewidth=0.5)
plt.plot(a[:,7],a[:,8],marker = 'x',linewidth= 0.5)
plt.axis('equal')

plt.show()


pygame.quit()

env.close()
