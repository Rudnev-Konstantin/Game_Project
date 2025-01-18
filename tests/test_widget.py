import pygame


import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import components.widget as wd


BACKGROUND_COLOR = (0, 0, 0)


def test_grid(size):
    pygame.init()
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    
    grid = wd.GridWidgets(screen, size, 5, 5)
    grid.assign_visualization(True)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                size = event.size
                grid.assign_size(size)
        
        screen.fill(BACKGROUND_COLOR)
        
        grid.draw()
        
        pygame.display.flip()
    pygame.quit()


def test_widget(size):
    pygame.init()
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    
    widget = wd.Widget(screen, size=(int(size[0] * 0.6), int(size[1] * 0.4)), coordinates=(10, 10),
                       radius=60, padding=(60, 30), content=wd.Widget(screen, color=(0, 255, 0)))
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                size = event.size
                widget.assign_size((int(size[0] * 0.6), int(size[1] * 0.4)))
        
        screen.fill(BACKGROUND_COLOR)
        
        widget.draw()
        
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    test_grid((800, 400))
    test_widget((800, 400))
