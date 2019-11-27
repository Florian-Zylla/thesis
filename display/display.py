import pygame
import numpy as np
import compass as c


class Display:
    #class to display and transform the observation into a window
    #in the bottom area of the window, the local direction and local position are displayed
    display = pygame.display.set_mode((420, 420))
    raw_img = np.ones((84,84,3),dtype=np.int8)*255
    font = 0
    textRect = 0
    def __init__(self):

        #init pygame
        pygame.init()
        display = pygame.display.set_mode((420, 420))
        pygame.display.set_caption('agents observation')

        # init font and text location
        self.font = pygame.font.Font(None, 31)
        text = self.font.render("INIT", True, (0, 0, 0)) # render text
        self.textRect = text.get_rect()
        self.textRect.center = (390, 405)


        #create and scale up observation
        surf = pygame.surfarray.make_surface(self.raw_img)
        surf = pygame.transform.scale(surf, (420, 420))

        #write image and text
        self.display.blit(surf, (0, 0))
        self.display.blit(text, self.textRect)

        #update window
        pygame.display.update()


    def update(self,observation, compass):

        # Scaling RGB camera from 0-1 to 0-255, upsize  and rotate image
        raw_img = (observation[0, :, :, :] * 255).astype(np.uint8)
        raw_img = np.flipud(np.rot90(raw_img))
        surf = pygame.surfarray.make_surface(raw_img)
        surf = pygame.transform.scale(surf, (420, 420))

        #render text
        text = self.font.render(str(compass.get()) + "°", True, (0, 0, 0))

        #write image and text
        self.display.blit(surf, (0, 0))
        self.display.blit(text, self.textRect)

        #update window
        pygame.display.update()


