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
        width, height = self.size
        
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
        
        # отрисовка контента
        if self.content is not None:
            if isinstance(self.padding_width[0], int):
                padding_width = [self.padding_width[0]]
            else:
                padding_width = [int(self.padding_width[0] * width)]
            
            if isinstance(self.padding_height[0], int):
                padding_height = [self.padding_height[0]]
            else:
                padding_height = [int(self.padding_height[0] * height)]
            
            if isinstance(self.padding_width[1], int):
                padding_width.append(self.padding_width[1])
            else:
                padding_width.append(int(self.padding_width[1] * width))
            
            if isinstance(self.padding_height[1], int):
                padding_height.append(self.padding_height[1])
            else:
                padding_height.append(int(self.padding_height[1] * height))
            
            content_x = self.coordinates[0] + padding_width[0]
            content_y = self.coordinates[1] + padding_height[0]
            
            width_content = self.size[0] - sum(padding_width)
            height_content = self.size[1] - sum(padding_height)
            
            self.content.set_coordinates((content_x, content_y))
            self.content.set_size((width_content, height_content))
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
        if not (hasattr(padding, '__iter__') or isinstance(padding, (int, float))):
            raise TypeError("Предполагается использование коллекции или числа.\
\n\tПример: (el, el), [el, el], int(), float()")
        
        if hasattr(padding, '__iter__'):
            for padding_item in padding:
                if isinstance(padding_item, float) and not (0 <= padding_item <= 1):
                    raise ValueError("Padding в частях от size находится в приделах: 0 <= padding <= 1")
        
        if isinstance(padding, (int, float)):
            self.padding_height = (padding, padding)
            self.padding_width = (padding, padding)
        elif len(padding) == 1 and isinstance(padding[0], (int, float)):
            self.padding_height = (padding[0], padding[0])
            self.padding_width = (padding[0], padding[0])
        elif len(padding) == 2 and all(isinstance(p, (int, float)) for p in padding):
            self.padding_height = (padding[0], padding[0])
            self.padding_width = (padding[1], padding[1])
        elif len(padding) == 4 and all(isinstance(p, (int, float)) for p in padding):
            self.padding_height = (padding[0], padding[2])
            self.padding_width = (padding[3], padding[1])
        else:
            raise ElementsError("int, float", "1, 2 или 4")


class ContainerWidget(Widget):
    def __init__(self, fond, widget, padding=None):
        base_attributes = vars(Widget(None)).copy()
        attributes = vars(fond).copy()
        
        fond_attributes = dict()
        for attribute in attributes:
            if attribute in base_attributes:
                fond_attributes[attribute] = attributes[attribute]
        if padding is None:
            padding = list(fond_attributes.pop("padding_height"))
            padding += list(fond_attributes.pop("padding_width"))
        else:
            fond_attributes.pop("padding_height")
            fond_attributes.pop("padding_width")
            self.set_padding(padding)
            padding = list(self.padding_height) + list(self.padding_width)
        padding[1], padding[3] = padding[3], padding[1]
        padding[2], padding[3] = padding[3], padding[2]
        fond_attributes["padding"] = padding
        fond_attributes["content"] = widget
        super().__init__(**fond_attributes)


class TextWidget(Widget):
    def __init__(self, surface, size=(0, 0), coordinates=(0, 0), color=(255, 255, 255, 255),
                 text=''):
        super().__init__(surface, size=size, coordinates=coordinates, color=color)
        self.set_text(text)
        
        self.font_size = 1
    
    def draw(self):
        font = pygame.font.Font(None, self.font_size)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_width, text_height = text_surface.get_size()
        
        if text_width < self.size[0] or text_height < self.size[1]:
            while True:
                font = pygame.font.Font(None, self.font_size)
                text_surface = font.render(self.text, True, (0, 0, 0))
                text_width, text_height = text_surface.get_size()
                
                if text_width > self.size[0] or text_height > self.size[1]:
                    break
                
                self.font_size += 1
            
            font = pygame.font.Font(None, self.font_size)
            text_surface = font.render(self.text, True, self.color)
            self.surface.blit(text_surface, self.coordinates)
        elif text_width > self.size[0] or text_height > self.size[1]:
            while True:
                font = pygame.font.Font(None, self.font_size)
                text_surface = font.render(self.text, True, (0, 0, 0))
                text_width, text_height = text_surface.get_size()
                
                if text_width < self.size[0] or text_height < self.size[1]:
                    break
                
                self.font_size -= 1
            
            font = pygame.font.Font(None, self.font_size)
            text_surface = font.render(self.text, True, self.color)
            self.surface.blit(text_surface, self.coordinates)
    
    def set_text(self, text):
        if not (type(text) == str):
            raise TypeError("Предполагается строковое значение: str")
        
        self.text = text


