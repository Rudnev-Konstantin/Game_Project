import pygame

import pytest
import testing

import components.widget as wd


@pytest.mark.parametrize("size", [(800, 450)])
@testing.testing_wrapper
@testing.game_loop_testing
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


@pytest.mark.parametrize("size", [(800, 450)])
@testing.testing_wrapper
@testing.game_loop_testing
def test_widget_mini_game(size):
    def init_objects(screen):
        grid_mini_game = wd.GridWidgets(screen, 7, 6)
        widget_mini_game = wd.Widget(screen,
                                     size=(int(size[0] * 0.6), int(size[1] * 0.4)), coordinates=(50, 50), radius=20, color=(125, 125, 125), content=grid_mini_game)
        
        widget_image_mini_game = wd.Widget(screen, radius=20, padding=(0.4, 0.43),
                                           content=wd.TextWidget(screen, text="image", color=(0, 0, 0)))
        grid_mini_game.add_widget(widget_image_mini_game, (0, 0), (6, 4))
        
        widget_name_mini_game = wd.TextWidget(screen, text="Name", color=(0, 0, 0))
        container_name = wd.ContainerWidget(widget_mini_game, widget_name_mini_game, padding=(0, 0.25))
        grid_mini_game.add_widget(container_name, (2, 5), (2, 1))
        
        return {"widget_mini_game": widget_mini_game}
    
    def event_cycle_conditions(event, widget_mini_game):
        if event.type == pygame.VIDEORESIZE:
            size = event.size
            widget_mini_game.set_size((int(size[0] * 0.6), int(size[1] * 0.4)))
    
    def rendering(widget_mini_game):
        widget_mini_game.draw()
    
    return init_objects, event_cycle_conditions, rendering
