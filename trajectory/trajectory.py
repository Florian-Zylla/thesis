
import numpy as np
class Trajectory:
    """
    each row contains 3 values: x,z position of current goal and approach speed
    there are 5 possible speed values (speed dividers)
    1 is full speed
    2 is full speed every second step
    3 is full speed every third step
    and so on
    """


    data = np.zeros((1, 3), dtype=np.float32)

    def __init__(self, x, z, v):
        self.data = np.array([[x, z, v]])

    def add(self, x, z, v):
        current = np.array([[x, z, v]])
        self.data = np.append(self.data,current, axis=0)

    def pop(self):
        if self.data.shape[0] == 0:
            return [-1, -1, -1]
        else:
            current = self.data[0, :]
            self.data = np.delete(self.data,0,0)
            return current

    def load(self):
        pass
    def add_path(self, other):
        self.data = np.append(self.data,other.data, axis=0)





