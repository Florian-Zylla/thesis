import math
class Odometry:
    pose = (0, 0)
    step = 0.0595

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
        y += speed[0, 2] * math.cos((theta / 180) * math.pi) * self.step
        y += speed[0, 0] * math.sin((theta / 180) * math.pi) * self.step
        x += speed[0, 2] * math.sin((theta / 180) * math.pi) * self.step
        x += speed[0, 0] * math.cos((theta / 180) * math.pi) * self.step
        self.pose = (x, y)
