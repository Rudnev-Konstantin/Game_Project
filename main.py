import pygame

import components.widget as wd


BACKGROUND_COLOR = (0, 0, 0)


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
    
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                size = event.size
                main_grid.set_size(size)
        
        screen.fill(BACKGROUND_COLOR)
        
        main_grid.draw()
        
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main((800, 450))
