import pygame


class Widget:
    def __init__(self, surface, size=(0, 0), coordinates=(0, 0), color=(255, 255, 255), radius=0,
                 padding=None, content=None):
        self.surface = surface
        
        self.assign_coordinates(coordinates)
        self.assign_size(size)
        self.assign_radius(radius)
        
        self.assign_color(color)
        
        try:
            self.assign_padding(padding)
        except TypeError:
            if padding is None:
                self.padding_height = (0, 0)
                self.padding_width = (0, 0)
            else:
                raise TypeError()
        
        self.content = content
    
    def draw(self):
        x, y = self.coordinates
        width, height = self.size[0] + sum(self.padding_width), self.size[1] + sum(self.padding_height)
        
        radius = self.radius if self.radius < min(width, height) / 2 else min(width, height) // 2
        
        # закругления по краям
        pygame.draw.circle(self.surface, self.color,
                           (x + radius, y + radius), radius)
        pygame.draw.circle(self.surface, self.color,
                           (x + width - radius, y + radius), radius)
        pygame.draw.circle(self.surface, self.color,
                           (x + radius, y + height - radius), radius)
        pygame.draw.circle(self.surface, self.color,
                           (x + width - radius, y + height - radius), radius)
        
        # заполнение пустого пространства
        pygame.draw.rect(self.surface, self.color, (x + radius, y, width - 2 * radius, height))
        pygame.draw.rect(self.surface, self.color, (x, y + radius, width, height - 2 * radius))
        
        if self.content is not None:
            content_x = self.coordinates[0] + self.padding_width[0]
            content_y = self.coordinates[1] + self.padding_height[0]
            
            self.content.assign_coordinates((content_x, content_y))
            self.content.assign_size(self.size)
            self.content.draw()
    
    def assign_coordinates(self, coordinates):
        if not (hasattr(coordinates, '__iter__')):
            raise TypeError()
        
        if not (len(coordinates) == 2 and type(coordinates[0]) == type(coordinates[1]) == int):
            raise TypeError()
        
        self.coordinates = coordinates
    
    def assign_size(self, size):
        if not (hasattr(size, '__iter__')):
            raise TypeError()
        
        if not (len(size) == 2 and type(size[0]) == type(size[1]) == int):
            raise TypeError()
        
        self.size = size
    
    def assign_radius(self, radius):
        if not (type(radius) == int):
            raise TypeError()
        
        self.radius = radius
    
    def assign_color(self, color):
        if not (hasattr(color, '__iter__')):
            raise TypeError()
        
        if not (len(color) == 3 and type(color[0]) == type(color[1]) == type(color[2]) == int):
            raise TypeError()
        
        if not (max(color) <= 255 and min(color) >= 0):
            raise ValueError()
        
        self.color = color
    
    def assign_padding(self, padding):
        if not (hasattr(padding, '__iter__') or type(padding) == int):
            raise TypeError()
        
        if type(padding) == int:
            self.padding_height = (padding, padding)
            self.padding_width = (padding, padding)
        elif len(padding) == 1:
            self.padding_height = (padding[0], padding[0])
            self.padding_width = (padding[0], padding[0])
        elif len(padding) == 2:
            self.padding_height = (padding[0], padding[0])
            self.padding_width = (padding[1], padding[1])
        elif len(padding) == 4:
            self.padding_height = (padding[0], padding[2])
            self.padding_width = (padding[3], padding[1])
        else:
            raise TypeError()


class GridWidgets(Widget):
    def __init__(self, surface, size, rows, cols):
        super().__init__(surface, size)
        
        self.rows = rows
        self.cols = cols
        
        self.border_color = (255, 255, 255)
        
        self.visualization = False
    
    def draw(self):
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
    
    def assign_visualization(self, state: bool):
        if not (type(state) == bool):
            raise TypeError()
        
        self.visualization = state


class WidgetMiniGame(Widget):
    pass
