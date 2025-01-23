import pygame

import subprocess
import sys

import components.widget as wd


BACKGROUND_COLOR = (139, 195, 74)


def get_mini_game_widget(screen):
    grid_mini_game = wd.GridWidgets(screen, 7, 6)
    widget_mini_game = wd.WidgetMiniGame(screen, coordinates=(50, 50), radius=20, color=(125, 125, 125),
                                         content=grid_mini_game)
    
    widget_image_mini_game = wd.Widget(screen, radius=20, padding=(0.4, 0.43),
                                        content=wd.TextWidget(screen, text="image", color=(0, 0, 0)))
    grid_mini_game.add_widget(widget_image_mini_game, (0, 0), (6, 4))
    
    widget_name_mini_game = wd.TextWidget(screen, text="Name", color=(0, 0, 0))
    container_name = wd.ContainerWidget(widget_mini_game, widget_name_mini_game, padding=(0, 0.25))
    grid_mini_game.add_widget(container_name, (2, 5), (2, 1))
    
    return widget_mini_game


def main(size):
    pygame.init()
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    pygame.display.set_caption("Mini Game")
    
    main_grid = wd.GridWidgets(screen, 6, 1, size=size)
    main_grid.set_visualization(False)
    
    header_grid = wd.GridWidgets(screen, 1, 10)
    header = wd.Widget(screen, color=(125, 125, 125), radius=10, content=header_grid)
    cont_header = wd.Widget(screen, color=BACKGROUND_COLOR, 
                            padding=(int(size[0] * 0.01), int(size[1] * 0.05)), content=header)
    main_grid.add_widget(cont_header, (0, 0), (1, 1))
    
    logo = wd.Widget(screen, radius=20)
    cont_logo = wd.ContainerWidget(header, logo, padding=(10, 20))
    header_grid.add_widget(cont_logo, (0, 0), (2, 1))
    
    catalog_mini_game = wd.GridWidgets(screen, 3, 3)
    catalog_mini_game.set_visualization(True)
    catalog_mini_game.set_padding((int(size[0] * 0.05), int(size[1] * 0.05)))
    main_grid.add_widget(catalog_mini_game, (0, 1), (1, 5))
    
    
    mini_game_1 = get_mini_game_widget(screen)
    mini_game_1.set_path("air_hockey")
    catalog_mini_game.add_widget(mini_game_1, (0, 0), (1, 1))
    
    mini_game_2 = get_mini_game_widget(screen)
    mini_game_2.set_path("cat_foots")
    catalog_mini_game.add_widget(mini_game_2, (1, 0), (1, 1))
    
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                size = event.size
                main_grid.set_size(size)
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_cur, y_cur = event.pos
                
                for widget_mini_game in catalog_mini_game.widgets:
                    widget = widget_mini_game["widget"]
                    
                    wd_coord = widget.coordinates
                    wd_size = widget.size
                    
                    if wd_coord[0] <= x_cur <= wd_coord[0] + wd_size[0]:
                        if wd_coord[1] <= y_cur <= wd_coord[1] + wd_size[1]:
                            subprocess.run([sys.executable, widget.path])
        
        screen.fill(BACKGROUND_COLOR)
        
        main_grid.draw()
        
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main((800, 450))
