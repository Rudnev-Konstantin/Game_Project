import pygame


class CollectionTypeError(TypeError):
    def __init__(self, message="Предполагается использование коллекции.\n\tПример: (el, el), [el, el]"):
        self.message = message
        super().__init__(self.message)

class ElementsError(CollectionTypeError):
    def __init__(self, type, count, message="Неверное количество или тип элементов.\n\tПредполагаемые "):
        self.type = type
        self.count = count
        self.message = message + f"количество - {self.count}, тип - {self.type}"
        super().__init__(self.message)


class Widget:
    def __init__(self, surface, size=(0, 0), coordinates=(0, 0), color=(255, 255, 255, 255), radius=0,
                 padding=None, content=None):
        self.surface = surface
        
        self.set_coordinates(coordinates)
        self.set_size(size)
        self.set_radius(radius)
        
        self.set_color(color)
        
        try:
            self.set_padding(padding)
        except TypeError as error:
            if padding is None:
                self.padding_height = (0, 0)
                self.padding_width = (0, 0)
            else:
                raise error
        
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
            
            self.content.set_coordinates((content_x, content_y))
            self.content.set_size(self.size)
            self.content.draw()
    
    def set_coordinates(self, coordinates):
        if not (hasattr(coordinates, '__iter__')):
            raise CollectionTypeError()
        
        if not (len(coordinates) == 2 and type(coordinates[0]) == type(coordinates[1]) == int):
            raise ElementsError("int", 2)
        
        self.coordinates = coordinates
    
    def set_size(self, size):
        if not (hasattr(size, '__iter__')):
            raise CollectionTypeError()
        
        if not (len(size) == 2 and type(size[0]) == type(size[1]) == int):
            raise ElementsError("int", 2)
        
        self.size = size
    
    def set_radius(self, radius):
        if not (type(radius) == int):
            raise TypeError("Предполагается числовое значение: int")
        
        self.radius = radius
    
    def set_color(self, color):
        if not (hasattr(color, '__iter__')):
            raise CollectionTypeError()
        
        if not (len(color) == 3 and type(color[0]) == type(color[1]) == type(color[2]) == int or
                len(color) == 4 and
                type(color[0]) == type(color[1]) == type(color[2]) == type(color[3]) == int):
            raise ElementsError("int", "3 или 4")
        
        if not (max(color) <= 255 and min(color) >= 0):
            raise ValueError("Значения величины канала находится в диапазоне: 0 <= value <= 255")
        
        self.color = color
    
    def set_padding(self, padding):
        if not (hasattr(padding, '__iter__') or type(padding) == int):
            raise TypeError("Предполагается использование коллекции или числа.\
\n\tПример: (el, el), [el, el], int()")
        
        if type(padding) == int:
            self.padding_height = (padding, padding)
            self.padding_width = (padding, padding)
        elif len(padding) == 1 and type(padding[0]) == int:
            self.padding_height = (padding[0], padding[0])
            self.padding_width = (padding[0], padding[0])
        elif len(padding) == 2 and type(padding[0]) == type(padding[1]) == int:
            self.padding_height = (padding[0], padding[0])
            self.padding_width = (padding[1], padding[1])
        elif len(padding) == 4 and (type(padding[0]) == type(padding[1]) == type(padding[2])
                                    == type(padding[3]) == int):
            self.padding_height = (padding[0], padding[2])
            self.padding_width = (padding[3], padding[1])
        else:
            raise ElementsError("int", "1, 2 или 4")


class GridWidgets(Widget):
    def __init__(self, surface, size, rows, cols):
        super().__init__(surface, size)
        
        self.rows = rows
        self.cols = cols
        
        self.border_color = (255, 255, 255, 255)
        
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
    
    def set_visualization(self, state: bool):
        if not (type(state) == bool):
            raise TypeError("Предполагается логическое значение: bool")
        
        self.visualization = state


class WidgetMiniGame(Widget):
    pass
