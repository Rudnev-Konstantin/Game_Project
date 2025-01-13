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
    pygame.display.set_caption('Cats and fishes')
    font = pygame.font.Font(None, 100)

    sprite_gold_fish = pygame.sprite.Sprite()
    sprite_black_fish = pygame.sprite.Sprite()
    sprite_gold_foot = pygame.sprite.Sprite()
    sprite_black_foot = pygame.sprite.Sprite()

    image_gold_fish = load_image("images/gold_fish.png", -1)
    image_gold_fish = pygame.transform.scale(image_gold_fish, (300, 300))

    image_black_fish = load_image("images/black_fish.png", -1)
    image_black_fish = pygame.transform.scale(image_black_fish, (300, 300))

    image_gold_foot = load_image("images/white_foot.png", -1)
    image_gold_foot = pygame.transform.scale(image_gold_foot, (333, 333))
    image_gold_foot = pygame.transform.rotate(image_gold_foot, -45)

    image_black_foot = load_image("images/white_foot.png", -1)
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

    gold_xx, gold_yy = (260, 200)
    black_xx, black_yy = (260, 200)

    image_phone = load_image("images/wood.jpg", -1)
    image_phone = pygame.transform.scale(image_phone, (900, 900))

    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 2000)

    NEWEVENTTYPE = pygame.USEREVENT + 1

    running = True
    flag = False
    flag_new_fish = False
    flag_gold_foot = False
    flag_black_foot = False

    cnt_gold = 0
    cnt_black = 0

    fps = 10
    clock = pygame.time.Clock()

    cnt_fishes = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == MYEVENTTYPE:
                pygame.time.set_timer(NEWEVENTTYPE, 2000)
                now_image = random.choice([sprite_gold_fish.image, sprite_black_fish.image])
                flag = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if flag:
                    if now_image == sprite_gold_fish.image:
                        cnt_gold += 1
                    else:
                        cnt_gold -= 1
                    flag = False
                    flag_gold_foot = True
                    pygame.time.set_timer(MYEVENTTYPE, 2000)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if flag:
                        if now_image == sprite_gold_fish.image:
                            cnt_black += 1
                        else:
                            cnt_black -= 1
                        flag = False
                        flag_black_foot = True
                        pygame.time.set_timer(MYEVENTTYPE, 2000)
            if event.type == NEWEVENTTYPE:
                pygame.time.set_timer(MYEVENTTYPE, 2000)

        screen.blit(image_phone, (0, 0))

        if not flag_gold_foot:
            screen.blit(sprite_gold_foot.image, (gold_x, gold_y))
        else:
            screen.blit(sprite_gold_foot.image, (gold_xx, gold_yy))
            flag_gold_foot = False

        if not flag_black_foot:
            screen.blit(sprite_black_foot.image, (black_x, black_y))
        else:
            screen.blit(sprite_black_foot.image, (black_xx, black_yy))
            flag_black_foot = False

        text_gold = font.render(f"Счёт: {cnt_gold}", True, (255, 255, 255))
        text_gold_rect = text_gold.get_rect(center=(150, 520))
        screen.blit(text_gold, text_gold_rect)

        text_black = font.render(f"Счёт: {cnt_black}", True, (0, 0, 0))
        text_black_rect = text_black.get_rect(center=(750, 360))
        screen.blit(text_black, text_black_rect)

        if flag:
            screen.blit(now_image, (now_x, now_y))

        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
