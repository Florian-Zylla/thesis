from animalai.envs.environment import UnityEnvironment
from animalai.envs.arena_config import ArenaConfig
import matplotlib
from matplotlib import pyplot as plt
import random
import pygame
import numpy as np
import time
import array
def rect_detect(array,c_min,c_max,start,end):
    for i in range(start[0],end[0]):
        for j in range(start[1],end[1]):
            if array[i,j,0]>c_min and array[i,j,0]<c_max:
                return True
    return False


# initial settings of the environment
env = UnityEnvironment(
    n_arenas=1,
    file_name='../env/AnimalAI',
    worker_id=random.randint(1, 100),
    seed=0,
    docker_training=False,
    inference=False,
    # resolution=512,
    #play=True
)

# configuration of objects inside the environment
print("Start")
arena_config_in = ArenaConfig('../code/acceleration_speed_test.yaml')
env_info = env.reset(arenas_configurations=arena_config_in)


raw_img = (np.random.rand(84, 84,3)*255).astype(np.uint8)
print(raw_img.shape)
pygame.init()
display = pygame.display.set_mode((420, 420))
pygame.display.set_caption('agents observation')
x = np.arange(0, 420)
y = np.arange(0, 420)
X, Y = np.meshgrid(x, y)
surf = pygame.surfarray.make_surface(raw_img)

turn_steps = 0
speed_x = []
speed_y = []
speed_z = []
a = []
t = []
dt = 0.059
s = 0

# the agent will take 20 time steps as an example
for i in range(120):

    # velocity
    speed = env_info['Learner'].vector_observations


    speed_x.append(speed[0][0])
    speed_y.append(speed[0][1])
    speed_z.append(speed[0][2])
    if i == 0:
        a.append(speed_z[0])
    else:
        a.append(speed_z[i]-speed_z[i-1])
    t.append(i)

    if i == 0:
        s += speed_z[i] * dt
    else:
        s += (speed_z[i] + speed_z[i-1])* (dt/2)
    print(s)
    # camera input
    observation = env_info['Learner'].visual_observations[0]

    # Scaling RGB camera from 0-1 to 0-255
    raw_img = (observation[0, :, :, :]*255).astype(np.uint8)
    raw_img = np.flipud(np.rot90(raw_img))
   # hsv_img = rgb2hsv_array(raw_img)
    hsv_img = matplotlib.colors.rgb_to_hsv((observation[0, :, :, :]).astype(np.float))

    ### Do some calculation with your observations here
    surf = pygame.surfarray.make_surface(raw_img)
    surf2 = pygame.transform.smoothscale(surf,(420,420))
    surf = pygame.transform.scale(surf,(420,420))

    #surf3 = pygame.transform.laplacian(surf)
    display.blit(surf, (0, 0))

    pygame.display.update()
    env_info = env.step([1, 0])
    #if i%2 == True :
     #   env_info = env.step([1,0])
    #else:
     #  env_info = env.step([0, 0])
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

print(a)
print(speed_z)
plt.plot(t,a)
plt.plot(t,speed_z)
plt.show()

time.sleep(3)
pygame.quit()
env.close()