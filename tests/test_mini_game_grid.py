import pygame


import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from components.mini_game_grid import GridWidgets


BACKGROUND_COLOR = (0, 0, 0)


def test_grid(size):
    pygame.init()
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    
    grid = GridWidgets(screen, size, 5, 5)
    grid.change_visualization(True)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                size = event.size
                grid.change_size(size)
        
        screen.fill(BACKGROUND_COLOR)
        
        grid.draw_grid()
        
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    test_grid((800, 400))
