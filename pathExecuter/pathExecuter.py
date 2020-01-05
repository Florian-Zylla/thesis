import math
import numpy as np
import trajectory as t

def diff_angles(a,b):
    diff_theta = abs(a - b)%360
    if diff_theta > 180:
        diff_theta = 360 -diff_theta
    if (a-b >= 0 and a-b <= 180) or (a-b<=-180 and a-b>=-360):
        diff_theta *= -1
    return diff_theta


class pathExecuter:
    """
    each row contains 3 values: x,z position of current goal and approach speed
    there are 5 possible speed values (speed dividers)
    1 is full speed
    2 is full speed every second step
    3 is full speed every third step
    and so on
    """

    path = 0
    end = False
    goal = 0
    def __init__(self, path):
        self.path = path
        self.goal = path.pop()
    def calc_action(self,i,odo,head):
        action = [0,0]
        # speed control
        if i % self.goal[2] == 0:
            action[0] = 1
        else:
            action[0] = 0

        # rotation
        delta_x = self.goal[0] - odo.get_pose()[0]
        delta_z = self.goal[1] - odo.get_pose()[1]
        dist = math.sqrt(math.pow(delta_x, 2) + math.pow(delta_z, 2))
        goal_theta = -90 + math.degrees(math.atan2(delta_z, delta_x))
        if goal_theta < -179:
            goal_theta = 360 + goal_theta

        diff_theta = diff_angles(goal_theta, head.get())

        # 5 -> 0.3
        if dist > 2:
            if diff_theta > 3:
                action[1] = 1
            elif diff_theta < -3:
                action[1] = 2
            else:
                action[1] = 0

            if diff_theta > 10 or diff_theta < -10:
                action[0] = 0
        else:
            self.goal = self.path.pop()
            if sum(self.goal) == -3:
                self.end = True

        if self.end == True:
            action = [0, 0]
        return action




