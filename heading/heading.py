class Heading:
    """
    class contains a simple euler angle representation with some functions for
    easy access and manipulation

    from -179 to 180
    """
    orientation = 0

    def __init__(self):
        self.orientation = 0

    def set(self, orient):
        self.orientation = orient
        # orient mod 6 must always be zero
        # and should be between -179 and 180

    def get(self):
        return self.orientation

    def update(self,action):

        if action == 2:
            self.orientation += 6
            if self.orientation > 180:
                self.orientation = self.orientation - 360

        if action == 1:
            self.orientation -= 6
            if self.orientation < -179:
                self.orientation = 360 + self.orientation

