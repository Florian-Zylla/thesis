class Compass:
    # simple compass class with 6 degrees accuracy

    # like a normal compass zero degrees is north=0 and turning right
    # starts to increase the value 6 degrees per step (E=90, S=180, W=270)
    orientation = 0

    def __init__(self):
        self.orientation = 0

    def set(self, orient):
        self.orientation = orient
        # orient mod 6 must always be zero
        # and should be between 0 and 359

    def get(self):
        return self.orientation

    def step_right(self):
        self.orientation += 6
        if self.orientation > 359:
            self.orientation = self.orientation % 360

    def step_left(self):
        self.orientation -= 6
        if self.orientation < 0:
            self.orientation = 360 + self.orientation
