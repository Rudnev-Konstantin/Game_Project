import pygame


import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import components.widget as wd


BACKGROUND_COLOR = (0, 0, 0)


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


@game_loop_testing
def test_grid(size):
    def init_objects(screen):
        grid = wd.GridWidgets(screen, 5, 5, size=size)
        grid.set_visualization(True)
        grid.set_padding(40)
        
        widget_1 = wd.Widget(screen, color=(255, 0, 0), radius=60, padding=30,
                             content=wd.Widget(screen, color=(0, 0, 0)))
        widget_2 = wd.Widget(screen, color=(0, 255, 0))
        widget_3 = wd.Widget(screen, color=(0, 0, 255), radius=500)
        
        grid_widgets = (
            (widget_1, (2, 1), (1, 3)),
            (widget_2, (0, 0), (2, 2)),
            (widget_3, (4, 4), (1, 1)),
            (widget_1, (3, 0), (2, 4))
        )
        
        grid.add_widgets(grid_widgets)
        
        return {"grid": grid}
    
    def event_cycle_conditions(event, grid):
        if event.type == pygame.VIDEORESIZE:
            size = event.size
            grid.set_size(size)
    
    def rendering(grid):
        grid.draw()
    
    return init_objects, event_cycle_conditions, rendering


@game_loop_testing
def test_widget(size):
    def init_objects(screen):
        widget = wd.Widget(screen, size=(int(size[0] * 0.6), int(size[1] * 0.4)), coordinates=(50, 50),
                       radius=60, padding=(60, 30), content=wd.Widget(screen, color=(0, 255, 0)))
        
        return {"widget": widget}
    
    def event_cycle_conditions(event, widget):
        if event.type == pygame.VIDEORESIZE:
            size = event.size
            widget.set_size((int(size[0] * 0.6), int(size[1] * 0.4)))
    
    def rendering(widget):
        widget.draw()
    
    return init_objects, event_cycle_conditions, rendering


if __name__ == '__main__':
    test_grid(size=(800, 450))
    test_widget(size=(800, 450))
