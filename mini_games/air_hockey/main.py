import pygame
import random


def draw_field(screen):
    screen.fill((35, 20, 90))
    radius = 30

    pygame.draw.line(screen, (255, 255, 255), [0, height // 2], [width // 2 - radius, height // 2], 5)
    pygame.draw.line(screen, (255, 255, 255), [width // 2 + radius, height // 2], [width, height // 2], 5)

    pygame.draw.circle(screen, (255, 255, 255), (width // 2, height // 2), radius, 5)
    pygame.draw.circle(screen, (255, 255, 255), (width // 2, height // 2), 5)


def load_image(name, colorkey=None):
    image = pygame.image.load(name)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, image_name):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.set_image(image_name)
        self.vx = random.randint(-5, 5)
        self.vy = random.choice([-5, 5])
        self.count_of_hits = 0
        while self.vx == 0:
            self.vx = random.randint(-5, 5)
        # self.vy = 0
        # print(self.vx, self.vy)

    def update(self):
        global fl
        self.rect = self.rect.move(self.vx, self.vy)
        # print(self.rect)
        if pygame.sprite.spritecollideany(self, vertical_borders):
            # print(self.vx)
            self.vx = -self.vx
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            # print(self.vx)
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, random_borders):
            self.vy = -self.vy
            fl = False
            if random_border:
                random_border.clear()
                random_borders.remove(random_border)

    def set_image(self, image_name):
        size = 60
        self.image = load_image(image_name, -1)
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(center=(self.x, self.y))


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([10, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.x = width // 3
            self.y = y1
            self.rect = pygame.Rect(self.x, self.y, width // 3, 1)
            self.image = pygame.Surface([self.x, 10])
        self.image.fill((255, 127, 127))

    def move(self, vx):
        self.x += vx
        self.rect = pygame.Rect(self.x, self.y, width // 3, 1)


class Random_Border(pygame.sprite.Sprite):
    def __init__(self, x1, way):
        global width, height
        super().__init__(all_sprites)
        self.add(random_borders)
        self.image = pygame.Surface([width // 5, 5])
        if way < 0:
            self.rect = pygame.Rect(x1, height // 3, width // 5, 1)
        else:
            self.rect = pygame.Rect(x1, height * 2 // 3, width // 5, 1)

    def clear(self):
        self.image = pygame.Surface([width, height], pygame.SRCALPHA, 32)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 600, 700
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Aeroxockey')

    all_sprites = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    random_borders = pygame.sprite.Group()
    random_border = None

    image_ball = "mini_games/air_hockey/img/ballyy.jpg"
    ball = Ball(width // 2, height // 2, image_ball)

    left = Border((10 / width), 0, (10 / width), height)
    right = Border(width - 10, 0, width - 10, height)
    down = Border(0, height * 0.01, width, height * 0.01)
    up = Border(0, height - height * 0.025, width, height - height * 0.025)

    vx = 40

    fl = False
    fps = 80
    clock = pygame.time.Clock()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    up.move(-vx)
                if event.key == pygame.K_RIGHT:
                    up.move(vx)
                if event.key == pygame.K_a:
                    down.move(-vx)
                if event.key == pygame.K_d:
                    down.move(vx)
        if ball.rect.y <= height // 3 and ball.vy > 0 and not fl:
            random_border = Random_Border(random.randrange(width // 5 + 10, width - width // 5 - 10), ball.vy)
            fl = True
            # print("!!!!!!!!!!!!!")
        elif ball.rect.y >= height * 2 // 3 and ball.vy < 0 and not fl:
            random_border = Random_Border(random.randrange(width // 5 + 10, width - width // 5 - 10), ball.vy)
            fl = True
            # print("############")
        draw_field(screen)
        all_sprites.draw(screen)  # Отображение всех спрайтов
        all_sprites.update()  # Обновление всех спрайтов

        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
