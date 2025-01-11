import pygame


class GridWidgets:
    def __init__(self, surface, size, rows, cols):
        self.surface = surface
        
        self.size = size
        self.rows = rows
        self.cols = cols
        
        self.border_color = (255, 255, 255)
        
        self.visualization = False
    
    def draw_grid(self):
        width, height = self.size
        
        cell_width = width // self.cols
        cell_height = height // self.rows
        
        if self.visualization:
            self.grid_visualization(width, height, cell_width, cell_height)
        else:
            pass
    
    def grid_visualization(self, width, height, cell_width, cell_height):
        if cell_height == 0 or cell_width == 0:
            return
        
        for x in range(0, width, cell_width):
            pygame.draw.line(self.surface, self.border_color, (x, 0), (x, height))
        
        for y in range(0, height, cell_height):
            pygame.draw.line(self.surface, self.border_color, (0, y), (width, y))
    
    def change_visualization(self, state: bool):
        assert type(state) == bool
        
        self.visualization = state
    
    def change_size(self, size):
        assert len(size) == 2 and type(size[0]) == type(size[1]) == int
        
        self.size = size


class WidgetMiniGame:
    pass
