import pygame

import pytest
import testing

import components.widget as wd


@pytest.mark.parametrize("size", [(800, 450)])
@testing.testing_wrapper
@testing.game_loop_testing
def test_grid(size):
    def init_objects(screen):
        grid = wd.GridWidgets(screen, size, 5, 5)
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


@pytest.mark.parametrize("size", [(800, 450)])
@testing.testing_wrapper
@testing.game_loop_testing
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