class GridWidgets(Widget):
    def __init__(self, surface, rows, cols, size=(0, 0)):
        super().__init__(surface, size)
        
        self.rows = rows
        self.cols = cols
        
        self.border_color = (255, 255, 255, 255)
        
        self.widgets = []
        
        self.visualization = False
    
    def draw(self):
        x_grid = self.coordinates[0] + self.padding_width[0]
        y_grid = self.coordinates[1] + self.padding_height[0]
        
        width = self.size[0] - sum(self.padding_width)
        height = self.size[1] - sum(self.padding_height)
        
        cell_width = width // self.cols
        cell_height = height // self.rows
        
        if self.visualization:
            self.grid_visualization((x_grid, y_grid), (width, height), (cell_width, cell_height))
        
        for struct_widget in self.widgets:
            widget = struct_widget["widget"]
            coordinates, size = struct_widget["coordinates"], struct_widget["size"]
            
            real_value = lambda p_1, p_2: (cell_width * p_1, cell_height * p_2)
            
            coordinates = real_value(*coordinates)
            coordinates = (coordinates[0] + x_grid, coordinates[1] + y_grid)
            size = real_value(*size)
            
            widget.set_coordinates(coordinates)
            widget.set_size(size)
            widget.draw()
    
    def add_widget(self, widget: Widget, coordinates, size):
        if not (isinstance(widget, Widget) or issubclass(type(widget), Widget)):
            raise TypeError("Предполагаемое значение принадлежит классу: Widget")
        
        if not (hasattr(coordinates, '__iter__')):
            raise CollectionTypeError()
        if not (len(coordinates) == 2 and type(coordinates[0]) == type(coordinates[1]) == int):
            raise ElementsError("int", 2)
        
        if not (hasattr(size, '__iter__')):
            raise CollectionTypeError()
        if not (len(size) == 2 and type(size[0]) == type(size[1]) == int):
            raise ElementsError("int", 2)
        
        
        vertical_border = coordinates[0] >= 0 and coordinates[0] + size[0] - 1 < self.cols
        horizontal_border = coordinates[1] >= 0 and coordinates[1] + size[1] - 1 < self.rows
        if not (vertical_border and horizontal_border):
            raise ValueError("Добавляемый элемент выходит за границы сетки")
        
        for struct_widget in self.widgets:
            intersections = [False, False]
            for i in range(2):
                point_1 = struct_widget["coordinates"][i]
                point_2 = struct_widget["coordinates"][i] + struct_widget["size"][i] - 1
                
                if coordinates[i] <= point_1 <= coordinates[i] + size[i] - 1:
                    intersections[i] = True
                if coordinates[i] <= point_2 <= coordinates[i] + size[i] - 1:
                    intersections[i] = True
            if all(intersections):
                raise ValueError("Добавляемый элемент пересекает другие элементы")
        
        
        self.widgets.append({"widget": widget, "coordinates": coordinates, "size": size})
    
    def add_widgets(self, widgets):
        try:
            for struct_widget in widgets:
                self.add_widget(*struct_widget)
        except Exception as error:
            raise error from Exception("Задайте Структуру вида: ((widget, coordinates, size), \
((widget, coordinates, size), ...)")
    
    def grid_visualization(self, coordinates, size, cell):
        x_grid, y_grid = coordinates
        width, height = size
        cell_width, cell_height = cell
        
        if cell_height == 0 or cell_width == 0:
            return
        
        for x in range(x_grid, width + x_grid + 1, cell_width):
            pygame.draw.line(self.surface, self.border_color, (x, y_grid), (x, height + y_grid))
        
        for y in range(y_grid, height + y_grid + 1, cell_height):
            pygame.draw.line(self.surface, self.border_color, (x_grid, y), (width + x_grid, y))
    
    def set_visualization(self, state: bool):
        if not (type(state) == bool):
            raise TypeError("Предполагается логическое значение: bool")
        
        self.visualization = state


class WidgetMiniGame(Widget):
    def __init__(self, surface, size=(0, 0), coordinates=(0, 0), color=(255, 255, 255, 255), radius=0, padding=None, content=None, path="mini_games/"):
        super().__init__(surface, size, coordinates, color, radius, padding, content)
        
        self.path = path
    
    def set_path(self, path):
        self.path += path + "/main.py"
    
    def is_tach(self):
        pass
