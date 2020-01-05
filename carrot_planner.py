from animalai.envs.environment import UnityEnvironment
from animalai.envs.arena_config import ArenaConfig
import matplotlib
import matplotlib.pyplot as plt
import random
import pygame
import numpy as np
import math
import time
import cv2 as cv


import compass.compass as c
import display.display as d
import groundTruth.groundTruth as gt
import odometry.odometry as o
import log.log as l
import heading.heading as h
import trajectory.trajectory as t
import pathExecuter.pathExecuter as pe


def diff_angles(a,b):
    diff_theta = abs(a - b)%360
    if diff_theta > 180:
        diff_theta = 360 -diff_theta
    if (a-b >= 0 and a-b <= 180) or (a-b<=-180 and a-b>=-360):
        diff_theta *= -1
    return diff_theta


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
head = h.Heading()


gt = gt.GroundTruth()
odo = o.Odometry()
log = l.Log(config)

p1 = t.Trajectory(23,17,2)
p1.add(20,10,2)
p1.add(2,2,2)
p1.add(3,20,2)
p1.add(5,37,2)

carrot_planner = pe.pathExecuter(p1)


#head.set(270)

action = [0,0]

env_info = env.step([0, 0]) #for top view init


gt.findArena()
gt.update()
odo.set_pose(gt.get())



# the agent will take 20 time steps as an example
for i in range(250):

    gt.update()
    # velocity
    speed = env_info['Learner'].vector_observations
    odo.update_pose(speed, head)

    # camera input
    observation = env_info['Learner'].visual_observations[0]

    log.update(i, speed, head, odo, gt)

    display.update(observation, head, gt)






    frame = (observation[0,:,:,:]*255).astype(np.uint8)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    low_threshold = 80
    ratio = 3
    kernel_size = (3,3)
    img_blur = cv.blur(gray, (3,3))
    detected_edges = cv.Canny(img_blur, low_threshold, low_threshold*ratio, kernel_size)
    #edges_high_thresh = cv.Canny(gray, 100, 150)
    #display.show(detected_edges)



    hsv_img = matplotlib.colors.rgb_to_hsv((observation[0, :, :, :]).astype(np.float))

    action = carrot_planner.calc_action(i,odo,head)

    env_info = env.step([action])

    head.update(action[1])


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
