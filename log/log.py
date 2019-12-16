import numpy as np
import time
import os

import compass.compass as c
import display.display as d
import groundTruth.groundTruth as gt
import odometry.odometry as o



class Log:
    start_time = 0
    config = 0
    data = np.zeros((1, 9), dtype=np.float32)

    def __init__(self, config):
        self.start_time = time.strftime("%d.%m.%Y-%H:%M:%S")
        config = config.strip(".yaml")
        config = config.strip("../thesis/test_configs/")

        self.config = config
    def update(self,step,speed,compass, odometry, groundtruth):
        (vx, vy, vz) = speed[0][:]
        (odox, odoy) = odometry.get_pose()
        (gtx, gty) = groundtruth.get()
        current = np.array([[step, vx, vy, vz, compass.get(), odox, odoy, gtx, gty]])
        self.data = np.append(self.data,current, axis=0)

    def save(self):

        os.chdir("/home/flo/thesis/log_files")


        np.save(self.start_time + "@" + self.config,self.data)
        print("log data saved to " + self.start_time + "@" + self.config + ".npy")
