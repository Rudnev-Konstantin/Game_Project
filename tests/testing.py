import pygame


import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)


BACKGROUND_COLOR = (0, 0, 0)


def testing_wrapper(func):
    def wrapper(size):
        try:
            func(size=size)
            assert True
        except Exception as error:
            assert False, error
    
    return wrapper


def game_loop_testing(func):
    def wrapper(*args, **kwargs):
        init_objects, event_cycle_conditions, rendering = func(*args, **kwargs)
        
        
        pygame.init()
        screen = pygame.display.set_mode(kwargs["size"], pygame.RESIZABLE)
        
        objects = init_objects(screen=screen)
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                event_cycle_conditions(event=event, **objects)
            
            screen.fill(BACKGROUND_COLOR)
            
            rendering(**objects)
            
            pygame.display.flip()
        pygame.quit()
    
    return wrapper
