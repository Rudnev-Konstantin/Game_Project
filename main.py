import pygame


BACKGROUND_COLOR = (0, 0, 0)


def main(size):
    pygame.init()
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                size = event.size
        
        screen.fill(BACKGROUND_COLOR)
        
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main((800, 400))
