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

class Log:
    start_time = 0
    t = np.array(0)
    v = np.array([0,0,0])
    pose_gt = np.array([0,0])
    pose_odo = np.array([0,0])
    orient = np.array([0])

    def __init__(self):
        self.start_time = time.strftime("%d.%m.%Y %H:%M:%S")

    def update(self,step,odometry,compass,groundTruth):
        self.step = np.append(self.t,np.array(step))
        self.v = np.append(self.v,[speed[0,:]],axis=0)
        self.pose_gt = np.append(self.pose_gt,[gt.get()])
        self.pose_odo = np.append(self.pose_odo,[odometry.get_pose()])
        self.orient = np.append(self.orient,np.array(compass.get()))




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
arena_config_in = ArenaConfig('../thesis/test_configs/acceleration_speed_test.yaml')
env_info = env.reset(arenas_configurations=arena_config_in)

display = d.Display()
compass = c.Compass()
gt = gt.GroundTruth()
odo = o.Odometry()
log = Log()
x = np.array(0)
y = np.array(0)
z = np.array(0)


l_turn = 0
l_forward = 0
t = np.array(0)

# the agent will take 20 time steps as an example
for i in range(120):

    if not i == 0:
        if i == 1:
            gt.findArena()
            gt.update()
            odo.set_pose(gt.get())
        gt.update()
    # velocity
    speed = env_info['Learner'].vector_observations
    #odo.update_pose(speed,compass)
    print(odo.get_pose())

    t = np.append(t,i)
    x = np.append(x,speed[0,0])
    y = np.append(y,speed[0,1])
    z = np.append(z,speed[0,2])
    # camera input
    observation = env_info['Learner'].visual_observations[0]
    display.update(observation, compass, gt)
    #log.update(i,odo,compass,gt)


    hsv_img = matplotlib.colors.rgb_to_hsv((observation[0, :, :, :]).astype(np.float))
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


    env_info = env.step([l_forward, l_turn])
    if l_turn == 2:
        compass.step_left()
    if l_turn == 1:
        compass.step_right()


plt.plot(t,z/50)
plt.plot(t,y)
plt.plot(t,x)
plt.show()
time.sleep(130)

pygame.quit()

env.close()
