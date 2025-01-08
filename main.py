import pygame
import random


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


def rotate(image, rect, angle):
    new_image = pygame.transform.rotate(image, angle)
    rect = new_image.get_rect(center=rect.center)
    return new_image, rect


if __name__ == '__main__':
    pygame.init()
    size = width, height = 900, 900
    screen = pygame.display.set_mode(size)

    sprite_gold_fish = pygame.sprite.Sprite()
    sprite_black_fish = pygame.sprite.Sprite()
    sprite_gold_foot = pygame.sprite.Sprite()
    sprite_black_foot = pygame.sprite.Sprite()

    image_gold_fish = load_image("gold_fish.png", -1)
    image_gold_fish = pygame.transform.scale(image_gold_fish, (300, 300))

    image_black_fish = load_image("black_fish.png", -1)
    image_black_fish = pygame.transform.scale(image_black_fish, (300, 300))

    image_gold_foot = load_image("white_foot.png", -1)
    image_gold_foot = pygame.transform.scale(image_gold_foot, (333, 333))
    image_gold_foot = pygame.transform.rotate(image_gold_foot, -45)

    image_black_foot = load_image("black_foot.webp", -1)
    image_black_foot = pygame.transform.scale(image_black_foot, (333, 333))
    image_black_foot = pygame.transform.rotate(image_black_foot, 135)

    sprite_gold_fish.image = image_gold_fish
    sprite_black_fish.image = image_black_fish
    sprite_gold_foot.image = image_gold_foot
    sprite_black_foot.image = image_black_foot

    sprite_gold_fish.rect = sprite_gold_fish.image.get_rect()
    sprite_black_fish.rect = sprite_black_fish.image.get_rect()
    sprite_gold_foot.rect = sprite_gold_foot.image.get_rect()
    sprite_black_foot.rect = sprite_black_foot.image.get_rect()

    gold_x, gold_y = (-40, 470)
    black_x, black_y = (500, -50)
    now_x, now_y = (330, 300)

    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 2000)
    running = True
    flag = False
    cnt_gold = 0
    cnt_black = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == MYEVENTTYPE:
                print("!!!!!")
                pygame.time.set_timer(MYEVENTTYPE, 0)
                now_image = random.choice([sprite_gold_fish.image, sprite_black_fish.image])
                flag = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if flag:
                    if now_image == sprite_gold_fish.image:
                        cnt_gold += 1
                    else:
                        cnt_gold -= 1
                    flag = False
                    pygame.time.set_timer(MYEVENTTYPE, 2000)
        screen.blit(sprite_gold_foot.image, (gold_x, gold_y))
        screen.blit(sprite_black_foot.image, (black_x, black_y))
        if flag:
            screen.blit(now_image, (now_x, now_y))
        pygame.display.flip()
        screen.fill(pygame.Color('cyan'))
    pygame.quit()
