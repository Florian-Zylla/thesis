from animalai.envs.environment import UnityEnvironment
from animalai.envs.arena_config import ArenaConfig
import matplotlib
import random
import pygame
import numpy as np
import time
import compass as c
import display as d

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
    # play=True,
)

# configuration of objects inside the environment
print("Start")
arena_config_in = ArenaConfig('../thesis/test_configs/rotational_step_width.yaml')
env_info = env.reset(arenas_configurations=arena_config_in)



display = d.Display()
# initalisation
compass = c.Compass()



# the agent will take 20 time steps as an example
for i in range(361):

    # velocity
    speed = env_info['Learner'].vector_observations
    #print("speed: ", speed)

    # camera input
    observation = env_info['Learner'].visual_observations[0]
    display.update(observation, compass)




    hsv_img = matplotlib.colors.rgb_to_hsv((observation[0, :, :, :]).astype(np.float))

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
time.sleep(10)

pygame.quit()

env.close()