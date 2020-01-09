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


def pixel2dist2(pixel):
    return 4.582e+09 * math.exp(-0.4491* pixel) + 35.16 * math.exp( -0.04358 * pixel)

def pixel2dist(pixel):
    if pixel == 42:
        return 0.5 * 80
    return 0.5 * (80/(pixel-42))



# initial settings of the environment
env = UnityEnvironment(
    n_arenas=1,
    file_name='../AnimalAI-Olympics/env/AnimalAI',
    worker_id=random.randint(1, 100),
    seed=0,
    docker_training=False,
    inference=True
    #play=True
)

# configuration of objects inside the environment
print("Start")
config = '../thesis/test_configs/depth.yaml'
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
p1.add(10,10,2)
p1.add(20,20,2)
p1.add(10,25,2)
p1.add(37,37,2)

carrot_planner = pe.pathExecuter(p1)



#head.set(90)

action = [0,0]

env_info = env.step([0, 0]) #for top view init


gt.findArena()
gt.update()
odo.set_pose([20,20])

depth = np.zeros((60,1))
surround = np.zeros((60,2))
pixel_val = np.zeros((60,1))

# the agent will take 20 time steps as an example
for i in range(330):

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
    low_threshold = 10  #30
    high_threshold = 30 #90
    ratio = 3
    kernel_size = (3,3)
    img_blur = cv.blur(gray, (3,3))
    detected_edges = cv.Canny(img_blur, low_threshold, high_threshold)#, kernel_size)
    #detected_edges = cv.Sobel(img_blur, cv.CV_32F, 1, 0)
    #edges_high_thresh = cv.Canny(gray, 100, 150)
    detected_edges[0:42][:] = 0
    #display.show(detected_edges)
    cv.imwrite("obstacle.png",gray)#cv.cvtColor(frame,cv.COLOR_BGR2RGB))

    for y in range(-42, 42):

        line = detected_edges[:, 42 + y]
        x = 42
        notFound = True
        while x < 84 and notFound:
            if line[x] == 255:
                depth = pixel2dist(x)
                depth_correct = depth / math.cos(math.radians(-y * (30 / 42)))
                notFound = False

                x_obs = odo.get_pose()[0] - depth_correct * math.sin(math.radians(head.get() - y * (30 / 42)))
                z_obs = odo.get_pose()[1] + depth_correct * math.cos(math.radians(head.get() - y * (30 / 42)))
                if depth < 10 and depth > 0 :
                    surround = np.append(surround, [[x_obs, z_obs]], axis=0)

            x += 1

    hsv_img = matplotlib.colors.rgb_to_hsv((observation[0, :, :, :]).astype(np.float))

    action = carrot_planner.calc_action(i,odo,head)

    #action =[0,2]
    env_info = env.step([action])

    head.update(action[1])


#log.save()

a = log.data

surround = np.delete(surround, 0,0 )

plt.figure(dpi=300)
#a[0,:]  = a[1,:]
plt.plot(surround[:,0], surround[:,1], 'o')
print(surround.size)

#plt.plot(a[:,5],a[:,6],marker='o',linewidth=0.5)
#plt.plot(a[:,7],a[:,8],marker = 'x',linewidth= 0.5)
plt.axis('equal')

plt.show()


pygame.quit()

env.close()
