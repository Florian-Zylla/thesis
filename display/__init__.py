import pygame
import numpy as np
import compass as c
import groundTruth as gt

class Display:
    #class to display and transform the observation into a window
    #in the bottom area of the window, the local direction and local position are displayed
    display = pygame.display.set_mode((420, 420))
    raw_img = np.ones((84,84,3),dtype=np.int8)*255
    font = 0
    textRect_loc_rot = 0
    textRect_pos_gt = 0
    def __init__(self):

        #init pygame
        pygame.init()
        display = pygame.display.set_mode((420, 420))
        pygame.display.set_caption('agents observation')

        # init font and text location
        self.font = pygame.font.Font(None, 31)
        text_loc_rot = self.font.render("INIT", True, (0, 0, 0)) # render text
        self.textRect_loc_rot = text_loc_rot.get_rect()
        self.textRect_loc_rot.center = (390, 405)

        text_pos_gt = self.font.render("x: 12.34 y: 56.78", True, (0, 0, 0))  # render text
        self.textRect_pos_gt= text_pos_gt.get_rect()
        self.textRect_pos_gt.center = (85, 405)

        #create and scale up observation
        surf = pygame.surfarray.make_surface(self.raw_img)
        surf = pygame.transform.scale(surf, (420, 420))

        #write image and text
        self.display.blit(surf, (0, 0))
        self.display.blit(text_loc_rot, self.textRect_loc_rot)
        self.display.blit(text_pos_gt, self.textRect_pos_gt)
        #update window
        pygame.display.update()


    def update(self,observation, compass,gt):

        # Scaling RGB camera from 0-1 to 0-255, upsize  and rotate image
        raw_img = (observation[0, :, :, :] * 255).astype(np.uint8)
        raw_img = np.flipud(np.rot90(raw_img))
        surf = pygame.surfarray.make_surface(raw_img)
        surf = pygame.transform.scale(surf, (420, 420))

        #render text
        text_loc_rot = self.font.render(str(compass.get()) + "°", True, (0, 0, 0))
        text_pos_gt = self.font.render("x: " + str(round(gt.get()[0],2))+ " y: " + str(round(gt.get()[1],2)), True, (0, 0, 0))  # render text

        #write image and text
        self.display.blit(surf, (0, 0))
        self.display.blit(text_loc_rot, self.textRect_loc_rot)
        self.display.blit(text_pos_gt, self.textRect_pos_gt)
        #update window
        pygame.display.update()


