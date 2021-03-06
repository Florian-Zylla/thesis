from animalai.envs.environment import UnityEnvironment
from animalai.envs.arena_config import ArenaConfig
import matplotlib
import matplotlib.pyplot as plt
import random
import pygame
import numpy as np
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
config = '../thesis/test_configs/acceleration_speed_test.yaml'
arena_config_in = ArenaConfig(config)
env_info = env.reset(arenas_configurations=arena_config_in)

display = d.Display()
compass = c.Compass()



gt = gt.GroundTruth()
odo = o.Odometry()
log = l.Log(config)


l_turn = 1
l_forward = 1
"""
t = 12
f=12
"""
env_info = env.step([0, 0])
gt.findArena()
gt.update()
odo.set_pose(gt.get())
# the agent will take 20 time steps as an example
for i in range(1000):

    gt.update()
    # velocity
    speed = env_info['Learner'].vector_observations
    odo.update_pose(speed,compass)
    #print(odo.get_pose())


    # camera input
    observation = env_info['Learner'].visual_observations[0]
    display.update(observation, compass, gt)
    log.update(i, speed, compass, odo, gt)


    hsv_img = matplotlib.colors.rgb_to_hsv((observation[0, :, :, :]).astype(np.float))
    """
    if i == 0:
        l_turn = 0
        l_forward = 1

    if i == 5:
        l_forward = 0
        l_turn = 0
    if i == 15:
        l_turn = 1
    if i == 30:
        l_turn = 0
        l_forward = 1
    if i == 35:
        l_forward = 0
    if i == 45:
        l_turn = 1
    if i == 60:
        l_forward = 1
        l_turn = 0
    if i == 65:
        l_forward = 0

    if i == 75:
        l_turn = 1

    if i == 90:
        l_turn = 0
        l_forward = 1

    if i == 95:
        l_forward = 0
    """
    """
    if i%2:
        l_forward = 0
    else:
        l_forward = 1
"""
    """
    t -= 1
    f -= 1
    if t <= 0:
        t = random.randint(0,15)
        l_turn = random.randint(0,2)
    if f <= 0:
        f = random.randint(0, 15)
        l_forward = random.randint(0, 2)
        if l_forward == 0:
            f = f/2



    env_info = env.step([l_forward, l_turn])
    if l_turn == 2:
        compass.step_left()
    if l_turn == 1:
        compass.step_right()
    """


log.save()
"""
plt.plot(t,z/50)
plt.plot(t,y)
plt.plot(t,x)
plt.show()
"""
a = log.data

plt.figure(dpi=300)
a[0,:]  = a[1,:]

plt.plot(a[:,5],a[:,6],marker='o',linewidth=0.5)
plt.plot(a[:,7],a[:,8],marker = 'x',linewidth= 0.5)
plt.axis('equal')
"""
plt.plot(a[:,0],a[:,1])
plt.plot(a[:,0],a[:,2])
plt.plot(a[:,0],a[:,3])
"""
plt.show()


pygame.quit()

env.close()
