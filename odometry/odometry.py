import math
class Odometry:
    pose = (0, 0)
    step = 0.07         #0.0595
    step_small = step/6
    old = 0
    def __init__(self):
        self.pose = (0, 0)

    def set_pose(self, input_pose):
        self.pose = input_pose

    def get_pose(self):
        return self.pose

    def update_pose(self, speed, compass):
        theta = compass.get()
        x = self.pose[0]
        y = self.pose[1]
        y += speed[0, 2] * math.cos(math.radians(theta)) * self.step
        #y += speed[0, 0] * math.sin(math.radians(theta)) * self.step
        x += speed[0, 2] * math.sin(math.radians(theta)) * self.step
        #x += speed[0, 0] * math.cos(math.radians(theta)) * self.step
        self.pose = (x, y)

    def update_pose2(self, speed, compass):
        theta = compass.get()
        x = self.pose[0]
        y = self.pose[1]
        if theta != self.old:
            theta_step = (theta-self.old)/6 #90-84 -> 1 and 90-96 -> -1
            theta_now = theta
            for a in range(6):
                y += speed[0, 2] * math.cos((theta / 180) * math.pi) * self.step_small
                #y += speed[0, 0] * math.sin((theta / 180) * math.pi) * self.step_small
                x += speed[0, 2] * math.sin((theta / 180) * math.pi) * self.step_small
                #x += speed[0, 0] * math.cos((theta / 180) * math.pi) * self.step_small

                theta_now += theta_step
        else:
            y += speed[0, 2] * math.cos((theta / 180) * math.pi) * self.step
            #y += speed[0, 0] * math.sin((theta / 180) * math.pi) * self.step
            x += speed[0, 2] * math.sin((theta / 180) * math.pi) * self.step
            #x += speed[0, 0] * math.cos((theta / 180) * math.pi) * self.step
        self.pose = (x, y)
        self.old = theta
