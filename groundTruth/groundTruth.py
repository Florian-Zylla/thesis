import cv2 as cv
import numpy as np
import mss


class GroundTruth:
    # class to extract an image of the arena from the unity environment topview, later detect the agent
    # and calculate its position
    gt_pos = (0, 0)
    edge_top_left = []
    edge_bottom_right = []
    agent = []
    w_TL, h_TL = (0, 0)
    w_BR, h_BR = (0, 0)
    w_AGENT, h_AGENT = (0, 0)
    TL = (0, 0)
    BR = (0, 0)
    agent_color_up = 225 / 2
    agent_color_low = 175 / 2
    relation = 40 / 512

    def __init__(self):
        self.edge_top_left = cv.imread("edge_top_left.png", 0)
        self.edge_bottom_right = cv.imread("edge_bottom_right.png", 0)
        self.agent = cv.imread("mask_agent.png", 0)

        self.w_TL, self.h_TL = self.edge_top_left.shape[::-1]
        self.w_BR, self.h_BR = self.edge_bottom_right.shape[::-1]
        self.w_AGENT, self.h_AGENT = self.agent.shape[::-1]

    def findArena(self):
        with mss.mss() as sct:
            img = cv.cvtColor(np.array(sct.grab(sct.monitors[0])), cv.COLOR_BGRA2BGR)

            screenshot = cv.cvtColor(np.array(img), cv.COLOR_BGR2GRAY)

            res_TL = cv.matchTemplate(screenshot, self.edge_top_left, method=cv.TM_SQDIFF)
            res_BR = cv.matchTemplate(screenshot, self.edge_bottom_right, method=cv.TM_SQDIFF)

            min_val1, max_val1, min_loc1, max_loc1 = cv.minMaxLoc(res_TL)
            min_val2, max_val2, min_loc2, max_loc2 = cv.minMaxLoc(res_BR)

            self.TL = (min_loc1[0] + self.w_TL, min_loc1[1] + self.h_TL)
            self.BR = min_loc2


    def update(self):
        with mss.mss() as sct:
            img = cv.cvtColor(np.array(sct.grab(sct.monitors[0])), cv.COLOR_BGRA2BGR)
            arena = img[self.TL[1] - 10:self.BR[1] + 12, self.TL[0] - 10:self.BR[0] + 12]

            hsv_arena = cv.cvtColor(arena, cv.COLOR_BGR2HSV)
            h_arena = hsv_arena[:, :, 0]
            mask = cv.inRange(h_arena, self.agent_color_low, self.agent_color_up)

            res = cv.matchTemplate(mask, self.agent, method=cv.TM_SQDIFF)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

            top_left = min_loc

            self.gt_pos = (
            (top_left[0] + self.w_AGENT / 2) * self.relation, (512 - (top_left[1] + self.h_AGENT / 2)) * self.relation)
            if min_val > 2500000:
                self.gt_pos = (-1, -1)

            agent = arena[top_left[0]:top_left[0] + self.w_AGENT,top_left[1]:top_left[1] + self.h_AGENT ]
            cv. imwrite("agent_output.png", agent)


    def get(self):
        return self.gt_pos
